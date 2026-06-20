---
id: sarg-005
difficulty: L3
category: ai-agent
subcategory: RAG技术
images:
- svg_rag.svg
feynman:
  essence: 通过优化查询、检索策略和上下文利用来提升RAG效果。
  analogy: 从简单的“关键词匹配”进化到“专家查阅资料并推理”。
  first_principle: 如何让检索增强生成系统处理复杂查询并减少幻觉？
  key_points:
  - 查询重写与多路召回
  - 图谱与自省机制
  - 长短上下文自适应策略
---

# RAG有哪些进阶技术？

基础RAG之上的进阶优化：

1. **Query Rewrite（查询重写）**：
- 将用户口语化问题重写为更适合检索的形式
- HyDE：先让LLM生成假设答案，用假设答案做检索

2. **Multi-Query（多查询）**：
- LLM从多个角度重写问题
- 分别检索，合并结果

3. **Step-back Prompting**：
- 先问更高层次的问题获取背景知识
- 再问具体问题

4. **GraphRAG**：
- 将文档构建知识图谱
- 检索时做图遍历，发现跨文档关系

5. **Self-RAG**：
- LLM自主决定何时检索、检索几次
- 评估检索结果质量，决定是否使用

6. **Adaptive RAG**：
- 根据问题复杂度选择不同策略
- 简单问题直接回答，复杂问题多轮检索

7. **Long-context RAG**：
- 利用长上下文模型（如Gemini 1M tokens）
- 减少检索次数，直接放入大量context
