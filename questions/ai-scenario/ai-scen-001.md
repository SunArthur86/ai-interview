---
id: ai-scen-001
difficulty: L3
category: ai-scenario
subcategory: RAG系统设计
tags:
- RAG
- 向量检索
- 混合检索
- Embedding
- 知识库
- 企业搜索
feynman:
  essence: 混合检索+重排序精准召回，结合权限控制生成可信答案。
  analogy: 像超级图书管理员，既能精准查书（混合检索），又能防止小朋友看禁区（权限控制）。
  first_principle: 如何从海量非结构化数据中快速、准确地提取相关信息并生成回答？
  key_points:
  - 文档摄入：解析、分块、元数据
  - 混合检索：向量+BM25，优势互补
  - Rerank精排：Cross-encoder提升Top-K质量
  - 安全合规：权限过滤与审计日志
follow_up:
- 如何处理文档更新后向量索引的增量更新？
- 如何评估RAG系统端到端的质量？
- 当检索结果不相关时，系统应该如何兜底？
---

# 如何设计一个企业级 RAG 知识库系统？要求支持百万级文档、秒级检索、高准确率回答。

【场景分析】
企业RAG核心需求：海量文档向量化存储、语义检索+关键词混合、LLM生成带引用的回答、权限隔离与审计。

【整体架构】
1. 文档摄入层：
   - 文档解析（PDF/Word/HTML/邮件）→ Unstructured/markdownify
   - 智能分块（Chunking）：语义分块 > 固定窗口，保留标题层级
   - 元数据标注（部门、权限、时间、来源）
2. 索引层：
   - Embedding模型（BGE-large / OpenAI text-embedding-3）
   - 向量库（Milvus/Qdrant/Pinecone），支持HNSW索引
   - 关键词索引（Elasticsearch BM25），实现混合检索
3. 检索层：
   - Query改写：同义扩展、HyDE（假设性文档生成）
   - 混合检索：Dense（向量）+ Sparse（BM25），RRF融合
   - 重排序（Reranker）：Cross-encoder（Cohere/bge-reranker）精排Top-5
4. 生成层：
   - 上下文组装：Top-K chunks + 系统Prompt + 用户问题
   - LLM生成：附引用来源标注
   - 幻觉检测：与检索chunk交叉验证
5. 安全层：
   - 文档级权限过滤（检索前/检索后双重过滤）
   - PII脱敏 + 审计日志

【核心流程】
用户提问 → Query改写 → 混合检索 → Rerank → 权限过滤 → 组装Prompt → LLM生成 → 引用标注 → 返回

【性能优化】
- 异步索引更新：文档变更走消息队列，避免阻塞检索
- 缓存：热门Query结果缓存（语义缓存，相似度>0.95命中）
- 预计算：文档摘要预生成，减少实时Token消耗
- 量化：向量量化（PQ/SQ）降低内存占用

【评测指标】
- 检索：Recall@K、MRR、NDCG
- 生成：Faithfulness（忠实度）、Answer Relevancy（相关性）、引用准确率
