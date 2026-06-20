---
id: misc-028
difficulty: L2
category: ai-basics
subcategory: RAG与向量检索
feynman:
  essence: 先粗筛再精排，用计算成本换取精度。
  analogy: 先在图书馆电脑搜到一批书（向量检索），再把书拿在手里细读目录决定要哪几本（Reranker）。
  first_principle: 如何在有限的计算资源下，从海量数据中找到最相关的极少数信息？
  key_points:
  - Bi-Encoder快但精度低，用于海量召回
  - Cross-Encoder精度高但慢，用于少量精排
  - 经典架构：召回Top50 -> 重排Top10
follow_up:
- Cross-Encoder为什么精度更高?
- 如何训练自定义Reranker?
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
