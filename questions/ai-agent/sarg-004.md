---
id: sarg-004
difficulty: L2
category: ai-agent
subcategory: RAG技术
images:
- svg_rag.svg
feynman:
  essence: 用精排模型对粗排结果进行二次筛选，提升准确率。
  analogy: 就像先用筛子快速筛沙，再人工挑出金子。
  first_principle: 如何在保证检索召回率的同时最大化结果的相关性？
  key_points:
  - 补全向量检索的信息损失
  - 牺牲速度换取精度
  - 流程：粗排召回 → 精排截断
---

# 什么是Reranking？为什么RAG需要它？

Reranking（重排序）是对初步检索结果用更精确的模型重新排序。

**为什么需要：**
1. 向量检索速度快但精度有限（embedding是压缩表示，有信息损失）
2. 召回阶段取Top-50/100（高召回率），Rerank阶段精排到Top-5/10（高精确率）
3. Cross-Encoder模型比Bi-Encoder更准确

**Bi-Encoder vs Cross-Encoder：**
- **Bi-Encoder（Embedding）**：query和doc分别编码，计算余弦相似度。速度快但精度有限。
- **Cross-Encoder（Reranker）**：query和doc拼接后一起输入模型，输出相关性分数。精度高但速度慢。

**常用Reranker：**
- BAAI/bge-reranker-v2-m3（多语言）
- Cohere Rerank API
- bce-reranker-base_v1

**流程：** 向量检索Top-100 → Rerank到Top-5 → 拼入Prompt
