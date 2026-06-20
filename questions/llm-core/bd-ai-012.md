---
id: bd-ai-012
difficulty: L3
category: llm-core
categories:
- ai-agent
- eng-practice
- llm-core
subcategory: Prompt工程
tags:
- 字节
- 面经
- Function Calling
- RAG
- Embedding
feynman:
  essence: Function Calling获取实时结构化数据，RAG检索离线非结构化知识。
  analogy: Function Calling是打电话问实时信息，RAG是去图书馆翻阅历史档案。
  first_principle: 如何将外部世界的实时数据与静态知识高效注入模型上下文？
  key_points:
  - Function Calling适合实时交互和工具执行
  - RAG适合私有知识库和文档问答
  - 向量检索基于语义而非关键词匹配
  - 常用混合检索与重排序提升精度
follow_up:
- Function Calling和RAG能同时用吗？——可以，Agent自主决定调哪个
- RAG的检索效果怎么评估？——Recall@K + MRR + 人工标注准确率
- 向量数据库选型？——Milvus(大规模)/Qdrant(轻量)/Pinecone(托管)
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

**Function Calling 与 RAG 流程对比：**
```text
Function Calling 流程:          RAG 流程:
User Query                       User Query
    ↓                                ↓
┌─────────────┐                ┌───────────────────┐
│   Intent    │                │   Query Rewrite   │
│Classification│               └─────────┬─────────┘
└──────┬──────┘                          │
       │                                 ↓
       ↓                         ┌───────────────────┐
┌─────────────┐                │  Vector Retrieval │ (Semantic Search)
│   External  │                └─────────┬─────────┘
│   API Call  │                          │
└──────┬──────┘                          ↓
       │                         ┌───────────────────┐
       ↓                         │  Context (Chunks) │
┌─────────────┐                └─────────┬─────────┘
│ Structured  │                          │
│    Data     │                          ↓
└──────┬──────┘                    ┌───────────────────┐
       │                           │   LLM Generation │
       └───────────┬───────────────┴─────────┬─────────┘
                   ↓                           ↓
              Final Answer (Fact+Reasoning)
```

**检索策略设计关键点：**
1. 混合检索（向量+关键词，用RRF融合）
2. Chunk大小要调（512-1024 Token，带重叠）
3. HyDE（先生成假答案再检索）
4. Rerank（Cross-Encoder重排提升精度）

## 常见考点
1. **参数缺失**：如果Function Call需要的参数用户没给，是直接报错还是反问用户？（策略：反问用户补充信息，不要自己瞎编参数）
2. **多跳查询**：RAG中遇到复杂问题需要多次检索才能回答，如何设计？（Agent推理链路：Answer A -> Question B -> Retrieve B -> Synthesize）
3. **时效性差异**：RAG适合解决时效性问题吗？（不适合，除非向量库更新频率极高，否则实时数据还是依赖Function Calling或搜索引擎）
