---
id: "agmu-011"
difficulty: "L1"
category: "ai-agent"
subcategory: "多智能体系统"
feynman:
  essence: "把 角色分工 + 任务依赖 + 执行顺序 从 prompt 工程里抽成一等公民,降低「写一大坨 system prompt」的心智负担,让 协作结构 可见、可复"
  analogy: "多 Agent 协作就像项目团队——每个 Agent 扮演不同角色（PM/开发/测试），通过消息传递协作，Boss-Worker 是中心调度，Pipeline 是流水线接力。"
  key_points:
    - "追问应对"
    - "把 角色分工 + 任务依赖 + 执行顺序 从 prompt 工程里抽成一等公民,降低「写一大坨"
    - "system prompt」的心智负担,让 协作结构 可见、可复用."
first_principle:
  problem: "为什么需要 CrewAI 的「Crew」抽象解决什么问题？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "模型本质是数学函数的参数优化——所有能力都来自数据和参数"
    - "质量 > 数量：数据质量决定模型上限，算法决定达到上限的效率"
  rebuild: "从 AI 系统出发：① 核心挑战是什么？② 现有方案如何解决？③ 有哪些 trade-off？④ 如果重新设计你会怎么做？"
---

# CrewAI 的「Crew」抽象解决什么问题

把 角色分工 + 任务依赖 + 执行顺序 从 prompt 工程里抽成一等公民,降低「写一大坨
system prompt」的心智负担,让 协作结构 可见、可复用.

- **追问应对:**若问缺点?答:抽象与真实权限/数据边界 仍需自己把控;复杂分支可能要
下沉到代码.
