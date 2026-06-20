---
id: agmu-019
difficulty: L2
category: ai-agent
subcategory: 多智能体系统
tags:
- IO
- IOC
feynman:
  essence: 单 Agent 是工具调度器，多 Agent 是协作组织。
  analogy: 单 Agent 是瑞士军刀，多 Agent 是专家组。
  first_principle: 如何根据任务复杂度选择系统架构模式？
  key_points:
  - 单Agent：统一策略，简单工具调用
  - 多Agent：角色隔离、并行、对抗
  - 选择：任务简单用单Agent
  - 复杂：需组织流程用多Agent
---

# 多 Agent 与「单 Agent + 多个工具」取舍

若只需统一策略调不同 API，单 Agent + 工具即可；若需要角色隔离、并行、对抗评审、组织流程，多 Agent 更合适。
