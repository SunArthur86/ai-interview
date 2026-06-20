---
id: misc-018
difficulty: L2
category: ai-basics
subcategory: 训练与微调
feynman:
  essence: CPT注入内化知识，RAG外挂实时信息，两者结合效果最优。
  analogy: CPT是把书背在脑子里，RAG是考试时开卷查书。
  first_principle: 如何让模型既具备深度的领域知识，又能实时获取最新信息？
  key_points:
  - CPT成本高但知识内化深
  - RAG成本低且知识实时更新
  - Prompt成本低但知识深度浅
  - 推荐CPT+RAG组合拳
follow_up:
- CPT和SFT的学习率如何设定?
- 如何评估领域适配效果?
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
