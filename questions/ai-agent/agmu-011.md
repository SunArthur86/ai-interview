---
id: agmu-011
difficulty: L1
category: ai-agent
subcategory: 多智能体系统
feynman:
  essence: 将协作结构显式化以降低 Prompt 编程的复杂度。
  analogy: 像把口头分工变成了可视化的组织架构图。
  first_principle: 如何将隐式的协作逻辑转化为可管理的显式结构？
  key_points:
  - 抽象：角色、任务、依赖为一等公民
  - 价值：结构可见可复用
  - 简化：降低Prompt负担
  - 局限：权限边界需手动把控
---

# CrewAI 的「Crew」抽象解决什么问题

把角色分工 + 任务依赖 + 执行顺序从 prompt 工程里抽成一等公民，降低「写一大坨 system prompt」的心智负担，让协作结构可见、可复用。

**追问应对**：若问缺点？答：抽象与真实权限/数据边界仍需自己把控；复杂分支可能要下沉到代码。
