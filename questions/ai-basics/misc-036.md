---
id: misc-036
difficulty: L2
category: ai-basics
subcategory: Prompt Engineering
tags:
- CAS
- Elasticsearch
feynman:
  essence: 通过明确角色、规则和约束来精确控制模型的行为边界。
  analogy: 像给新员工发详细的《岗位手册》，告诉他该做什么、不该做什么以及怎么说话。
  first_principle: 如何将模糊的任务需求转化为模型可理解、可执行的精确指令？
  key_points:
  - 使用CREATE框架构建完整人设
  - 多用具体正面指令，少用模糊否定
  - System层定规矩，User层派任务
follow_up:
- System Prompt应该多长?
- 如何版本管理Prompt?
---

# System Prompt设计的最佳实践是什么?如何设计有效的角色和约束

- **System Prompt设计框架 (CREATE):**

- **C**ontext - 角色和背景(你是XX公司的AI助手)
- **R**ole - 具体职责(你负责回答客户的技术问题)
- **E**xamples - 示例对话
- **A**uthenticity - 语气风格(专业但友好)
- **R**ules - 规则约束(不要编造、不确定时说不知道)
- **T**one - 输出格式(结构化、带标题)
- **E**dge cases - 边界处理(遇到XX时应该YY)

- **关键原则:**
1. **具体>模糊** - 「回答200字以内」优于「简洁回答」
2. **正面指令>负面指令** - 「只基于文档回答」优于「不要编造」
3. **结构化** - 用Markdown/XML标签组织prompt
4. **分层** - System层定角色,User层给任务
5. **可测试** - 每条规则都能通过测试用例验证
