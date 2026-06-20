---
id: "misc-005"
difficulty: "L2"
category: "ai-basics"
subcategory: "大模型原理"
tags:
  - "IO"
feynman:
  essence: "MQA/GQA/MLA 都是 Key/Value 在不同 head 间的共享策略：MQA 所有 head 共享一组 KV（最快、质量略降），GQA 每 N 个 head 共享一组（折中），MLA 用低秩投影压缩 KV（DeepSeek 方案，质量高且省 KV Cache）。"
  analogy: "大语言模型就像读过整个互联网的学者——通过预测「下一个词」生成文本，积累了海量语言模式和知识。"
  key_points:
    - "核心权衡: K/V头越少→KV Cache越小→推理越快,但质量可能下降"
    - "GQA (Grouped Query Attention):"
    - "将Q头分为G组,每组共享一对K/V"
first_principle:
  problem: "它们本质上为什么不同？各自的设计目标和适用场景是什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "GQA的分组数如何选择?"
  - "MQA在什么场景下值得质量折中?"
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
