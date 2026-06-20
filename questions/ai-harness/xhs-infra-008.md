---
id: xhs-infra-008
difficulty: L4
category: ai-harness
subcategory: 推理与部署
tags:
- 系统设计
- Serving
- 推荐系统
- LLM
- 小红书
feynman:
  essence: 分级调度与弹性异构资源组合，平衡高并发与成本。
  analogy: 像餐厅运营，大厨（大模型）做难菜，帮厨（小模型）做快餐，合理排队。
  first_principle: 如何在保证低延迟和高吞吐的前提下，最小化推理服务成本？
  key_points:
  - 动态批处理（Continuous Batching）提升吞吐
  - 请求路由实现大小模型分级处理
  - 会话亲和性复用KV Cache降低延迟
  - 利用混合异构GPU和Spot实例降低成本
follow_up:
- 模型路由器如何决策用大模型还是小模型？
- KV Cache在多轮对话中如何管理？
- 推荐场景的冷启动如何用LLM优化？
---

# 设计一个支持百万QPS的大模型Serving系统（结合推荐场景）。如何做负载均衡和成本优化？

## 整体架构设计

```text
Client
  |
  v
+-----------------------+
|   API Gateway (L7)    | <--- 鉴权/限流/路由
+-----------+-----------+
            |
+-----------v-----------+    +-----------------------+
|   Request Router      |--->|  Load Balancer (L4)   |
| (Model/Session Logic) |    +-----------------------+
+-----------+-----------+              |
            |           +--------------v--------------+
            +----------->|   GPU Inference Cluster   |
                        | +------+   +------+   +----+|
                        | |vLLM  |   |TGI   |   |TRT-LLM||
                        | |(Paged|   |(Flash|   |(Tensor||
                        | |Attn)|   |Attn)|   |Core) ||
                        | +------+   +------+   +----+|
                        +------------------------------+
                        | KV Cache (GPU/CPUDisagg)    |
                        +------------------------------+
```

## 核心组件优化

### 1. 负载均衡与路由
- **L7 负载均衡**：
  - 基于请求内容路由：长文本 → 高显存节点；短文本 → 高吞吐节点。
  - 基于用户画像路由：VIP 用户优先独占或路由至低延迟节点。
- **会话亲和**：
  - 确保同一用户的连续请求（尤其是多轮对话）尽可能落在同一节点，直接命中 KV Cache，避免重新 Prefill。
  - 若节点负载过高，支持 KV Cache 的迁移或重建（Copy-on-write 机制）。

### 2. 批处理与调度策略
- **Continuous Batching (vLLM/Orca)**：
  - 动态识别已完成的序列，立即插入新序列，剔除静态 Padding 的浪费。
- **迭代级调度**：
  - 不等到 Batch 中所有句子生成结束才处理下一波，而是每次迭代只处理当前未完成的 Token。
- **Prefill vs Decode 分离**：
  - 预填充阶段是 Compute Bound，解码阶段是 Memory Bound。
  - **分离架构**：将计算密集的 Prefill 卸载到专用 Compute 节点，Decode 留在 Memory 节点，最大化整体吞吐。

### 3. 成本优化
- **异构 GPU 池**：
  - A100/H100：用于 70B+ 模型或低延迟要求。
  - L40S/T4：用于 7B/13B 模型或离线生成任务。
  - **弹性伸缩**：利用 Spot 实例处理离线任务（如索引更新、Embedding 生成），降低 50%+ 成本。
- **Speculative Decoding (投机采样)**：
  - 使用小模型（如 70B 参数用 7B 做辅助）提前生成 N 个 Token，大模型并行验证。验证成功即输出，失败则回滚。
  - 加速比通常在 1.5x - 2.5x，显存几乎不增加。
- **前缀缓存**：
  - 系统提示词 或通用 Prompt 段只计算一次 KV Cache，所有请求共享。

### 4. 推荐场景特化
- **Refined Pipeline**：
  - **Rank 阶段**：传统双塔模型，CPU/GPU 快速召回。
  - **Rerank 阶段**：LLM 重排 Top-K 候选集（利用 LLM 的语义理解能力）。
- **Batch Rerank**：
  - 将多个 Item 拼接成一个 Prompt 送入 LLM，一次性重排，减少推理次数。
  - 示例：`User: x; Items: [A, B, C]; Output: Ranked List`.
- **冷启动解决**：利用 LLM 生成 Item 的 Embedding 或描述文本，补全冷启动 Item 的特征。

## 监控指标
- **系统指标**：QPS, P99/P95 Latency (TTFT - Time To First Token, TPOT - Time Per Output Token), GPU Utilization.
- **效率指标**：
  - **KV Cache Hit Rate**：直接反映会话复用效果。
  - **Preemption Rate**：Spot 实例的中断率。
  - **Decode/Prefill Ratio**：衡量请求长尾分布。
- **成本指标**：Cost per 1k Requests, Cost per Token。

## 常见考点
1. **PagedAttention 的核心思想**：借鉴操作系统的虚拟内存，将 KV Cache 切分为固定大小的 Blocks，存储在非连续显存中，解决显存碎片化问题，极大提升 Batch Size 上限。
2. **Continuous Batching vs Static Batching**： Static Batching 必须等 Batch 中最长的序列生成完才能释放资源，Continuous Batching 可以动态进出，为何对高并发场景至关重要？
3. **TTFT (Time To First Token) vs TPOT**：TTFT 受限于 Prefill 阶段速度和带宽（可优化），TPOT 受限于 Decode 阶段的显存带宽（瓶颈通常在此）。如何针对性优化？
4. **多模态（VLM）推理的挑战**：图像 Token 化后通常极长（如 256-576 tokens），导致 Prefill 时间极长，如何压缩图像特征或采用异步流式处理？
