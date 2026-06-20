---
id: "misc-030"
difficulty: "L2"
category: "ai-basics"
subcategory: "RAG与向量检索"
tags:
  - "IOC"
feynman:
  essence: "- *GraphRAG核心思想:** **传统RAG：** 文档→chunks→embedding→检索 **GraphRAG：** 文档→**知识图谱**→社"
  analogy: "RAG 就像开卷考试——先翻书找到相关段落（检索），再结合理解写出答案（生成），不靠死记硬背（模型参数），知识可随时更新。"
  key_points:
    - "GraphRAG核心思想:"
    - "实体抽取 - LLM从文档中抽取实体和关系"
    - "图谱构建 - 构建实体-关系图"
first_principle:
  problem: "从第一性原理看：GraphRAG(微软提出)?相比传统向量RAG有什么优势 的根本优势/劣势来源于什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "GraphRAG的图谱构建成本如何控制?"
  - "社区检测算法如何选择?"
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
