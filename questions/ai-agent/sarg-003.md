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

Embedding模型是RAG系统的基础，选择考虑因素：

1. 多语言支持：中文场景选择支持中文的模型
- BAAI/bge-large-zh-v1.5（中文最佳）
- BAAI/bge-m3（多语言）
- text-embedding-3-small/large（OpenAI）

2. 维度大小：
- 768维：bge-base
- 1024维：bge-large
- 1536维：OpenAI text-embedding-ada-002
- 维度越大信息越丰富，但存储和检索成本越高

3. 性能评估：MTEB（Massive Text Embedding Benchmark）排行榜

4. 部署方式：
- API：OpenAI、Cohere（无需GPU）
- 本地部署：bge系列（需要GPU）

5. 最大输入长度：通常512 tokens，长文档需要切分

最佳实践：bge-m3支持最多8192 tokens输入，支持稠密+稀疏+多向量检索。
