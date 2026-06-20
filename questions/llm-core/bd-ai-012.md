---
id: "bd-ai-012"
difficulty: "L3"
category: "llm-core"
categories:
  - "ai-agent"
  - "eng-practice"
  - "llm-core"
subcategory: "Prompt工程"
tags:
  - "字节"
  - "面经"
  - "Function Calling"
  - "RAG"
  - "Embedding"
feynman:
  essence: "Function Calling=让AI去做（调API执行操作），RAG=让AI去查（检索文档补充知识）。两者互补不互斥。"
  analogy: "FC像报警台（实时接警+派警执行），RAG像图书馆（查阅资料获取背景）。复杂任务=先去图书馆查资料，再报警执行。"
  key_points:
    - "FC:实时+结构化+可执行"
    - "RAG:离线+非结构化+只读"
    - "Embedding=语义翻译官"
    - "实际项目:两者结合"
first_principle:
  problem: "LLM知识有截止日期且无执行能力。如何获取实时信息？如何使用私有知识？"
  axioms:
    - "模型知识有截止日期→需要外部数据源"
    - "模型无执行能力→需要FC"
    - "私有知识不在训练集中→需要RAG"
  rebuild: "从模型局限出发：实时数据怎么获取（FC调API）？私有知识怎么补充（RAG向量检索）？两者如何配合（Agent自主决策）？检索质量怎么保证（混合检索+Rerank）？"
follow_up:
  - "Function Calling和RAG能同时用吗？——可以，Agent自主决定调哪个"
  - "RAG的检索效果怎么评估？——Recall@K + MRR + 人工标注准确率"
  - "向量数据库选型？——Milvus(大规模)/Qdrant(轻量)/Pinecone(托管)"
---

# 【字节面经】Function Calling与RAG的区别和联系是什么？什么时候用Function Calling，什么时候用RAG？

**两者都是让模型基于真实数据回答，但方式完全不同。**

**Function Calling：** 让模型调用外部接口获取实时数据（天气/股票/数据库查询）。特点是数据实时的、结构化的，模型拿到就能用。

**RAG：** 把私有文档检索出来塞进上下文（公司文档/产品手册/会议纪要）。特点是数据离线的、非结构化的，需要先切片→Embedding→存向量数据库。

**什么时候用哪个？**
- 需要实时数据或需要执行操作 → Function Calling
- 需要领域知识或私有文档 → RAG
- 实际项目中经常两者结合：RAG提供知识背景，Function Calling提供实时数据和执行能力

**Embedding/向量数据库在RAG中的作用：**
- Embedding是RAG的翻译官，把文本转成向量，语义相近的向量距离就近
- 向量数据库是存这些向量的专用仓库（Milvus/Pinecone/Qdrant），核心能力是快速做相似度检索
- RAG的检索不是关键词匹配而是算向量距离

**检索策略设计关键点：**
1. 混合检索（向量+关键词，用RRF融合）
2. Chunk大小要调（512-1024 Token，带重叠）
3. HyDE（先生成假答案再检索）
4. Rerank（Cross-Encoder重排提升精度）
