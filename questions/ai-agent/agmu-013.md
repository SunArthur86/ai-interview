---
id: agmu-013
difficulty: L1
category: ai-agent
subcategory: 多智能体系统
feynman:
  essence: BPM 管确定流程，Agent 管模糊推理。
  analogy: BPM 是红绿灯和道路，Agent 是司机。
  first_principle: 如何融合刚性业务流程与柔性智能决策？
  key_points:
  - BPM：确定性流程，人工节点
  - Agent：语言推理，开放工具
  - 架构：BPM编排Agent作为节点
  - 主辅：合规BPM为主，探索Agent为主
---

# 企业里多 Agent 与「传统工作流引擎(BPM)」关系是什么

BPM 管确定性流程与人工节点；多 Agent 管需要语言推理与开放工具调用的步骤。

**常见架构**：BPM 编排确定性 + LLM Agent 作为某一人工/自动活动；或 Agent 产出结构化决策，由 BPM 落账。

**追问应对**：若问「谁主谁辅？」——答：强合规流程 BPM 主；强探索任务 Agent 主，但要有护栏。
