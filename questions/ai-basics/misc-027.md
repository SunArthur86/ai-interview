---
id: misc-027
difficulty: L2
category: ai-basics
subcategory: RAG与向量检索
tags:
- IO
- GC
feynman:
  essence: 结合关键词的精确匹配和向量检索的语义理解。
  analogy: 像查字典，既看目录索引（关键词）又看内容理解（语义），两头都不误。
  first_principle: 如何同时满足精确查找（如人名）和模糊理解（如同义词）的检索需求？
  key_points:
  - BM25精准匹配专有名词，弱在语义
  - 向量检索擅长模糊匹配，弱在精确字符
  - RRF是混合排序的主流算法
follow_up:
- RRF为什么比加权平均更常用?
- 如何确定alpha参数?
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
