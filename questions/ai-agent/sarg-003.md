---
id: "sarg-003"
difficulty: "L2"
category: "ai-agent"
subcategory: "RAG技术"
images:
  - "svg_rag.svg"
feynman:
  essence: "Embedding模型是RAG系统的基础，选择考虑因素： 1. 多语言支持：中文场景选择支持中文的模型 - BAAI/bge-large-zh-v1.5（中文最"
  analogy: "Embedding 就像把词语放到语义地图上——意思相近的词距离近，无关的词距离远，让机器能计算「相似度」。"
  key_points:
    - "多语言支持：中文场景选择支持中文的模型"
    - "BAAI/bge-large-zh-v1.5（中文最佳）"
    - "BAAI/bge-m3（多语言）"
first_principle:
  problem: "如果要解决这个问题，最本质的方法论是什么？先理解问题约束，再找最优路径。"
  axioms:
    - "Agent = LLM + 规划 + 记忆 + 工具——LLM 是大脑，其余是手脚"
    - "ReAct 的本质是「思考-行动-观察」循环——显式推理比隐式更可靠"
    - "Agent 的上限不取决于 LLM 能力，而取决于工具集和记忆系统的设计"
  rebuild: "从 Agent 架构出发：① Agent 为什么比纯 LLM 强？② 规划/记忆/工具各自解决什么问题？③ 如何评估 Agent 效果？④ 理想的 Agent 架构是什么样？"
---

# 如何选择Embedding模型？

Embedding模型是RAG系统的基础，选择考虑因素：

1. 多语言支持：中文场景选择支持中文的模型
- BAAI/bge-large-zh-v1.5（中文最佳）
- BAAI/bge-m3（多语言）
- text-embedding-3-small/large（OpenAI）

2. 维度大小：
- 768维：bge-base
- 1024维：bge-large
- 1536维：OpenAI text-embedding-ada-002
- 维度越大信息越丰富，但存储和检索成本越高

3. 性能评估：MTEB（Massive Text Embedding Benchmark）排行榜

4. 部署方式：
- API：OpenAI、Cohere（无需GPU）
- 本地部署：bge系列（需要GPU）

5. 最大输入长度：通常512 tokens，长文档需要切分

最佳实践：bge-m3支持最多8192 tokens输入，支持稠密+稀疏+多向量检索。
