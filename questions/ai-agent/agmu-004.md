---
id: agmu-004
difficulty: L1
category: ai-agent
subcategory: 多智能体系统
feynman:
  essence: Pipeline 重顺序，Boss-Worker 重动态调度。
  analogy: Pipeline 是固定传送带，Boss-Worker 是灵活的派单中心。
  first_principle: 如何平衡任务执行的确定性与灵活性？
  key_points:
  - Pipeline：固定阶段，顺序执行
  - Boss-Worker：动态图，并行派发
  - 混合：Boss定阶段，内部跑Pipeline
  - 差异：确定性 vs 灵活性
---

# Boss-Worker 和 Pipeline 有什么本质差异

Pipeline 强调固定的阶段顺序与数据形态；Boss-Worker 强调动任务态图——Boss 可按需增删子任务、并行派发。

**Pipeline 更像工厂流水线**；**Boss-Worker 更像项目经理排期**。

**追问应对**：若问「能混合吗？」——答：非常常见，例如 Boss 定阶段，阶段内 Pipeline，阶段间讨论。
