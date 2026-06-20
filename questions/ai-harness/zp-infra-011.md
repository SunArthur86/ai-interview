---
id: zp-infra-011
difficulty: L4
category: ai-harness
subcategory: 工程化
tags:
- 智谱
- 面经
- 分布式训练
- ZeRO
- 3D Parallelism
- 系统设计
feynman:
  essence: 通过KV分层管理和前缀复用最大化算力利用率。
  analogy: 像图书馆管理，热门书放手边（GPU），旧书放书架（CPU），封存书放仓库（SSD）。
  first_principle: 如何在高并发下最大化 GPU 显存利用率和计算效率？
  key_points:
  - KV Cache 分层（GPU/CPU/SSD）
  - 前缀复用减少重复计算
  - 连续批处理提升吞吐
  - 基于KV占用率的负载均衡
follow_up:
- KV Cache 从 CPU 换回 GPU 有多快？—— PCIe 4.0 约 64GB/s，1M token KV（~10GB）约 0.15s
- 怎么监控 Agent Serving 健康？—— P99 延迟、KV 命中率、GPU 利用率、队列深度
- 如何处理突发流量？—— 请求排队 + 优先级调度 + 自动扩缩 GPU 实例
---

# 【智谱Infra面经】设计一个支持 1M 上下文 + 多模态的高并发 Agent Serving 系统，如何处理调度、KV 管理和负载均衡？

**百万级 Agent Serving 系统设计（增强版）：**

**整体架构：**

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                              Client Requests                              │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        API Gateway (L7 LB)                               │
│  (Auth / Rate Limit / Request Routing / Telemetry)                       │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          Scheduler Controller                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                    │
│  │ Request      │  │ Prefix       │  │ Dynamic      │                    │
│  │ Classifier   │──│ Analyzer     │──│ Batcher      │                    │
│  │ (Agent/Chat) │  │ (Radix Tree) │  │ (Iterative)  │                    │
│  └──────────────┘  └──────────────┘  └──────────────┘                    │
└──────────┬──────────────────────────────┬───────────────────────┬──────────┘
           │                              │                       │
           ▼                              ▼                       ▼
  ┌────────────────┐            ┌────────────────┐      ┌──────────────────┐
  │   KV Cache     │            │  GPU Cluster   │      │  Worker Nodes    │
  │   Manager      │            │  (vLLM/SGLang) │      │  (Host LLM)      │
  │                │            │                │      │                  │
  │ ┌────────────┐ │            │ ┌────────────┐ │      │ (Small Models)   │
  │ │GPU HBM     │◄────────────┤ │Block Mgr   │ │      │                  │
  │ │(Hot/Active)│ │    Swap    │ │(PagedAttn) │ │      └──────────────────┘
  │ └────────────┘ │            │ └────────────┘ │
  │ ┌────────────┐ │            │ ┌────────────┐ │
  │ │CPU RAM     │◄────────────┤ │Compute     │ │
  │ │(Warm/Swap) │ │  (PCIe/NV)│ │Kernel      │ │
  │ └────────────┘ │            │ └────────────┘ │
  │ ┌────────────┐ │            │                │
  │ │SSD / Obj   │ │            │   TP/PP Group  │
  │ │(Cold/Offload)│             │                │
  │ └────────────┘ │            └────────────────┘
  └────────────────┘
```

**关键设计点（深度解析）：**

1.  **KV Cache 分层管理**
    *   **热**：当前活跃请求的 KV Blocks → GPU HBM（通过 `BlockManager` 管理物理块）。
    *   **温**：Agent 多轮对话历史或 Tool Calling 等待时的上下文 → CPU RAM（利用 `cpu_offload` 机制）。
    *   **冷**：长时间挂起会话 → SSD/NVMe（释放 CPU 内存，仅保留元数据）。
    *   **原理细节**：基于引用计数或 LRU 策略进行换出。在 Agent 调用工具时，模型推理暂停，此时 KV 必须卸载到 CPU 以腾出 GPU 给其他请求，工具返回后再从 CPU 换入 GPU 继续生成。

2.  **前缀复用（RadixAttention）
    *   **原理**：将 System Prompt、Tool Definition 等静态长文本计算出的 KV Cache 存储在全局共享内存中。
    *   **实现**：使用 Radix Tree（基数树）管理 KV Block 的逻辑索引。新请求到来时，只需计算 Prompt 的变动部分，直接指针指向共享的物理 Block。
    *   **边界**：需要处理 Cuda Graph 的捕获问题（动态共享前缀可能破坏图），通常需要 Partial Capture 或 fallback 机制。

3.  **动态批处理**
    *   **策略**：采用 **Continuous Batching**（或称 Iterative Scheduling）。
    *   **流程**：
        1.  Scheduler 轮询所有 Running Batch。
        2.  对于已经 `finished` 的 slot，立即释放并加入 `free_queue`。
        3.  从 `waiting_queue` 中选取新请求，如果剩余 free blocks 足够其 prefill 阶段需求，则立即插队加入当前 batch。
    *   **优势**：消除了传统 Static Batching 中必须等最慢请求结束的 Padding 浪费，显著提升 GPU利用率。

4.  **负载均衡与调度策略**
    *   **指标**：不仅是 `Concurrent Requests`，更核心是 **`KV Cache Utilization`**（剩余 Block 数量）。
    *   **算法**：加权最小连接数或一致性哈希。将长上下文请求路由到剩余显存较大的节点，避免因碎片化导致的 OOM（Out Of Memory）。
    *   **多模态处理**：对于多模态输入（图像），通常将 Image Encoder 独立部署，将 Image Embedding 视作特殊的 PrefixKV 注入到 LLM 的输入序列中。

5.  **成本与性能优化**
    *   **Speculative Decoding**：利用小模型（如 7B）草稿，大模型（如 70B）验证。在 Token 生成阶段，若验证通过，则一次生成多个 Token，大幅提升生成速度。
    *   **量化**：激活值/权重使用 FP8/INT8，KV Cache 使用 INT8/FP8（需关注平滑量化 SmoothQuant 对 KV 精度的影响）。

---

## 常见考点
1.  **PagedAttention 中 Block 表的管理机制**：GPU 上的物理块表和 CPU 上的逻辑块表如何映射？Copy-on-Write 机制是如何实现 KV 共享的？
2.  **Continuous Batching 的调度开销**：如果 Scheduler 轮询频率过高，CPU 成为瓶颈如何解决？（如 C++ 实现 Scheduler、Batch 调度）
3.  **Long Context 的极限优化**：当 Context 超过单卡显存，甚至超过集群显存时（Ring Attention），KV 如何切分和通信？
4.  **多模态输入的 KV 处理**：多模态 Feature Token 数量巨大（如高分辨率图），如何避免其挤占 LLM 的 Text KV 空间？（答案：Feature 压缩/池化、独立的 LoRA 适配器处理）。
