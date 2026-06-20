---
id: agmu-010
difficulty: L1
category: ai-agent
subcategory: 多智能体系统
feynman:
  essence: AutoGen 重对话流，LangGraph 重状态流转。
  analogy: AutoGen 像聊天群组，LangGraph 像工作流引擎。
  first_principle: 如何选择适合交互逻辑与工程控制的抽象框架？
  key_points:
  - AutoGen：多角色对话，快速组合
  - LangGraph：状态机，易审计
  - 侧重：AutoGen偏探索，LangGraph偏生产
  - 混用：节点嵌套，统一追踪
---

# AutoGen 和 LangGraph 多 Agent 有什么气质差异

AutoGen 偏对话与多角色交互的快速组合；LangGraph 偏显式图状态机与检查点/分支。

若强调生产可恢复与审计，LangGraph 往往更易形式化；若强调探索式对话与人机混合，AutoGen 叙事更自然。

**追问应对**：若问「能混用吗？」——答：可以，例如 LangGraph 节点内嵌 AutoGen 会话，但要统一 trace id 与成本核算。
