---
id: "ai-scen-006"
difficulty: "L2"
category: "ai-scenario"
subcategory: "RAG系统设计"
tags:
  - "混合检索"
  - "BM25"
  - "Dense检索"
  - "RRF融合"
  - "Rerank"
  - "Query路由"
images:
  - "svg_rag_pipeline.svg"
feynman:
  essence: "【场景分析】 纯向量检索擅长语义匹配但弱于精确关键词（产品名、错误码）；纯BM25擅长精确匹配但不懂同义改写"
  analogy: "RAG 就像开卷考试——先翻书找到相关段落（检索），再结合理解写出答案（生成），不靠死记硬背（模型参数），知识可随时更新。"
  key_points:
    - "【场景分析】 纯向量检索擅长语义匹配但弱于精确关键词（产品名、错误码）"
    - "【双路检索架构】 1. Sparse路径（BM25）： - Elasticsearch/OpenSearch全文本索引 - 分词器：IK中文分词 + 标准英文分词 - 优势：精确匹配、缩写、专有名词、"
    - "语义型查询 → Dense权重↑ - 混合型：动态调整权重 - 短查询（<3词）倾向BM25，长查询倾向Dense 【Rerank精排】 - 融合后Top-50 → Cross-encoder Rer"
first_principle:
  problem: "如果要解决这个问题，最本质的方法论是什么？先理解问题约束，再找最优路径。"
  axioms:
    - "模型本质是数学函数的参数优化——所有能力都来自数据和参数"
    - "质量 > 数量：数据质量决定模型上限，算法决定达到上限的效率"
  rebuild: "从 AI 系统出发：① 核心挑战是什么？② 现有方案如何解决？③ 有哪些 trade-off？④ 如果重新设计你会怎么做？"
follow_up:
  - "RRF的k参数如何调优？"
  - "如果向量库和ES数据不一致怎么办？"
  - "如何在不增加延迟的情况下提升混合检索效果？"
---

# 如何设计RAG系统的混合检索方案？结合BM25关键词检索和Dense向量检索的优势。

【场景分析】
纯向量检索擅长语义匹配但弱于精确关键词（产品名、错误码）；纯BM25擅长精确匹配但不懂同义改写。混合检索取两者之长。

【双路检索架构】
1. Sparse路径（BM25）：
   - Elasticsearch/OpenSearch全文本索引
   - 分词器：IK中文分词 + 标准英文分词
   - 优势：精确匹配、缩写、专有名词、错误码
   - 返回Top-50候选
2. Dense路径（向量）：
   - Embedding模型 → Milvus/Qdrant HNSW检索
   - 优势：语义相似、同义词、跨语言
   - 返回Top-50候选
3. 融合策略：
   - RRF（Reciprocal Rank Fusion）：score = Σ 1/(k+rank_i)，k=60
   - 加权融合：α×BM25_score + (1-α)×Dense_score
   - 线性插值需要先归一化两路分数（min-max或softmax）

【Query路由优化】
- 意图分类：关键词型查询 → BM25权重↑；语义型查询 → Dense权重↑
- 混合型：动态调整权重
- 短查询（<3词）倾向BM25，长查询倾向Dense

【Rerank精排】
- 融合后Top-50 → Cross-encoder Reranker精排
- 模型：bge-reranker-v2-m3 / Cohere Rerank
- 输出Top-5给LLM生成
- Rerank提升MRR通常20%~40%

【评测对比】
| 策略 | Recall@10 | MRR | 延迟 |
|------|-----------|-----|------|
| 纯BM25 | 62% | 0.45 | 5ms |
| 纯Dense | 71% | 0.52 | 12ms |
| 混合+Rerank | 85% | 0.68 | 35ms |
