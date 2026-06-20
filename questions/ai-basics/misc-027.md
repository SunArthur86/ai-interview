---
id: "misc-027"
difficulty: "L2"
category: "ai-basics"
subcategory: "RAG与向量检索"
tags:
  - "IO"
  - "GC"
feynman:
  essence: "- *为什么需要混合检索:** - **BM25(关键词检索):** 擅长精确匹配(产品名、人名、术语),但不理解语义 - **向量检索(语义检索):** 擅长"
  analogy: "RAG 就像开卷考试——先翻书找到相关段落（检索），再结合理解写出答案（生成），不靠死记硬背（模型参数），知识可随时更新。"
  key_points:
    - "BM25(关键词检索): 擅长精确匹配(产品名、人名、术语),但不理解语义"
    - "向量检索(语义检索): 擅长语义相似,但精确匹配弱"
    - "混合 = 两者优势互补"
first_principle:
  problem: "为什么需要 混合检索(Hybrid Search)?BM25和向量检索如何融合？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "RRF为什么比加权平均更常用?"
  - "如何确定alpha参数?"
---

# 什么是混合检索(Hybrid Search)?BM25和向量检索如何融合

- **为什么需要混合检索:**

- **BM25(关键词检索):** 擅长精确匹配(产品名、人名、术语),但不理解语义
- **向量检索(语义检索):** 擅长语义相似,但精确匹配弱
- **混合 = 两者优势互补**

- **融合方法:**

1. **RRF (Reciprocal Rank Fusion):**
score = sum(1 / (k + rank_i))
- k通常取60
- 简单有效,不需要分数归一化
- **最常用**

2. **加权平均:**
score = alpha * norm(bm25_score) + (1-alpha) * norm(vector_score)
- 需要将两种分数归一化到[0,1]
- alpha通常0.5-0.7

- **实践:**
- Weaviate/Qdrant原生支持混合检索
- LangChain的EnsembleRetriever封装了RRF
