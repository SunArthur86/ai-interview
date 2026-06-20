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

**企业级 RAG 知识库系统设计（增强版）：**

【场景分析】
企业 RAG 核心需求：海量文档向量化存储、语义检索 + 关键词混合、LLM 生成带引用的回答、权限隔离与审计。

**整体架构（数据流向图）：**

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                           Data Source (S3/DB)                             │
└──────────────────────────────┬───────────────────────────────────────────┘
                               │ (Ingestion Pipeline - Async)
                               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         Ingestion & Processing Layer                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                │
│  │ Parser       │───▶│ Chunking     │───▶│ Embedding    │                │
│  │ (Unstructured)│   │ (Semantic/   │    │ Model (BGE)  │                │
│  │              │   │  Recursive)  │    │ (GPU Batch)  │                │
│  └──────────────┘    └──────────────┘    └──────┬───────┘                │
│                                              │                         │
│                                              │ Vector + Metadata       │
│                                              ▼                         │
│  ┌──────────────────────────────────────────────────────┐             │
│  │             Vector Database (Milvus/Qdrant)           │             │
│  │  ┌────────────────────────────────────────────────┐  │             │
│  │  │ Index: HNSW / IVF_FLAT (Dense Vector)          │  │             │
│  │  │ Metadata: Filter Index (Tenant/Time/ACL)       │  │             │
│  │  └────────────────────────────────────────────────┘  │             │
│  └──────────────────────────────────────────────────────┘             │
└──────────────────────────────┬───────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         Retrieval & Augmentation Layer                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                │
│  │ Query        │───▶│ Hybrid       │───▶│ Reranker     │                │
│  │ Rewrite      │    │ Retrieval    │    │ (Cross-Enc)  │                │
│  │ (HyDE)       │    │ (Dense+Sparse)│   │ (Top-K)      │                │
│  └──────────────┘    └──────┬───────┘    └──────┬───────┘                │
│                             │                   │                         │
│                             ▼                   │                         │
│                    ┌────────────────┐          │                         │
│                    │ Elasticsearch  │          │                         │
│                    │ (BM25/Keyword) │          │                         │
│                    └────────────────┘          │                         │
│                             │                   │                         │
│                             └────────┬──────────┘                         │
│                                      ▼ (RRF Fusion + Rank)                │
│                          ┌──────────────────────┐                        │
│                          │  Security Filter     │                        │
│                          │  (Pre/Post ACL)      │                        │
│                          └──────────┬───────────┘                        │
└─────────────────────────────┬────────────────────────────────────────────┘
                              │ (Context + Prompt)
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                           Generation Layer                                │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                │
│  │ Context      │───▶│ LLM Service  │───▶│ Answer       │                │
│  │ Assembler    │    │ (vLLM/LangChain)│   │ Post-process │                │
│  │ (Max Token   │    │              │    │ (Citation)   │                │
│  │  Truncation) │    │              │    │              │                │
│  └──────────────┘    └──────────────┘    └──────────────┘                │
└──────────────────────────────────────────────────────────────────────────┘
```

**核心流程与关键细节：**

1.  **文档摄入**
    *   **解析**：针对 PDF/Word/表格，使用 `Unstructured` 或专用 OCR 引擎。
    *   **分块**：避免简单的固定长度切分。推荐 **Recursive Character Split** 或 **Semantic Chunking**（基于 Embedding 相似度切分），确保语义完整。
    *   **元数据**：必须包含 `doc_id`, `tenant_id`, `department`, `create_time`, `access_level`。

2.  **索引层**
    *   **Embedding 模型**：BGE-large-zh (中文) / OpenAI text-embedding-3。支持 GPU 批量推理加速。
    *   **向量索引**：Milvus/Qdrant。推荐 **HNSW** (Hierarchical Navigable Small World) 索引，兼顾召回率与速度。参数 `M` (连接数) 和 `ef_construction` 需根据数据规模调优。
    *   **关键词索引**：Elasticsearch。BM25 用于处理精确匹配（如人名、型号、缩写），弥补语义向量对专有名词理解的不足。

3.  **检索层**
    *   **Query 改写**：
        *   **HyDE**：生成假设性回答向量，用回答向量检索，比问题向量更接近文档向量。
        *   **Query Decomposition**：复杂问题拆解为多个子问题。
    *   **混合检索**：Dense Retrieval (向量) + Sparse Retrieval (BM25)。
    *   **融合**：使用 **RRF (Reciprocal Rank Fusion)** 算法合并两个排序列表，公式 $score(d) = \sum_{q} \frac{1}{k+rank_q(d)}$。避免简单的加权平均带来的分值归一化难题。
    *   **重排序**：取出 Top-20/50，用 Cross-encoder (如 `bge-reranker-large`) 精排。重排模型计算量大，通常部署在 CPU 集群或单独的 GPU 服务上。

4.  **生成层**
    *   **上下文组装**：
        *   限制 Context Window (如 4k/8k tokens)。
        *   策略：优先保留 Rerank 后的高分 Chunk；如果用户提问强调时间，优先按时间元数据筛选。
    *   **Prompt 工程**：强制 LLM 输出引用来源 `[doc_id]`，如果不知道答案，明确回答 "不知道"，不要胡编。

5.  **安全层**
    *   **权限过滤**：
        *   **Pre-Retrieval Filter**：在检索前，通过 Vector DB 的 Metadata Filter 过滤掉用户无权访问的 `tenant_id`。这是最高效的。
        *   **Post-Retrieval Filter**：在 LLM 组装 Context 前，再次校验 Chunk 的 ACL。
    *   **PII 脱敏**：在 Ingestion 阶段或 Generation 阶段识别并掩盖敏感信息（手机号、身份证）。

**性能优化：**
*   **异步索引**：使用 Kafka/Pulsar 解耦文档上传与索引构建，避免阻塞用户上传接口。
*   **缓存**：
    *   **语义缓存**：对用户的 Query 做 Embedding，在 Redis 中缓存 Top-K 结果。相似度 > 0.95 直接返回，绕过检索与生成。
    *   **LLM 缓存**：对完全相同的 Prompt 缓存 LLM 的 Response。
*   **向量量化**：使用 PQ (Product Quantization) 将向量从 Float32 压缩到 Int8，牺牲极小精度换取显存/内存节省。

---

## 常见考点
1.  **混合检索的融合策略**：除了 RRF，还有哪些加权融合方式？如何处理向量检索和关键词检索分数量级不一致的问题？（答案：Min-Max 归一化、Sigmoid 归一化）。
2.  **RAG 幻觉问题**：如何检测 LLM 生成的答案与检索到的 Context 不一致？（答案：FactScore、引用验证模型、让 LLM 先生成再反向验证）。
3.  **向量数据库选型**：Milvus vs Pinecone vs PG-Vector 的优劣对比？在什么场景下 PG-Vector 足够？（答案：数据量小（<百万）、已有 PostgreSQL 基础设施时可用 PG-Vector；大规模高并发需专用向量库）。
4.  **召回率优化**：当检索结果不相关时，如何系统性排查？（答案：检查分块是否破坏语义、Embedding 模型是否适配领域知识、Query 改写是否准确、是否缺乏 BM25 纠错）。
