---
id: "misc-048"
difficulty: "L2"
category: "ai-basics"
subcategory: "RAG与向量检索"
tags:
  - "IOC"
images:
  - "svg_embedding_training.svg"
feynman:
  essence: "Embedding 模型选型看维度、语言、最大 token、MTEB 榜单成绩：BGE（智源，中英文强，bge-large-zh/bge-m3 多语言）、E5（微软，多任务通用）、Cohere（英文强、商用 API）、OpenAI text-embedding-3；中文场景推荐 BGE-large-zh-v1.5 或 BGE-M3（支持稠密+稀疏+多向量）。"
  analogy: "Embedding 就像把词语放到语义地图上——意思相近的词距离近，无关的词距离远，让机器能计算「相似度」。"
  key_points:
    - "主流Embedding模型:"
    - "中文优先: BGE-large-zh-v1.5 或 BGE-M3"
    - "多语言: BGE-M3 或 Cohere"
first_principle:
  problem: "如果要解决这个问题，最本质的方法论是什么？先理解问题约束，再找最优路径。"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "BGE-M3的「三多」是什么意思?"
  - "Matryoshka Embedding如何实现维度可变?"
---

# 如何选择Embedding模型?BGE、E5、Cohere各有什么特点?中文场景推荐什么

- **主流Embedding模型:**

| 模型 | 类型 | 维度 | 中文支持 | 特点 |
|------|------|------|---------|------|
| BGE-M3 | 开源 | 1024 | **优秀** | 多语言/多功能/多粒度 |
| BGE-large-zh | 开源 | 1024 | **优秀** | 中文专项优化 |
| E5-mistral | 开源 | 4096 | 好 | 强通用 |
| GTE | 开源 | 768/1024 | 好 | 阿里达摩院 |
| text-embedding-3 | API | 1536/3072 | 好 | OpenAI |
| Cohere embed v3 | API | 1024 | 好 | 多语言 |

- **选择建议:**

1. **中文优先:** BGE-large-zh-v1.5 或 BGE-M3
2. **多语言:** BGE-M3 或 Cohere
3. **英文/通用:** text-embedding-3-large 或 E5
4. **预算充足:** OpenAI/Cohere API
5. **本地部署:** BGE系列(通过sentence-transformers加载)

- **评估指标:** MTEB Leaderboard(覆盖56个任务的embedding评测)
