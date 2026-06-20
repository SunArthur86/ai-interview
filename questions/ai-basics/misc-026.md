---
id: "misc-026"
difficulty: "L2"
category: "ai-basics"
subcategory: "RAG与向量检索"
tags:
  - "IOC"
feynman:
  essence: "RAG 分块（Chunking）策略：固定长度（按 token 数切，简单但可能切断语义）、按结构（段落/标题/Markdown 层级，保留语义）、递归分块（先按大结构再细分）、语义分块（按 embedding 相似度在语义断点切）、重叠分块（相邻块重叠几十 token 防边界丢失）。选型：结构化文档用按结构，长文用语义，追求简单用固定长度+重叠。"
  analogy: "RAG 就像开卷考试——先翻书找到相关段落（检索），再结合理解写出答案（生成），不靠死记硬背（模型参数），知识可随时更新。"
  key_points:
    - "chunk_size: 256-1024 tokens(常用512)"
    - "overlap: chunk_size的10-20%"
    - "最佳实践 - Parent-Child Chunking:"
first_principle:
  problem: "从第一性原理看：RAG中的文档分块(Chunking)有哪些策略?如何选择最优策略 的根本优势/劣势来源于什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "语义分块如何实现?"
  - "Markdown文档如何结构化分块?"
---

# RAG中的文档分块(Chunking)有哪些策略?如何选择最优策略

- **分块策略:**

| 策略 | 方法 | 优点 | 适用 |
|------|------|------|------|
| 固定长度 | 按token数切分 | 简单 | 通用 |
| 递归分割 | 按段落→句子递归 | 保留语义 | 文档 |
| 语义分块 | embedding相似度断句 | **最佳语义** | 高质量RAG |
| 结构化分块 | 按Markdown标题/代码块 | **保留结构** | 技术文档 |
| 父子分块 | 小块检索+大块生成 | **最优方案** | 生产系统 |

- **关键参数:**
- chunk_size: 256-1024 tokens(常用512)
- overlap: chunk_size的10-20%

- **最佳实践 - Parent-Child Chunking:**
1. 文档切成大块(parent, 1024 tokens)
2. 大块再切成小块(child, 256 tokens)
3. **检索用child**(精确匹配)
4. **生成用parent**(完整上下文)
