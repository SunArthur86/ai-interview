---
id: "sarg-001"
difficulty: "L1"
category: "ai-agent"
subcategory: "RAG技术"
images:
  - "svg_rag.svg"
feynman:
  essence: "RAG（Retrieval-Augmented Generation）= 检索 + 生成"
  analogy: "RAG 就像开卷考试——先翻书找到相关段落（检索），再结合理解写出答案（生成），不靠死记硬背（模型参数），知识可随时更新。"
  key_points:
    - "离线阶段：文档 → 切片(chunking) → Embedding → 存入向量数据库"
    - "在线阶段：用户问题 → Embedding → 向量检索 → Top-K文档 → 构造Prompt → LLM生成回答"
    - "知识更新：LLM训练数据有截止日期，RAG可以查询最新信息"
first_principle:
  problem: "为什么需要 RAG的基本架构？为什么需要RAG？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Agent = LLM + 规划 + 记忆 + 工具——LLM 是大脑，其余是手脚"
    - "ReAct 的本质是「思考-行动-观察」循环——显式推理比隐式更可靠"
    - "Agent 的上限不取决于 LLM 能力，而取决于工具集和记忆系统的设计"
  rebuild: "从 Agent 架构出发：① Agent 为什么比纯 LLM 强？② 规划/记忆/工具各自解决什么问题？③ 如何评估 Agent 效果？④ 理想的 Agent 架构是什么样？"
---

# RAG的基本架构是什么？为什么需要RAG？

RAG（Retrieval-Augmented Generation）= 检索 + 生成。

基本流程：
1. 离线阶段：文档 → 切片(chunking) → Embedding → 存入向量数据库
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
