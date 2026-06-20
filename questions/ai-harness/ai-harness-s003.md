---
id: "ai-harness-s003"
difficulty: "L3"
category: "ai-harness"
subcategory: "推理优化"
images:
  - "svg_transformer.svg"
feynman:
  essence: "大模型超过单GPU显存时需要并行： 1. 张量并行（Tensor Parallelism, TP）： - 将每一层的权重矩阵按行/列切分到多GPU - 每层需要"
  analogy: "Harness Engineering 就像给 AI 搭建完整的施工脚手架——不只是调 LLM API，而是构建提示词管理、工具编排、错误处理、监控的完整工程框架。"
  key_points:
    - "张量并行（Tensor Parallelism, TP）："
    - "将每一层的权重矩阵按行/列切分到多GPU"
    - "每层需要All-Reduce通信"
first_principle:
  problem: "为什么需要 模型并行有哪些方案？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Harness Engineering 的核心是工程化——把 LLM 的潜力通过系统设计转化为可靠的生产力"
    - "评测驱动开发——没有 Golden Set 和持续评测，AI 系统就是黑盒"
    - "LLM 应用的可靠性 = 提示工程 + 错误处理 + 降级策略 + 可观测性"
  rebuild: "从工程化出发：① 为什么 LLM 应用需要 Harness？② 可观测性的核心指标？③ 如何做评测和回归？④ 理想的 AI 工程平台是什么样？"
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
