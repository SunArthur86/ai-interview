---
id: "misc-034"
difficulty: "L2"
category: "ai-basics"
subcategory: "Prompt Engineering"
tags:
  - "IO"
  - "Elasticsearch"
feynman:
  essence: "Function Calling / Tool Use(最可靠)。"
  analogy: "Prompt 就像给 AI 的工作指令——指令越清晰、示例越精准、推理步骤越明确（CoT），AI 完成质量越高。"
  key_points:
    - "结构化JSON输出的方法:"
    - "方法1:Function Calling / Tool Use(最可靠)"
    - "方法2:JSON Mode(OpenAI/Anthropic原生支持)"
first_principle:
  problem: "如果要解决这个问题，最本质的方法论是什么？先理解问题约束，再找最优路径。"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "Function Calling和JSON Mode有什么区别?"
  - "如何处理模型输出不合法JSON的情况?"
---

# 如何设计结构化Prompt确保LLM稳定输出JSON?有哪些最佳实践

- **结构化JSON输出的方法:**

- **方法1:Function Calling / Tool Use(最可靠)**
```json
{"type": "function", "function": {"name": "extract", "parameters": {"type": "object", "properties": {...}}}}
```

- **方法2:JSON Mode(OpenAI/Anthropic原生支持)**
- 设置 response_format = {"type": "json_object"}

- **方法3:结构化Prompt(通用)**
- 用XML标签分隔指令、示例、输出格式
- 提供JSON Schema
- 使用「只输出JSON,不要其他内容」约束

- **最佳实践:**
1. 提供明确的输出Schema(字段名+类型+描述)
2. 给2-3个Few-shot示例
3. 温度设为0
4. 后处理:正则提取JSON / json5解析 / 重试机制
5. 用Pydantic/Zod定义schema并验证
