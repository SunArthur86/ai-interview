---
id: sarg-002
difficulty: L2
category: ai-agent
subcategory: RAG技术
images:
- svg_rag.svg
feynman:
  essence: 将长文档合理切分为语义完整的片段，以提升检索匹配度。
  analogy: 像切肉，顺着纹理切，肉片才完整且好找。
  first_principle: 如何在保留语义完整性的同时，最大化检索的匹配效率？
  key_points:
  - 固定长度简单但易切断语义
  - 递归分割和语义切分保持完整性
  - 父子索引兼顾检索精度和上下文
  - 设置Overlap防止边界信息丢失
---

# RAG的Chunking策略有哪些？

文本切片质量直接影响检索效果。

常见策略：

1. 固定长度：按字符数切分（如500字），简单但可能切断语义

2. 递归分割：先按段落(\n\n)，再按句子(\n)，最后按字符。保持语义完整性。LangChain默认。

3. 语义切分（Semantic Chunking）：用embedding计算相邻句子相似度，相似度低于阈值时切分。效果最好但计算量大。

4. 文档结构感知：根据文档结构（标题、章节、页码）切分。如Markdown按标题层级切分。

5. 父子分块（Parent-Child）：小块检索（精确匹配），大块返回（提供完整上下文）。

关键参数：
- chunk_size：块大小（200-1000 tokens）
- chunk_overlap：重叠区域（10-20%），避免边界信息丢失

最佳实践：先按文档结构切分，块大小300-500 tokens，重叠50 tokens。
