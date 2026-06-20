---
id: sarg-006
difficulty: L2
category: ai-agent
subcategory: RAG技术
images:
- svg_rag.svg
feynman:
  essence: 专门用于存储、索引和检索高维向量数据的数据库。
  analogy: 书籍目录不仅记录书名，还能根据内容相似度快速找书。
  first_principle: 如何在大规模高维空间中实现毫秒级的近似最近邻搜索？
  key_points:
  - 分布式与SaaS之分
  - 核心算法影响性能与精度
  - pgvector降低集成门槛
---

# 向量数据库有哪些选择？各有什么特点？

主流向量数据库对比：

1. **Milvus**：
- 开源、分布式、高性能
- 支持多种索引（HNSW、IVF、DiskANN）
- 适合大规模生产环境（亿级向量）

2. **Pinecone**：
- 全托管SaaS、零运维
- 商业产品，按用量付费
- 适合快速上线

3. **ChromaDB**：
- 轻量级、嵌入式
- 适合开发/原型
- 不适合大规模生产

4. **Weaviate**：
- 开源、支持多模态
- 内置模块化

5. **Qdrant**：
- Rust实现、高性能
- 支持过滤和payload

6. **pgvector（PostgreSQL扩展）**：
- 在现有PG数据库上添加向量支持
- 适合不想引入新组件的项目

**索引算法：** HNSW（精度高、内存大）、IVF（可调精度/速度）、DiskANN（磁盘存储，适合超大规模）。
