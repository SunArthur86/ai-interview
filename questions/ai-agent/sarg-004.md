---
id: "sarg-004"
difficulty: "L2"
category: "ai-agent"
subcategory: "RAG技术"
images:
  - "svg_rag.svg"
feynman:
  essence: "Reranking（重排序）是对初步检索结果用更精确的模型重新排序。"
  analogy: "RAG 就像开卷考试——先翻书找到相关段落（检索），再结合理解写出答案（生成），不靠死记硬背（模型参数），知识可随时更新。"
  key_points:
    - "Reranking（重排序）是对初步检索结果用更精确的模型重新排序"
    - "为什么需要： 1. 向量检索速度快但精度有限（embedding是压缩表示，有信息损失） 2. 召回阶段取Top-50/100（高召回率），Rerank阶段精排到Top-5/10（高精确率） 3. C"
    - "速度快但精度有限 - Cross-Encoder（Reranker）：query和doc拼接后一起输入模型，输出相关性分数"
first_principle:
  problem: "为什么需要 Reranking？为什么RAG需要它？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Agent = LLM + 规划 + 记忆 + 工具——LLM 是大脑，其余是手脚"
    - "ReAct 的本质是「思考-行动-观察」循环——显式推理比隐式更可靠"
    - "Agent 的上限不取决于 LLM 能力，而取决于工具集和记忆系统的设计"
  rebuild: "从 Agent 架构出发：① Agent 为什么比纯 LLM 强？② 规划/记忆/工具各自解决什么问题？③ 如何评估 Agent 效果？④ 理想的 Agent 架构是什么样？"
---

# 什么是Reranking？为什么RAG需要它？

Reranking（重排序）是对初步检索结果用更精确的模型重新排序。

为什么需要：
1. 向量检索速度快但精度有限（embedding是压缩表示，有信息损失）
2. 召回阶段取Top-50/100（高召回率），Rerank阶段精排到Top-5/10（高精确率）
3. Cross-Encoder模型比Bi-Encoder更准确

Bi-Encoder vs Cross-Encoder：
- Bi-Encoder（Embedding）：query和doc分别编码，计算余弦相似度。速度快但精度有限
- Cross-Encoder（Reranker）：query和doc拼接后一起输入模型，输出相关性分数。精度高但速度慢

常用Reranker：
- BAAI/bge-reranker-v2-m3（多语言）
- Cohere Rerank API
- bce-reranker-base_v1

流程：向量检索Top-100 → Rerank到Top-5 → 拼入Prompt
