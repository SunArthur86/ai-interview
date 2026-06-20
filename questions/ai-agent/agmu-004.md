---
id: "agmu-004"
difficulty: "L1"
category: "ai-agent"
subcategory: "多智能体系统"
feynman:
  essence: "Pipeline 强调 固定的阶段顺序与数据形态;Boss-Worker 强调 动态任务图--Boss 可 按需增删子任务、并行派发.Pipeline 更像工厂"
  analogy: "Boss-Worker 和 Pipeline 就像两种工厂模式——Boss-Worker 是经理派活工人干（中心调度），Pipeline 是流水线每人负责一步（链式传递）。"
  key_points:
    - "Pipeline 强调 固定的阶段顺序与数据形态"
    - "Boss-Worker 强调 动态任务图--Boss 可 按需增删子任务、并行派发.Pipeline 更像工厂流水线"
    - "Boss-Worker 更像项目经理排期. - *追问应对:**若问「能混合吗?」--答:非常常见,例如 Boss 定阶段,阶段内 Pipeline, 阶段间 讨论."
first_principle:
  problem: "它们本质上为什么不同？各自的设计目标和适用场景是什么？"
  axioms:
    - "模型本质是数学函数的参数优化——所有能力都来自数据和参数"
    - "质量 > 数量：数据质量决定模型上限，算法决定达到上限的效率"
  rebuild: "从 AI 系统出发：① 核心挑战是什么？② 现有方案如何解决？③ 有哪些 trade-off？④ 如果重新设计你会怎么做？"
---

# Boss-Worker 和 Pipeline 有什么本质差异

Pipeline 强调 固定的阶段顺序与数据形态;Boss-Worker 强调 动态任务图--Boss 可
按需增删子任务、并行派发.Pipeline 更像工厂流水线;Boss-Worker 更像项目经理排期.
- **追问应对:**若问「能混合吗?」--答:非常常见,例如 Boss 定阶段,阶段内 Pipeline,
阶段间 讨论.
