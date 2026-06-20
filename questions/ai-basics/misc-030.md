---
id: misc-030
difficulty: L2
category: ai-basics
subcategory: RAG与向量检索
tags:
- IOC
feynman:
  essence: 利用知识图谱结构化信息，解决全局理解和复杂推理问题。
  analogy: 从零散的碎纸片（向量RAG）拼成了一张结构清晰的地图（GraphRAG），既能看局部也能看全貌。
  first_principle: 如何让RAG系统不仅回答局部事实，还能理解数据集的全局结构和潜在联系？
  key_points:
  - 构建实体关系图谱，进行社区归纳
  - Local Search查点，Global Search查面
  - 擅长多跳推理和全局综述
follow_up:
- GraphRAG的图谱构建成本如何控制?
- 社区检测算法如何选择?
---

# GraphRAG(微软提出)是什么?相比传统向量RAG有什么优势

- **GraphRAG核心思想:**

**传统RAG：** 文档→chunks→embedding→检索
**GraphRAG：** 文档→**知识图谱**→社区检测→多层级摘要→检索

- **构建流程:**
1. **实体抽取** - LLM从文档中抽取实体和关系
2. **图谱构建** - 构建实体-关系图
3. **社区检测** - Leiden算法将图划分为层级社区
4. **摘要生成** - 为每个社区生成摘要

- **两种检索模式:**
- **Local Search:** 从相关实体出发,检索邻域子图 → 适合具体问题
- **Global Search:** 遍历所有社区摘要 → 适合「整个数据集讲了什么」类全局问题

- **优势:**
1. **多跳推理** - 图结构天然支持
2. **全局理解** - 社区摘要解决「整体洞察」类问题
3. **可溯源** - 答案可追溯到具体关系链

- **代价:** 图谱构建成本高(大量LLM调用)
