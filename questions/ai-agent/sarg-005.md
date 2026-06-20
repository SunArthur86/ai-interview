---
id: "sarg-005"
difficulty: "L3"
category: "ai-agent"
subcategory: "RAG技术"
images:
  - "svg_rag.svg"
feynman:
  essence: "基础RAG之上的进阶优化：  1. Query Rewrite（查询重写）： - 将用户口语化问题重写为更适合检索的形式 - HyDE：先让LLM生成假设答案，用假设答案做检索  2. Multi-Query（多查询）： - LLM从多个角度重写问题 - 分别检索。"
  analogy: "RAG 就像开卷考试——先翻书找到相关段落（检索），再结合理解写出答案（生成），不靠死记硬背（模型参数），知识可随时更新。"
  key_points:
    - "Query Rewrite（查询重写）："
    - "将用户口语化问题重写为更适合检索的形式"
    - "HyDE：先让LLM生成假设答案，用假设答案做检索"
first_principle:
  problem: "为什么需要 RAG有哪些进阶技术？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Agent = LLM + 规划 + 记忆 + 工具——LLM 是大脑，其余是手脚"
    - "ReAct 的本质是「思考-行动-观察」循环——显式推理比隐式更可靠"
    - "Agent 的上限不取决于 LLM 能力，而取决于工具集和记忆系统的设计"
  rebuild: "从 Agent 架构出发：① Agent 为什么比纯 LLM 强？② 规划/记忆/工具各自解决什么问题？③ 如何评估 Agent 效果？④ 理想的 Agent 架构是什么样？"
---

# RAG有哪些进阶技术？

基础RAG之上的进阶优化：

1. Query Rewrite（查询重写）：
- 将用户口语化问题重写为更适合检索的形式
- HyDE：先让LLM生成假设答案，用假设答案做检索

2. Multi-Query（多查询）：
- LLM从多个角度重写问题
- 分别检索，合并结果

3. Step-back Prompting：
- 先问更高层次的问题获取背景知识
- 再问具体问题

4. GraphRAG：
- 将文档构建知识图谱
- 检索时做图遍历，发现跨文档关系

5. Self-RAG：
- LLM自主决定何时检索、检索几次
- 评估检索结果质量，决定是否使用

6. Adaptive RAG：
- 根据问题复杂度选择不同策略
- 简单问题直接回答，复杂问题多轮检索

7. Long-context RAG：
- 利用长上下文模型（如Gemini 1M tokens）
- 减少检索次数，直接放入大量context
