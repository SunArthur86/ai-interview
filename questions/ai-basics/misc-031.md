---
id: "misc-031"
difficulty: "L2"
category: "ai-basics"
subcategory: "RAG与向量检索"
tags:
  - "IO"
  - "IOC"
  - "索引"
  - "Elasticsearch"
feynman:
  essence: "- *RAG评估维度:** - *检索质量(Retrieval):** - **Context Precision** - 检索到的文档中有多少是相关的 - *"
  analogy: "RAG 就像开卷考试——先翻书找到相关段落（检索），再结合理解写出答案（生成），不靠死记硬背（模型参数），知识可随时更新。"
  key_points:
    - "检索质量(Retrieval):"
    - "Context Precision - 检索到的文档中有多少是相关的"
    - "Context Recall - 所有相关文档中有多少被检索到"
first_principle:
  problem: "如果要解决这个问题，最本质的方法论是什么？先理解问题约束，再找最优路径。"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "如何减少RAG的幻觉?"
  - "Faithfulness如何自动计算?"
---

# 如何评估RAG系统的质量?Ragas框架的核心指标有哪些

- **RAG评估维度:**

- **检索质量(Retrieval):**
- **Context Precision** - 检索到的文档中有多少是相关的
- **Context Recall** - 所有相关文档中有多少被检索到

- **生成质量(Generation):**
- **Faithfulness** - 答案是否忠于检索到的文档(无幻觉)
- **Answer Relevancy** - 答案是否回应了用户问题

- **Ragas框架:**
- 开源RAG评估工具
- 无需人工标注,用LLM自动评估
- 支持 grounding(忠实度) / relevance(相关性) / recall(召回)

- **其他评估工具:** TruLens、LlamaIndex Evaluation、LangSmith
