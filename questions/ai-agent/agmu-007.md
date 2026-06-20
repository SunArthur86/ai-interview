---
id: agmu-007
difficulty: L1
category: ai-agent
subcategory: 多智能体系统
feynman:
  essence: 稳定流程走 Pipeline，探索任务走动态调度。
  analogy: 流水线生产标准品，特种部队执行动态任务。
  first_principle: 如何适应不同确定性程度的任务处理需求？
  key_points:
  - Pipeline：稳定SOP，契约清晰
  - 动态：探索性，可分叉
  - 混合：主干加动态分支
  - 控制：白名单与预算约束
---

# 动态任务分配和固定 Pipeline 各适合什么场景

**固定 Pipeline 适合**：SOP 稳定、输入输出契约清晰（如审核流水线）。

**动态分配适合**：探索性任务（研究、故障排查），中间可能发现新子问题。

**工程上常混合**：主干 Pipeline + 动态插入节点。

**追问应对**：若问「动态会不会不可控？」——答：需要预算、最大深度、允许的工具白名单与人类在环。
