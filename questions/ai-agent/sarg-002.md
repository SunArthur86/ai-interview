---
id: "sarg-002"
difficulty: "L2"
category: "ai-agent"
subcategory: "RAG技术"
images:
  - "svg_rag.svg"
feynman:
  essence: "先按段落(\\n\\n)，再按句子(\\n)，最后按字符。保持语义完整性。LangChain默认。。"
  analogy: "RAG 就像开卷考试——先翻书找到相关段落（检索），再结合理解写出答案（生成），不靠死记硬背（模型参数），知识可随时更新。"
  key_points:
    - "常见策略： 1. 固定长度：按字符数切分（如500字），简单但可能切断语义 2. 递归分割：先按段落( )，再按句子( )，最后按字符"
    - "3. 语义切分（Semantic Chunking）：用embedding计算相邻句子相似度，相似度低于阈值时切分"
    - "4. 文档结构感知：根据文档结构（标题、章节、页码）切分"
first_principle:
  problem: "为什么需要 RAG的Chunking策略有哪些？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Agent = LLM + 规划 + 记忆 + 工具——LLM 是大脑，其余是手脚"
    - "ReAct 的本质是「思考-行动-观察」循环——显式推理比隐式更可靠"
    - "Agent 的上限不取决于 LLM 能力，而取决于工具集和记忆系统的设计"
  rebuild: "从 Agent 架构出发：① Agent 为什么比纯 LLM 强？② 规划/记忆/工具各自解决什么问题？③ 如何评估 Agent 效果？④ 理想的 Agent 架构是什么样？"
---

# RAG的Chunking策略有哪些？

文本切片质量直接影响检索效果。

常见策略：

1. 固定长度：按字符数切分（如500字），简单但可能切断语义

2. 递归分割：先按段落(\n\n)，再按句子(\n)，最后按字符。保持语义完整性。LangChain默认。

3. 语义切分（Semantic Chunking）：用embedding计算相邻句子相似度，相似度低于阈值时切分。效果最好但计算量大。

4. 文档结构感知：根据文档结构（标题、章节、页码）切分。如Markdown按标题层级切分。

5. 父子分块（Parent-Child）：小块检索（精确匹配），大块返回（提供完整上下文）。

关键参数：
- chunk_size：块大小（200-1000 tokens）
- chunk_overlap：重叠区域（10-20%），避免边界信息丢失

最佳实践：先按文档结构切分，块大小300-500 tokens，重叠50 tokens。
