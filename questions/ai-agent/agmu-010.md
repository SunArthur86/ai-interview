---
id: "agmu-010"
difficulty: "L1"
category: "ai-agent"
subcategory: "多智能体系统"
feynman:
  essence: "AutoGen 偏 对话与多角色交互 的快速组合;LangGraph 偏 显式图状态机 与 检查点/分 支.若强调 生产可恢复与审计,LangGraph 往往更"
  analogy: "LangGraph 就像状态机工厂——用图（Graph）定义 Agent 的流转逻辑，节点是处理步骤，边是条件跳转，状态在节点间传递。"
  key_points:
    - "AutoGen 偏 对话与多角色交互 的快速组合"
    - "LangGraph 偏 显式图状态机 与 检查点/分 支.若强调 生产可恢复与审计,LangGraph 往往更易 形式化"
    - "若强调 探索式对话与人机混合, AutoGen 叙事更自然. - *追问应对:**若问「能混用吗?」--答:可以,例如 LangGraph 节点内嵌 AutoGen 会话, 但要 统一 trace i"
first_principle:
  problem: "它们本质上为什么不同？各自的设计目标和适用场景是什么？"
  axioms:
    - "模型本质是数学函数的参数优化——所有能力都来自数据和参数"
    - "质量 > 数量：数据质量决定模型上限，算法决定达到上限的效率"
  rebuild: "从 AI 系统出发：① 核心挑战是什么？② 现有方案如何解决？③ 有哪些 trade-off？④ 如果重新设计你会怎么做？"
---

# AutoGen 和 LangGraph 多 Agent 有什么气质差异

AutoGen 偏 对话与多角色交互 的快速组合;LangGraph 偏 显式图状态机 与 检查点/分
支.若强调 生产可恢复与审计,LangGraph 往往更易 形式化;若强调 探索式对话与人机混合,
AutoGen 叙事更自然.
- **追问应对:**若问「能混用吗?」--答:可以,例如 LangGraph 节点内嵌 AutoGen 会话,
但要 统一 trace id 与成本核算.
