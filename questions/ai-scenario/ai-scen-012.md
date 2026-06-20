---
id: ai-scen-012
difficulty: L3
category: ai-scenario
subcategory: AI Agent系统设计
tags:
- Agent规划
- ReAct
- Plan-and-Execute
- Tree of Thoughts
- 任务分解
- 推理引擎
feynman:
  essence: 将复杂任务拆解为可执行的步骤链，并在执行过程中根据反馈动态调整。
  analogy: 像写代码前先画流程图，遇到报错时回溯修改逻辑，而不是盲目执行。
  first_principle: 如何让AI将模糊的目标转化为可执行的、有条理的具体行动步骤？
  key_points:
  - 根据任务类型选择ReAct、计划-执行或思维树模式。
  - 利用DAG图管理子任务依赖和并行。
  - 执行失败时触发动态重规划，保留有效进度。
  - 限制分解深度，防止陷入无限递归。
follow_up:
- ReAct和Plan-and-Execute分别适合什么场景？
- 如何防止Agent陷入无限循环？
- 如何评估Agent的规划质量？
---

# 如何设计AI Agent的规划（Planning）与推理（Reasoning）引擎？让Agent能自主分解复杂任务。

【场景分析】
Agent规划能力是区分「聊天机器人」和「自主Agent」的关键。核心挑战：任务分解质量、计划可执行性、动态调整能力。

【规划模式分类】
1. ReAct（Reasoning + Acting）：
   - Thought → Action → Observation 循环
   - 每一步先推理再行动，根据观察结果调整
   - 适用：探索性任务、工具调用密集型
2. Plan-and-Execute：
   - 先生成完整计划（Plan），再逐步执行（Execute）
   - 计划是结构化的步骤列表，每步有明确输入输出
   - 适用：流程明确的任务（数据分析、报告生成）
3. Tree of Thoughts（ToT）：
   - 生成多个候选思路 → 评估 → 选择最优路径
   - 支持回溯（backtracking）
   - 适用：需要创造性解决方案的任务
4. ReWOO（Reasoning WithOut Observation）：
   - 一次性生成所有推理步骤和工具调用
   - 减少LLM调用次数，降低成本和延迟
   - 适用：工具调用链固定的场景

【任务分解策略】
- 自顶向下：大任务 → 子任务 → 具体步骤
- 分解标准：每个子任务可独立完成、可验证
- 依赖建模：DAG图表示子任务间的依赖关系
- 并行识别：无依赖的子任务标记为可并行

【动态重规划】
- 触发条件：步骤执行失败、外部条件变化、用户中途修改需求
- 策略：保留已完成步骤 → 重新规划剩余部分
- 防抖：避免频繁重规划导致振荡

【实现要点】
- 计划表示：结构化JSON（steps数组，每步含action、params、expect）
- 步骤验证：每步执行后检查是否符合预期（LLM自评 + 规则检查）
- 最大深度：限制分解深度（max_depth=5），防止无限递归
- 超时：单步执行超时 → 跳过或降级

【评测维度】
- 任务完成率：端到端成功完成的比例
- 步骤效率：实际步骤数 / 最优步骤数
- 计划合理性：人类专家评分（1-5）
