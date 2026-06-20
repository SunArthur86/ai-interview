---
id: ai-harness-s003
difficulty: L3
category: ai-harness
subcategory: 推理优化
images:
- svg_transformer.svg
feynman:
  essence: 通过拆分模型层、权重矩阵或数据序列，突破单卡显存限制。
  analogy: 大象装冰箱：把象切开分装(层并行)，或几个人一起抬(张量并行)，或多冰箱放不同象(数据并行)。
  first_principle: 如何将一个巨大的模型拆解，使其能分布式地运行在多个有限的硬件资源上？
  key_points:
  - TP切分层内权重，通信频繁适合单机内互联
  - PP切分层间堆叠，减少通信气泡适合跨机
  - DP处理不同数据配合ZeRO节省显存
  - SP和EP分别针对长序列和MoE架构优化
---

# 模型并行有哪些方案？

大模型超过单GPU显存时需要并行：

1. **张量并行**：
- 将每一层的权重矩阵按行/列切分到多GPU
- 每层需要All-Reduce通信
- 适合单机多卡（NVLink高速互联）

2. **流水线并行**：
- 将模型的不同层分到不同GPU
- 微批次处理（Micro-batching）减少气泡
- 适合跨机多卡

3. **数据并行**：
- 每个GPU有完整模型副本
- 处理不同batch
- ZeRO优化：将优化器状态/梯度/参数分片到不同GPU

4. **序列并行**：
- 将长序列切分到多GPU处理
- Ring Attention、DeepSpeed Ulysses

5. **专家并行**：
- MoE模型的专家分布到不同GPU
- All-to-All通信

Megatron-LM + DeepSpeed通常组合使用TP+PP+DP。

- **补充：通信开销与拓扑结构**
- **TP 通信**: 使用 All-Reduce，必须在层间完成，延迟敏感，极其依赖 NVLink 带宽（通常仅限单机内）。
- **PP 通信**: 点对点通信，仅需传递激活值，对带宽要求相对较低，适合跨机（以太网/InfiniBand）。
- **3D 并行**: 结合 DP(数据) + PP(层) + TP(模型切分)，用于训练千亿参数模型；推理中常用 TP + PP。

- **并行策略对比图**

```text
[张量并行 TP]       [流水线并行 PP]       [数据并行 DP]
Layer 1 (Part A)    GPU 0: Layer 1-10    GPU 0: Full Model
Layer 1 (Part B)    GPU 1: Layer 11-20   GPU 1: Full Model
    │  (All-Reduce)      │ (P2P Send)        │ (All-Reduce)
Layer 2 (Part A)    GPU 2: Layer 21-30   GPU 2: Full Model
Layer 2 (Part B)                        GPU 3: Full Model
```

## 常见考点
1. **推理时为什么首选 TP 而不是 PP？**
   - TP 的通信延迟被计算掩盖，且无需像 PP 那样处理 Pipeline Bubble（气泡），延迟更低，更适合在线推理。
2. **ZeRO-1/2/3 的区别是什么？**
   - ZeRO-1 切分优化器状态，ZeRO-2 切分梯度，ZeRO-3 切分模型参数。推理中主要参考 ZeRO-3 思想进行模型卸载。
3. **什么是 Ring Attention？**
   - 序列并行的一种，通过环形通信传递 KV Cache 块，使得每个 GPU 只计算部分 Attention，突破单卡显存限制。
