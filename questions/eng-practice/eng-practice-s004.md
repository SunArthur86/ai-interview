---
id: "eng-practice-s004"
difficulty: "L2"
category: "eng-practice"
subcategory: "工程化实战"
images:
  - "svg_quantization.svg"
feynman:
  essence: "Token成本是LLM应用的主要运营成本。"
  analogy: "Agent 成本管控就像家庭理财——跟踪每笔支出（Token消耗），区分必需消费和浪费（缓存命中/模型路由优化），在预算内最大化效果。"
  key_points:
    - "简单任务用小模型（GPT-3.5/GLM-4-Flash）"
    - "复杂任务才用大模型（GPT-4/Claude）"
    - "路由策略：用小模型判断难度，分流到不同模型"
first_principle:
  problem: "从第一性原理看：LLM应用的token成本如何优化 的根本优势/劣势来源于什么？"
  axioms:
    - "模型本质是数学函数的参数优化——所有能力都来自数据和参数"
    - "质量 > 数量：数据质量决定模型上限，算法决定达到上限的效率"
  rebuild: "从 AI 系统出发：① 核心挑战是什么？② 现有方案如何解决？③ 有哪些 trade-off？④ 如果重新设计你会怎么做？"
---

# LLM应用的token成本如何优化？

Token成本是LLM应用的主要运营成本。

1. 模型选择：
- 简单任务用小模型（GPT-3.5/GLM-4-Flash）
- 复杂任务才用大模型（GPT-4/Claude）
- 路由策略：用小模型判断难度，分流到不同模型

2. Prompt优化：
- 精简system prompt
- 压缩对话历史
- 使用摘要替代完整历史

3. 缓存策略：
- Semantic Cache：相同/相似问题命中缓存
- Prompt Caching（API层）：前缀缓存

4. 批量处理：
- Batch API（OpenAI Batch）：50%折扣

5. 上下文管理：
- RAG减少不必要的context
- 动态截断

6. 自建部署：
- 高频使用时自建模型更便宜
- 用vLLM+量化
