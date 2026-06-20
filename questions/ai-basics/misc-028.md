---
id: "misc-028"
difficulty: "L2"
category: "ai-basics"
subcategory: "RAG与向量检索"
feynman:
  essence: "- *Reranker的作用:** 向量检索返回Top-K候选后,用Reranker精排,提升最终结果质量. - *Bi-Encoder vs Cross-En"
  analogy: "RAG 就像开卷考试——先翻书找到相关段落（检索），再结合理解写出答案（生成），不靠死记硬背（模型参数），知识可随时更新。"
  key_points:
    - "Reranker的作用:"
    - "Bi-Encoder vs Cross-Encoder:"
    - "Bi-Encoder召回Top-50(快)"
first_principle:
  problem: "它们本质上为什么不同？各自的设计目标和适用场景是什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "Cross-Encoder为什么精度更高?"
  - "如何训练自定义Reranker?"
---

# RAG中为什么需要Reranker?Cross-Encoder和Bi-Encoder有什么区别

- **Reranker的作用:**
向量检索返回Top-K候选后,用Reranker精排,提升最终结果质量.

- **Bi-Encoder vs Cross-Encoder:**

| | Bi-Encoder | Cross-Encoder |
|--|-----------|---------------|
| 原理 | 分别编码Q和D,算余弦相似 | Q和D拼接后一起编码 |
| 速度 | **快**(可预计算) | 慢(每对都要推理) |
| 精度 | 中 | **高** |
| 角色 | **召回**(第一阶段) | **重排**(第二阶段) |

- **两阶段检索流程:**
1. Bi-Encoder召回Top-50(快)
2. Cross-Encoder重排选Top-5(准)

- **主流Reranker:**
- Cohere Rerank(API)
- BGE-Reranker(开源)
- Jina Reranker(开源)
