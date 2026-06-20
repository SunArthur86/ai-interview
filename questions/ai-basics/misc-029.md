---
id: "misc-029"
difficulty: "L2"
category: "ai-basics"
subcategory: "RAG与向量检索"
tags:
  - "IOC"
feynman:
  essence: "RAG 查询改写技术包括：① Query Rewriting（LLM 把模糊问题改写成精确检索查询）；② HyDE（先让 LLM 生成假设答案，再用它去检索，解决 query 与 doc 表达不一致）；③ Step-Back Prompting（先问更高层的概念再检索具体事实）；④ Multi-Query（生成多个子查询并行检索再融合）。"
  analogy: "RAG 就像开卷考试——先翻书找到相关段落（检索），再结合理解写出答案（生成），不靠死记硬背（模型参数），知识可随时更新。"
  key_points:
    - "1. Query Rewriting(查询改写):"
    - "用LLM将用户模糊问题改写为更精确的检索查询"
    - "例:「怎么用那个东西」→「如何使用React Hooks」"
first_principle:
  problem: "为什么需要 RAG中的查询改写技术有哪些?HyDE和Step-Back Prompting分别解决什么问题？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "HyDE在什么场景下效果最好?"
  - "Multi-Query会增加多少延迟?"
---

# RAG中的查询改写技术有哪些?HyDE和Step-Back Prompting分别解决什么问题

- **查询改写技术:**

- **1. Query Rewriting(查询改写):**
- 用LLM将用户模糊问题改写为更精确的检索查询
- 例:「怎么用那个东西」→「如何使用React Hooks」

- **2. HyDE (Hypothetical Document Embeddings):**
- 先让LLM生成一个假想答案
- 用假想答案的embedding去检索(而不是用原问题)
- 原理:答案比问题更接近目标文档的语义
- 效果:对于事实型问题检索质量大幅提升

- **3. Step-Back Prompting:**
- 将具体问题抽象为更宽泛的问题
- 例:「Google 2024 Q4收入」→「Google最近4个季度收入趋势」
- 先检索背景知识,再回答具体问题

- **4. Multi-Query:**
- 用LLM生成同一问题的多个变体
- 分别检索后取并集+去重+重排
