---
id: eng-practice-s001
difficulty: L2
category: eng-practice
subcategory: 工程化实战
images:
- svg_react.svg
feynman:
  essence: 通过精准的语言指令引导大模型输出高质量结果的技巧。
  analogy: 像给新员工写SOP，不仅要告诉他做什么，还要给他看几个优秀范例，并规定好输出格式。
  first_principle: 如何通过自然语言指令最大化激发模型预训练知识的潜力并控制其输出？
  key_points:
  - 明确角色设定和任务目标
  - 提供Few-shot示例引导模型模仿
  - 使用思维链(CoT)提升复杂推理能力
  - 加入负面约束防止模型幻觉
---

# LLM应用的Prompt工程有哪些最佳实践？

1. **角色设定**: '你是一个经验丰富的XX专家'
2. **任务分解**: 复杂任务拆成步骤
3. **Few-shot**: 提供2-5个示例
4. **输出格式约束**: '请以JSON格式输出，包含字段：xxx'
5. **Chain-of-Thought**: '请一步一步思考'
6. **负面约束**: '不要编造数据，如果不确定请说不知道'

**高级技巧**：
- **Self-Consistency**: 多次采样取多数投票
- **CoT-SC**: CoT + Self-Consistency
- **Tree-of-Thoughts**: 树状思维探索
- **ReAct**: 结合工具调用的推理

**实际工程中**：
1. 模板化管理Prompt（版本控制）
2. A/B测试不同Prompt
3. 使用Prompt框架：LangChain、LlamaIndex
4. 结构化输出：JSON Mode、Outlines、Guidance
5. 多轮对话管理：context window管理
