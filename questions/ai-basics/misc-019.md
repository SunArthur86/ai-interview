---
id: misc-019
difficulty: L2
category: ai-basics
subcategory: 推理优化
tags:
- Elasticsearch
feynman:
  essence: 通过降低精度压缩模型体积，AWQ/GPTQ在保持性能的同时显著降低显存。
  analogy: 把高清图片压缩成普通画质，但重点区域保持清晰，人眼看不出来。
  first_principle: 如何在大幅降低模型显存占用的同时，保持模型推理精度不下降？
  key_points:
  - AWQ基于激活值保护重要权重
  - GPTQ利用Hessian信息量化
  - QLoRA适合量化训练场景
  - INT4量化是推理主流
follow_up:
- INT4量化对推理速度有多大提升?
- 量化后的模型如何恢复精度损失?
---

# 模型量化的主要方法有哪些?GPTQ和AWQ的区别是什么

- **量化方法对比:**

| 方法 | 类型 | 精度损失 | 适用 |
|------|------|---------|------|
| RTN | 简单舍入 | 大 | 基线 |
| GPTQ | 后训练量化 | 小 | 通用 |
| AWQ | 激活感知 | **极小** | 通用 |
| QLoRA(NF4) | 量化+微调 | **极小** | 训练 |

- **GPTQ:** 逐层量化,用Hessian矩阵信息指导量化

- **AWQ:** 核心发现:不是所有权重同等重要,激活值大的通道更重要.保护重要通道(缩放),非重要通道激进量化.**不需要反向传播**,比GPTQ更快.INT4量化下精度损失最小.

- **实际应用:** vLLM默认支持AWQ,大部分开源模型提供GPTQ/AWQ量化版本
