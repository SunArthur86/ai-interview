---
id: agmu-017
difficulty: L2
category: ai-agent
subcategory: 多智能体系统
tags:
- IO
feynman:
  essence: 分层评估结合人工黄金集，避免模型评估偏差。
  analogy: 像考核员工，既要考试（单元），也要看项目成果（端到端）。
  first_principle: 如何全方位量化多智能体系统的性能表现？
  key_points:
  - 单元：单Agent输入输出
  - 集成：交互逻辑测试
  - 端到端：整体任务成功率
  - 防偏：LLM-as-judge需黄金集校准
---

# 多 Agent 的评估怎么做

**分层**：单元（单 Agent I/O）、集成（两两交互）、端到端（任务成功率）；辅以 LLM-as-judge 需防偏，最好配黄金集与人审。

```python
from typing import Callable, Any, Set, List

def run_with_guard(agent_step: Callable[[List[str]], str], user_goal: str, max_steps: int = 20):
    transcript: List[str] = []
    seen: Set[str] = set()
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
```
