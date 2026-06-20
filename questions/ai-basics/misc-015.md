---
id: "misc-015"
difficulty: "L2"
category: "ai-basics"
subcategory: "训练与微调"
tags:
  - "IO"
feynman:
  essence: "ZeRO-3 (Add Parameter Partitioning)。"
  analogy: "分布式系统就像连锁店——一家变多家，需要统一菜单（一致性）、协调库存（分布式事务）、处理网络问题。"
  key_points:
    - "ZeRO分布式训练优化:"
    - "ZeRO-3 (Add Parameter Partitioning):"
    - "模型参数也切分,每张卡只存1/N"
first_principle:
  problem: "从第一性原理看：ZeRO (Zero Redundancy Optimizer)的三级优化分别?如何选择 的根本优势/劣势来源于什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "ZeRO-3的通信开销如何估算?"
  - "Tensor Parallelism和ZeRO能否同时使用?"
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
