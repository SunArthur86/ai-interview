---
id: misc-034
difficulty: L2
category: ai-basics
subcategory: Prompt Engineering
tags:
- IO
- Elasticsearch
feynman:
  essence: 通过格式约束与结构化定义引导模型输出标准JSON数据。
  analogy: 像填表一样给模型空格子，并告诉他不要在格子外写字。
  first_principle: 如何解决非结构化文本输出难以被程序解析和集成的问题？
  key_points:
  - 优先使用Function Calling或原生JSON Mode
  - 提供JSON Schema和Few-shot示例
  - 设置低温度并配合后处理校验
follow_up:
- Function Calling和JSON Mode有什么区别?
- 如何处理模型输出不合法JSON的情况?
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
