---
id: "ai-scen-014"
difficulty: "L3"
category: "ai-scenario"
subcategory: "AI Agent系统设计"
tags:
  - "错误恢复"
  - "重试机制"
  - "Checkpoint"
  - "降级策略"
  - "Agent健壮性"
  - "异常处理"
feynman:
  essence: "【场景分析】 Agent失败类型多样：工具调用失败、LLM输出格式错误、上下文超限、逻辑死循环、外部服务不可用。"
  analogy: "AI Agent 就像有自主行动能力的实习生——能理解任务、拆解步骤、使用工具、根据反馈调整。"
  key_points:
    - "瞬态错误（Transient）："
    - "网络超时、API限流、临时不可用"
    - "策略：指数退避重试（3次，间隔1s/2s/4s）"
first_principle:
  problem: "如果要解决这个问题，最本质的方法论是什么？先理解问题约束，再找最优路径。"
  axioms:
    - "模型本质是数学函数的参数优化——所有能力都来自数据和参数"
    - "质量 > 数量：数据质量决定模型上限，算法决定达到上限的效率"
  rebuild: "从 AI 系统出发：① 核心挑战是什么？② 现有方案如何解决？③ 有哪些 trade-off？④ 如果重新设计你会怎么做？"
follow_up:
  - "如何设计Agent的Checkpoint频率？"
  - "Agent死循环检测有哪些实用算法？"
  - "如何在不影响用户体验的情况下实现降级？"
---

# 如何设计AI Agent的错误恢复机制？当Agent执行任务中途失败时，如何优雅地处理和恢复。

【场景分析】
Agent失败类型多样：工具调用失败、LLM输出格式错误、上下文超限、逻辑死循环、外部服务不可用。健壮的Agent必须有完善的错误恢复策略。

【错误分类与恢复策略】
1. 瞬态错误（Transient）：
   - 网络超时、API限流、临时不可用
   - 策略：指数退避重试（3次，间隔1s/2s/4s）
   - 超过重试次数 → 降级到备用方案
2. 工具调用失败：
   - 参数错误：LLM重新生成参数 → 重试
   - 权限不足：跳过该步骤，记录告警
   - 工具不可用：切换到替代工具或返回部分结果
3. LLM输出异常：
   - 格式错误：JSON解析失败 → 重试 + 格式约束Prompt
   - 空回复/拒绝回答：重试或切换模型
   - 幻觉输出：后处理校验 + 重新生成
4. 逻辑错误：
   - 死循环：检测重复动作序列 → 强制跳出
   - 无进展：连续N步无状态变化 → 触发重规划
   - 上下文爆炸：Token超限 → 上下文压缩/摘要

【恢复框架设计】
- execute_step(): try-catch包裹每步执行
- TransientError → retry(max_attempts=3, exponential backoff)
- ValidationError → regenerate(修正参数)
- CriticalError → escalate(升级处理)
- fallback(): 所有恢复失败时的兜底策略

【状态检查点（Checkpoint）】
- 定期保存Agent执行状态（每步或每N步）
- 失败后从最近的Checkpoint恢复，而非从头开始
- 实现：Redis / PostgreSQL存储中间状态

【降级策略】
- L1 降级：大模型 → 小模型（更快但可能质量降低）
- L2 降级：Agent模式 → 简单检索+模板回答
- L3 降级：自动 → 人工转接

【可观测性】
- 错误分类统计：按类型、频率、影响范围
- Trace记录：完整执行链路，便于事后分析
- 告警：错误率突增 → 自动告警
