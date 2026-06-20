---
id: misc-015
difficulty: L2
category: ai-basics
subcategory: 训练与微调
tags:
- IO
feynman:
  essence: 通过切分优化器状态、梯度和参数，打破显存墙，训练超大模型。
  analogy: 多人合伙买房，每人只出一份钱，共同拥有整套房子。
  first_principle: 如何在有限显存下训练参数量远超单卡容量的模型？
  key_points:
  - Stage 1切优化器，Stage 2切梯度
  - Stage 3切参数，支持最大模型
  - 通信代价随级别递增
  - 大模型首选ZeRO-3
follow_up:
- ZeRO-3的通信开销如何估算?
- Tensor Parallelism和ZeRO能否同时使用?
---

# ZeRO (Zero Redundancy Optimizer)的三级优化分别是什么?如何选择

- **ZeRO分布式训练优化:**

| 级别 | 切分对象 | 显存节省 | 通信量 |
|------|---------|---------|--------|
| ZeRO-1 | 优化器状态 | 4x | 与DP相同 |
| ZeRO-2 | + 梯度 | 8x | 略增 |
| ZeRO-3 | + 模型参数 | **~Nx** | **显著增加** |

- **ZeRO-3 (Add Parameter Partitioning):**
- 模型参数也切分,每张卡只存1/N
- 前向/反向时动态All-Gather收集参数
- 适合:**超大模型(>70B)或多卡训练**
- 代价:通信量约为ZeRO-2的1.5倍

- **选择建议:**
- 模型<7B:ZeRO-1或纯DP
- 模型7B-70B:ZeRO-2
- 模型>70B:ZeRO-3 + CPU Offload
