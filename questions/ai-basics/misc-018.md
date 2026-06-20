---
id: "misc-018"
difficulty: "L2"
category: "ai-basics"
subcategory: "训练与微调"
feynman:
  essence: "CPT注入领域知识 -> SFT调整格式 -> RAG补充实时信息。"
  analogy: "RAG 就像开卷考试——先翻书找到相关段落（检索），再结合理解写出答案（生成），不靠死记硬背（模型参数），知识可随时更新。"
  key_points:
    - "CPT注入领域知识 -> SFT调整格式 -> RAG补充实时信息"
    - "例如:医疗大模型 = 医学文献CPT + 医患对话SFT + 医学知识库RAG"
first_principle:
  problem: "为什么需要 领域模型适配的三大范式(CPT vs RAG vs Prompt)如何选择？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "CPT和SFT的学习率如何设定?"
  - "如何评估领域适配效果?"
---

# 领域模型适配的三大范式(CPT vs RAG vs Prompt)如何选择

- **三种适配范式对比:**

| 维度 | 继续预训练(CPT) | RAG | Prompt Engineering |
|------|----------------|-----|--------------------|
| 知识更新 | 慢(需重训) | **实时** | 实时 |
| 成本 | 高(GPU训练) | **低** | **极低** |
| 知识深度 | **深** | 中 | 浅 |
| 幻觉风险 | 中 | **低** | 高 |

- **最佳实践:组合使用**
1. CPT注入领域知识 -> SFT调整格式 -> RAG补充实时信息
2. 例如:医疗大模型 = 医学文献CPT + 医患对话SFT + 医学知识库RAG
