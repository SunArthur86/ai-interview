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

1. 张量并行（Tensor Parallelism, TP）：
- 将每一层的权重矩阵按行/列切分到多GPU
- 每层需要All-Reduce通信
- 适合单机多卡（NVLink高速互联）

2. 流水线并行（Pipeline Parallelism, PP）：
- 将模型的不同层分到不同GPU
- 微批次处理（Micro-batching）减少气泡
- 适合跨机多卡

3. 数据并行（Data Parallelism, DP）：
- 每个GPU有完整模型副本
- 处理不同batch
- ZeRO优化：将优化器状态/梯度/参数分片到不同GPU

4. 序列并行（Sequence Parallelism, SP）：
- 将长序列切分到多GPU处理
- Ring Attention、DeepSpeed Ulysses

5. 专家并行（Expert Parallelism, EP）：
- MoE模型的专家分布到不同GPU
- All-to-All通信

Megatron-LM + DeepSpeed通常组合使用TP+PP+DP。
