---
id: "eng-practice-s001"
difficulty: "L2"
category: "eng-practice"
subcategory: "工程化实战"
images:
  - "svg_react.svg"
feynman:
  essence: "1. 角色设定：'你是一个经验丰富的XX专家' 2. 任务分解：复杂任务拆成步骤 3. Few-shot：提供2-5个示例 4. 输出格式约束：'请以JSON格"
  analogy: "Prompt 就像给 AI 的工作指令——指令越清晰、示例越精准、推理步骤越明确（CoT），AI 完成质量越高。"
  key_points:
    - "角色设定：'你是一个经验丰富的XX专家'"
    - "任务分解：复杂任务拆成步骤"
    - "Few-shot：提供2-5个示例"
first_principle:
  problem: "为什么需要 LLM应用的Prompt工程有哪些最佳实践？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "模型本质是数学函数的参数优化——所有能力都来自数据和参数"
    - "质量 > 数量：数据质量决定模型上限，算法决定达到上限的效率"
  rebuild: "从 AI 系统出发：① 核心挑战是什么？② 现有方案如何解决？③ 有哪些 trade-off？④ 如果重新设计你会怎么做？"
---

# LLM应用的Prompt工程有哪些最佳实践？

1. 角色设定：'你是一个经验丰富的XX专家'
2. 任务分解：复杂任务拆成步骤
3. Few-shot：提供2-5个示例
4. 输出格式约束：'请以JSON格式输出，包含字段：xxx'
5. Chain-of-Thought：'请一步一步思考'
6. 负面约束：'不要编造数据，如果不确定请说不知道'

高级技巧：
- Self-Consistency：多次采样取多数投票
- CoT-SC：CoT + Self-Consistency
- Tree-of-Thoughts：树状思维探索
- ReAct：结合工具调用的推理

实际工程中：
1. 模板化管理Prompt（版本控制）
2. A/B测试不同Prompt
3. 使用Prompt框架：LangChain、LlamaIndex
4. 结构化输出：JSON Mode、Outlines、Guidance
5. 多轮对话管理：context window管理
