---
id: "agmu-017"
difficulty: "L2"
category: "ai-agent"
subcategory: "多智能体系统"
tags:
  - "IO"
feynman:
  essence: "**分层：** 单元(单 Agent I/O)、集成(两两交互)、端到端(任务成功率);辅以 LLM-as- judge 需防偏,最好配 黄金集与人审. fro"
  analogy: "多 Agent 协作就像项目团队——每个 Agent 扮演不同角色（PM/开发/测试），通过消息传递协作，Boss-Worker 是中心调度，Pipeline 是流水线接力。"
  key_points:
    - "**分层：** 单元(单 Agent I/O)、集成(两两交互)、端到端(任务成功率)"
    - "辅以 LLM-as- judge 需防偏,最好配 黄金集与人审. from typing import Callable, Any, Set, List def run_with_guard(agen"
    - "abort\") seen.add(h) transcript.append(action) if \"DONE\" in action: return transcript raise RuntimeEr"
first_principle:
  problem: "为什么需要 多 Agent 的评估怎么做？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "模型本质是数学函数的参数优化——所有能力都来自数据和参数"
    - "质量 > 数量：数据质量决定模型上限，算法决定达到上限的效率"
  rebuild: "从 AI 系统出发：① 核心挑战是什么？② 现有方案如何解决？③ 有哪些 trade-off？④ 如果重新设计你会怎么做？"
---

# 多 Agent 的评估怎么做

**分层：** 单元(单 Agent I/O)、集成(两两交互)、端到端(任务成功率);辅以 LLM-as-
judge 需防偏,最好配 黄金集与人审.
from typing import Callable, Any, Set, List
def run_with_guard(agent_step: Callable[[List[str]], str], user_goal: str,
**max_steps：** int = 20):
**transcript：** List[str] = []
**seen：** Set[str] = set()
for _ in range(max_steps):
action = agent_step(transcript + [f"GOAL: {user_goal}"])
h = action.strip()
if h in seen:
raise RuntimeError("detected repeated action; abort")
seen.add(h)
transcript.append(action)
if "DONE" in action:
return transcript
raise RuntimeError("max steps exceeded")
python
