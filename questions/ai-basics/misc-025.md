---
id: misc-025
difficulty: L2
category: ai-basics
subcategory: RAG与向量检索
tags:
- IO
- IOC
images:
- svg_rag_pipeline.svg
feynman:
  essence: 给LLM外挂一个可搜索的“知识硬盘”，随用随查。
  analogy: 像开卷考试，允许考生查阅参考资料来回答问题，而不是只靠脑子记。
  first_principle: 如何在不重新训练模型的前提下，让LLM能够利用外部私有知识并减少胡编乱造？
  key_points:
  - 流程：检索增强生成，先查后答
  - 优势：降低幻觉，知识可实时更新
  - 挑战：检索准确率和分块策略是关键
follow_up:
- 如何评估RAG系统效果?
- RAG和长上下文(Long Context)如何取舍?
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
