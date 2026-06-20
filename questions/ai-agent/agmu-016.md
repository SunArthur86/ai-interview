---
id: "agmu-016"
difficulty: "L2"
category: "ai-agent"
subcategory: "多智能体系统"
feynman:
  essence: "会,所以需要 单一契约源(OpenAPI/JSON Schema)+ 契约测试 Agent 或静态检查 + 状态机门禁."
  analogy: "多 Agent 协作就像项目团队——每个 Agent 扮演不同角色（PM/开发/测试），通过消息传递协作，Boss-Worker 是中心调度，Pipeline 是流水线接力。"
  key_points:
    - "会,所以需要 单一契约源(OpenAPI/JSON Schema)+ 契约测试 Agent 或静态检查 +"
first_principle:
  problem: "为什么需要 多 Agent 会不会降低「一致性」(同一产品前后端接口对不上)？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "模型本质是数学函数的参数优化——所有能力都来自数据和参数"
    - "质量 > 数量：数据质量决定模型上限，算法决定达到上限的效率"
  rebuild: "从 AI 系统出发：① 核心挑战是什么？② 现有方案如何解决？③ 有哪些 trade-off？④ 如果重新设计你会怎么做？"
---

# 多 Agent 会不会降低「一致性」(同一产品前后端接口对不上)

会,所以需要 单一契约源(OpenAPI/JSON Schema)+ 契约测试 Agent 或静态检查 +
状态机门禁.
