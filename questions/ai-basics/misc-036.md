---
id: "misc-036"
difficulty: "L2"
category: "ai-basics"
subcategory: "Prompt Engineering"
tags:
  - "CAS"
  - "Elasticsearch"
feynman:
  essence: "**System Prompt设计框架 (CREATE):**"
  analogy: "Prompt 就像给 AI 的工作指令——指令越清晰、上下文越充分，AI 完成质量越高。"
  key_points:
    - "System Prompt设计框架 (CREATE):"
    - "Context - 角色和背景(你是XX公司的AI助手)"
    - "Role - 具体职责(你负责回答客户的技术问题)"
first_principle:
  problem: "为什么需要 System Prompt设计的最佳实践?如何设计有效的角色和约束？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "System Prompt应该多长?"
  - "如何版本管理Prompt?"
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
