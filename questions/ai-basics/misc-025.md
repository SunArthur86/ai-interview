---
id: "misc-025"
difficulty: "L2"
category: "ai-basics"
subcategory: "RAG与向量检索"
tags:
  - "IO"
  - "IOC"
images:
  - "svg_rag_pipeline.svg"
feynman:
  essence: "**RAG (Retrieval-Augmented Generation) 流程:**"
  analogy: "RAG 就像开卷考试——先翻书找到相关段落（检索），再结合理解写出答案（生成），不靠死记硬背（模型参数），知识可随时更新。"
  key_points:
    - "RAG (Retrieval-Augmented Generation) 流程:"
    - "知识实时性 - 数据更新只需更新知识库"
    - "减少幻觉 - 有据可依"
first_principle:
  problem: "从第一性原理看：RAG的基本流程?相比纯LLM有什么优势?核心挑战有哪些 的根本优势/劣势来源于什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "如何评估RAG系统效果?"
  - "RAG和长上下文(Long Context)如何取舍?"
---

# RAG的基本流程是什么?相比纯LLM有什么优势?核心挑战有哪些

- **RAG (Retrieval-Augmented Generation) 流程:**

```
用户问题 → Embedding → 向量检索 → Top-K文档 → 拼接Prompt → LLM生成
```

- **优势:**
1. **知识实时性** - 数据更新只需更新知识库
2. **减少幻觉** - 有据可依
3. **可溯源** - 答案可标注来源
4. **成本低** - 无需微调模型

- **核心挑战:**
1. **检索质量** - 召回不准确导致答案错误
2. **分块策略** - chunk太大浪费token,太小丢失上下文
3. **多跳推理** - 答案需要多个文档拼接
4. **重排** - 向量相似不等于语义相关
5. **查询理解** - 用户问题可能模糊或需要改写
