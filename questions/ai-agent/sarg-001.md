---
id: sarg-001
difficulty: L1
category: ai-agent
subcategory: RAG技术
images:
- svg_rag.svg
feynman:
  essence: 给LLM外挂知识库，通过检索增强生成答案的准确性。
  analogy: 像考试时允许翻书，遇到不懂的问题查资料再作答。
  first_principle: 如何在不重新训练模型的情况下，让LLM掌握外部知识？
  key_points:
  - 离线索引文档，在线检索增强
  - 解决知识时效性和私有化问题
  - 显著减少幻觉并提供来源
  - 无需训练，落地成本低
---

# RAG的基本架构是什么？为什么需要RAG？

RAG（Retrieval-Augmented Generation）= 检索 + 生成。

基本流程：
1. 离线阶段：文档 → 切片 → Embedding → 存入向量数据库
2. 在线阶段：用户问题 → Embedding → 向量检索 → Top-K文档 → 构造Prompt → LLM生成回答

为什么需要RAG：
1. 知识更新：LLM训练数据有截止日期，RAG可以查询最新信息
2. 私有知识：企业内部文档、API文档等LLM未训练的数据
3. 减少幻觉：有据可依的生成，降低编造
4. 可追溯：可以标注信息来源
5. 成本低：不需要微调模型

对比微调：
- RAG：适合知识密集型任务，无需训练
- 微调：适合风格/格式调整，需要训练数据
- 混合：先微调能力，再用RAG补充知识
