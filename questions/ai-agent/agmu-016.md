---
id: agmu-016
difficulty: L2
category: ai-agent
subcategory: 多智能体系统
feynman:
  essence: 多 Agent 协作需引入统一契约源以保障一致性。
  analogy: 多人协作装修必须按同一张图纸施工。
  first_principle: 如何消除多智能体并行协作中的数据冲突？
  key_points:
  - 风险：多Agent易导致不一致
  - 契约：单一源头（Schema）
  - 校验：契约测试Agent或静态检查
  - 门禁：状态机约束
---

# 多 Agent 会不会降低「一致性」(同一产品前后端接口对不上)

会，所以需要单一契约源（OpenAPI/JSON Schema）+ 契约测试 Agent 或静态检查 + 状态机门禁。
