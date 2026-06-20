---
id: "agmu-013"
difficulty: "L1"
category: "ai-agent"
subcategory: "多智能体系统"
feynman:
  essence: "BPM 管 确定性流程与人工节点;多 Agent 管 需要语言推理与开放工具调用的步骤.常"
  analogy: "多 Agent 协作就像项目团队——每个 Agent 扮演不同角色（PM/开发/测试），通过消息传递协作，Boss-Worker 是中心调度，Pipeline 是流水线接力。"
  key_points:
    - "多 Agent 管 需要语言推理与开放工具调用的步骤.常 **见架构：** BPM 编排确定性 + LLM Agent 作为某一人工/自动活动"
    - "或 Agent 产出结构化决策, 由 BPM 落账. - *追问应对:**若问「谁主谁辅?」--答:强合规流程 BPM 主"
    - "强探索任务 Agent 主,但要 有 护栏."
first_principle:
  problem: "为什么需要 企业里多 Agent 与「传统工作流引擎(BPM)」关系？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "模型本质是数学函数的参数优化——所有能力都来自数据和参数"
    - "质量 > 数量：数据质量决定模型上限，算法决定达到上限的效率"
  rebuild: "从 AI 系统出发：① 核心挑战是什么？② 现有方案如何解决？③ 有哪些 trade-off？④ 如果重新设计你会怎么做？"
---

# 企业里多 Agent 与「传统工作流引擎(BPM)」关系是什么

BPM 管 确定性流程与人工节点;多 Agent 管 需要语言推理与开放工具调用的步骤.常
**见架构：** BPM 编排确定性 + LLM Agent 作为某一人工/自动活动;或 Agent 产出结构化决策,
由 BPM 落账.
- **追问应对:**若问「谁主谁辅?」--答:强合规流程 BPM 主;强探索任务 Agent 主,但要
有 护栏.
