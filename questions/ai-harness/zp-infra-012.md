---
id: zp-infra-012
difficulty: L3
category: ai-harness
subcategory: 工程化
tags:
- 智谱
- 面经
- AI Infra
- 求职准备
- 学习路线
feynman:
  essence: 掌握从Transformer架构到分布式训练落地的全栈优化技术。
  analogy: 像赛车队，既要懂引擎原理（Transformer），也要懂赛道调优（CUDA/Infra）。
  first_principle: 如何以最低的成本和延迟，最大化大模型的训练与推理效率？
  key_points:
  - 四大核心：架构、推理、训练、CUDA
  - 必读源码：vLLM、DeepSpeed、FlashAttention
  - 面试重点：项目量化、原理深究
  - 实战导向：不做理论派，重工程落地
follow_up:
- 没有 Infra 实习经验怎么办？ — — 自己复现 vLLM/DeepSpeed 实验，做 benchmark 对比
- CUDA 编程零基础怎么入门？ — — NVIDIA 官方教程 + 简单 GEMM/softmax kernel 练习
- Infra 和算法岗的区别？ — — Infra 重工程/系统/性能优化，算法重模型/训练/数据
---

# 【智谱面经】大模型 Infra 岗位怎么准备？必看资料有哪些？面试考察重点是什么？

**大模型 AI Infra 岗位准备全攻略（增强版）：**

**一、核心知识树（4 大模块）**

1.  **Transformer 架构原理**
    *   **Attention 机制**：Self-Attention 的复杂度 $O(N^2)$，Multi-Head Attention 的并行性。
    *   **变体**：GQA（Grouped Query Attention，减少 KV Head 数量），MLA（Multi-Head Latent Attention，DeepSeek V2 核心，极度压缩 KV）。
    *   **位置编码**：RoPE（旋转位置编码）的原理（复数域旋转）、外推性（YaRN/NTK-aware）。
    *   **MoE**：Sparse MoE 的路由机制、负载均衡损失。

2.  **推理优化（高频考点）**
    *   **KV Cache**：原理、显存占用计算公式 ($2 \times 2 \times n_{layers} \times d_{model} \times n_{heads} \times seq\_len$)。
    *   **PagedAttention**：解决显存碎片化的核心，类比 OS 的虚拟内存分页。
    *   **量化**：
        *   W8A8 / W4A16 / W4A4 的区别。
        *   GPTQ（基于 Hessian 矩阵重要性），AWQ（基于 Activation 的权重量化），SmoothQuant（平滑激活值与权重）。
    *   **投机解码**：Draft Model + Verify Model 的流程，分析树状注意力验证的加速比。

3.  **训练优化**
    *   **并行策略**：
        *   DP（数据并行）：简单，通信量大（AllReduce）。
        *   TP（张量并行）：层内切分，通信频率高（AllReduce），适合单机多卡。
        *   PP（流水线并行）：层间切分，存在 Bubble（气泡），Micro-batch 调度（1F1B）。
        *   EP（专家并行）：MoE 专用，All-to-All 通信。
    *   **ZeRO**：Stage 1 (Optimizer sharding), Stage 2 (Gradient sharding), Stage 3 (Parameter sharding)。
    *   **混合精度**：FP16/BF16 的梯度溢出问题，Loss Scaling。

4.  **CUDA / Kernel**
    *   **硬件模型**：SM（Streaming Multiprocessor），Warp（32线程），Bank Conflict，Memory Coalescing。
    *   **优化技巧**：Shared Memory 利用，Tiling（分块计算），流水线掩盖延迟。
    *   **FlashAttention**：Tiling 技术（将 softmax 分块计算，避免读取全量 $N^2$ 矩阵），IO-aware。

**二、必看资料（🔺 高优先级）**

**论文：**
- *必读*："Attention Is All You Need", "FlashAttention" v2/v3, "PagedAttention" (vLLM paper), "Llama 2/3".
- *进阶*："DeepSeek-V2" (MoE + MLA), "Mixture of Experts".
- *训练*："ZeRO: Memory Optimizations", "Megatron-LM".

**开源项目（读源码）：**
- **vLLM**：重点看 `block_manager.py`, `scheduler.py`, `paged_attn_kernel`.
- **FlashAttention**：重点看 `flash_attn_kernel` 的 Tiling 逻辑.
- **DeepSpeed**：重点看 ZeRO-3 的 parameter gathering 逻辑.

**工具/教程：**
- NVIDIA "Optimizing CUDA Kernels" 系列视频.
- HuggingFace "Transformers" 源码解读（Model 生成流程）.

**三、面试考察重点**

| 维度 | 占比 | 说明 |
|------|------|------|
| **项目深挖** | 40% | STAR 结构 + 量化成果（MFU 提升多少、推理加速多少倍、显存优化幅度）|
| **原理追问** | 30% | 量化原理、KV Cache 预分配策略、Attention 的 CUDA Kernel 实现 |
| **系统设计** | 15% | 设计百万 QPS Serving / 万卡训练集群 / KV Cache 存储体系 |
| **手撕代码** | 10% | 手写 Attention Matrix（PyTorch）、简单的 CUDA Kernel 或 C++ Multi-threading |
| **行为/文化** | 5% | 技术热情、对前沿进展的追踪 |

**四、准备时间线（6-8 周）**

```text
Week 1-2: 基础夯实（Transformer 数学推导 + RoPE + MoE 基础）
Week 3-4: 论文精读（FlashAttention v2/v3 + vLLM 架构 + ZeRO 原理）
Week 5-6: 源码实践（跑通 vLLM 二次开发 + 手写 FlashAttn 核心代码片段）
Week 7-8: 场景设计 + 模拟面试（高并发推理场景、万卡训练容灾设计）
```

**五、简历建议**
- **技术栈关键词**：vLLM, PagedAttention, FlashAttention, ZeRO-3, MPI, NCCL, TensorRT-LLM, CUDA Core.
- **量化数据**："推理吞吐 2k tps -> 8k tps (4x)", "显存占用降低 40% (AWQ+KV Cache Quantization)".
- **难点解决**：描述遇到的最难的 Bug 或性能瓶颈（如：NCCL Hang, OOM 排查）.

---

## 常见考点
1.  **RoPE 的数学原理**：如何通过复数乘法实现相对位置编码？外推时 NTK-alpha 参数的作用机制是什么？
2.  **FlashAttention v1/v2/v3 的区别**：v2 引入了什么并行策略（Warp-level 并行）？v3 针对 Hopper 架构做了哪些优化（Tensor Memory Accelerator, TMA）？
3.  **vLLM 的调度器死锁情况**：在什么情况下 Continuous Batching 会导致无法调度新请求（长尾效应，所有 GPU 都被几个长 Context 占满，剩余 Block 小于任何新请求的 Prefill 需求）？如何解决？（答案：Prefill 阶段的 Block 分片或抢占机制）。
4.  **MoE 的 All-to-All 通信瓶颈**：在专家并行中，Token 分发和收集的通信量如何计算？如何通过专家容量冗余减少通信冲突？
