---
id: sarg-003
difficulty: L2
category: ai-agent
subcategory: RAG技术
images:
- svg_rag.svg
feynman:
  essence: 选择能精准捕捉语义且匹配场景需求的高质量向量化模型。
  analogy: 像选翻译，既要懂语言（中文），又要懂专业（领域）。
  first_principle: 如何将文本转化为能准确表达语义且高效的向量表示？
  key_points:
  - 优先考虑语言支持和MTEB排名
  - 权衡维度大小与存储/检索成本
  - 根据算力选择API或本地部署
  - 长文档场景注意Context Window长度
---

# 如何选择Embedding模型？

Embedding 模型决定了 RAG 检索的“天花板”，直接影响了语义匹配的准确度。

### 选择维度与细节

1.  **多语言与领域支持**
    *   **通用英文**：OpenAI `text-embedding-3-small/large`（性能强，维度可选）。
    *   **中文场景**：BAAI `bge-large-zh` 或 `bge-small-zh`（目前中文社区公认效果较好）。
    *   **多语言**：BAAI `bge-m3`（支持 100+ 种语言，且支持长文本）。

2.  **维度与性能权衡**
    *   **高维 (1024/1536)**：信息量大，精度高，但存储成本高、检索计算慢。如 `bge-large`, `OpenAI ada-002`。
    *   **低维 (384/512)**：速度快，存储省，适合海量数据或低延迟场景。如 `bge-small`。
    *   **Matryoshka (嵌套维度)**：OpenAI `text-embedding-3` 支持动态截断维度，无需重新训练即可在精度和速度间灵活切换。

3.  **检索类型**
    *   **Dense Retrieval (稠密检索)**：传统向量检索，适合语义匹配。
    *   **Sparse Retrieval (稀疏检索)**：如 BM25、Splade，适合精确关键词匹配（如人名、型号）。
    *   **混合检索**：最佳实践通常是 `Dense (向量) + Sparse (关键词)` 结合，互补长短。`bge-m3` 同时支持这两种能力。

4.  **上下文长度**
    *   传统模型通常限制在 **512 tokens**。超过长度的文本需切分，会导致上下文割裂。
    *   新一代模型如 `bge-m3` 或 `jina-embeddings-v2` 支持 **8192 tokens**，可以直接对长段落进行编码，保持语义完整性。

### 评估指标
参考 **MTEB (Massive Text Embedding Benchmark)** 排行榜，重点关注 **Retrieval** 类目的数据集表现，而非总榜（因为总榜包含分类、聚类等任务，不完全代表 RAG 检索能力）。

## 常见考点
1.  **微调过的 Embedding 模型比通用模型好在哪里？**
    在特定领域（如医疗、法律）的数据上微调后，模型能学会该领域的“行话”和语义距离，解决通用模型对专业术语理解偏差的问题。
2.  **向量归一化的作用是什么？**
    将向量模长变为 1，使得相似度计算简化为点积，且便于使用余弦相似度进行空间度量，消除文本长度对相似度分数的影响。
3.  **如何评估 Embedding 是否适合我的数据？**
    构造一个包含“Query-正文档-负文档”的小规模测试集，计算 Recall@k 或 MRR 指标进行实测。
