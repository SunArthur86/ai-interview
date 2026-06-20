---
id: misc-005
difficulty: L2
category: ai-basics
subcategory: 大模型原理
tags:
- IO
feynman:
  essence: 通过多头共享K/V矩阵,大幅缩减显存占用并提升推理速度。
  analogy: 多个人(Q)共用同一套参考书(K/V),不用每人买一套,省钱又省地方。
  first_principle: 如何在保持注意力表达能力的前提下,极大压缩KV Cache显存?
  key_points:
  - MHA:独立KV,质量好但慢
  - MQA:所有头共用一个KV,极快但伤质量
  - GQA:分组共享,兼顾速度与质量
follow_up:
- GQA的分组数如何选择?
- MQA在什么场景下值得质量折中?
---

# MHA、MQA、GQA三者有什么区别?为什么大模型倾向用GQA

三者是Key/Value在不同head间的共享策略:

| 方案 | K/V头数 | KV Cache | 质量 | 速度 |
|------|---------|----------|------|------|
| MHA | = Q头数 | 大 | 最好 | 慢 |
| MQA | 1 | **最小** | 下降 | **最快** |
| GQA | 分组共享 | 中等 | **接近MHA** | **快** |

- **核心权衡:** K/V头越少→KV Cache越小→推理越快,但质量可能下降

- **GQA (Grouped Query Attention):**
- 将Q头分为G组,每组共享一对K/V
- 例如32个Q头分为8组,每组4个Q头共享K/V
- KV Cache减少为MHA的1/4

- **实际应用:**
- LLaMA-2 70B: GQA (8组)
- LLaMA-3: GQA
- Mistral: GQA
- GLM-4: GQA
