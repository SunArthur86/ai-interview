---
id: "sarg-006"
difficulty: "L2"
category: "ai-agent"
subcategory: "RAG技术"
images:
  - "svg_rag.svg"
feynman:
  essence: "主流向量数据库对比： 1. Milvus： - 开源、分布式、高性能 - 支持多种索引（HNSW、IVF、DiskANN） - 适合大规模生产环境（亿级向量）"
  analogy: "RAG 就像开卷考试——先翻书找到相关段落（检索），再结合理解写出答案（生成），不靠死记硬背（模型参数），知识可随时更新。"
  key_points:
    - "支持多种索引（HNSW、IVF、DiskANN）"
    - "适合大规模生产环境（亿级向量）"
    - "全托管SaaS、零运维"
first_principle:
  problem: "为什么需要 向量数据库有哪些选择？各有什么特点？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Agent = LLM + 规划 + 记忆 + 工具——LLM 是大脑，其余是手脚"
    - "ReAct 的本质是「思考-行动-观察」循环——显式推理比隐式更可靠"
    - "Agent 的上限不取决于 LLM 能力，而取决于工具集和记忆系统的设计"
  rebuild: "从 Agent 架构出发：① Agent 为什么比纯 LLM 强？② 规划/记忆/工具各自解决什么问题？③ 如何评估 Agent 效果？④ 理想的 Agent 架构是什么样？"
---

# 向量数据库有哪些选择？各有什么特点？

主流向量数据库对比：

1. Milvus：
- 开源、分布式、高性能
- 支持多种索引（HNSW、IVF、DiskANN）
- 适合大规模生产环境（亿级向量）

2. Pinecone：
- 全托管SaaS、零运维
- 商业产品，按用量付费
- 适合快速上线

3. ChromaDB：
- 轻量级、嵌入式
- 适合开发/原型
- 不适合大规模生产

4. Weaviate：
- 开源、支持多模态
- 内置模块化

5. Qdrant：
- Rust实现、高性能
- 支持过滤和payload

6. pgvector（PostgreSQL扩展）：
- 在现有PG数据库上添加向量支持
- 适合不想引入新组件的项目

索引算法：HNSW（精度高、内存大）、IVF（可调精度/速度）、DiskANN（磁盘存储，适合超大规模）。
