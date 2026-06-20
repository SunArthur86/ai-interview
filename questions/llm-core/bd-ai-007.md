---
id: bd-ai-007
difficulty: L4
category: llm-core
categories:
- ai-agent
- eng-practice
- llm-core
subcategory: Agent核心框架
tags:
- 字节
- 面经
- 多Agent
- 通信
- 异常处理
feynman:
  essence: 星型架构解耦通信，四层防线（超时、重试、降级、校验）保障鲁棒性。
  analogy: 像公司架构：老板（主）给员工（子）派活，不干就换人，干完要质检。
  first_principle: 如何协调多个独立智能体可靠地完成复杂任务？
  key_points:
  - 推荐Hub-Spoke星型架构
  - 消息结构化确保可追踪
  - 超时重试降级校验四层防错
  - 状态持久化支持断点续传
  - 关键操作保留人工介入口
follow_up:
- 子Agent之间能直接通信吗？——可以但不推荐，容易循环依赖
- 多Agent如何做负载均衡？——按子Agent队列深度路由，空闲的优先
- 如何防止子Agent无限循环？——最大循环次数 + 超时 + 活跃度检测
---

# 【字节面经】多Agent架构下，主Agent和子Agent的通信链路怎么设计？异常如何处理？

**多Agent通信架构设计：**

常见三种模式：
1. **星型（Hub-Spoke）** — 主Agent协调，子Agent各司其职。推荐：解耦清晰、出问题好排查
2. **链式（Pipeline）** — Agent1→Agent2→Agent3，每步验证。适合线性流水线
3. **网状（Mesh）** — Agent之间直接通信。灵活但复杂，容易循环依赖

**推荐星型架构的设计要点：**
- 主Agent负责任务分解、路由、结果聚合
- 子Agent之间不直接通信，通过主Agent中转
- 采用结构化消息格式（msg_id/from/to/type/content/context_ref）

**异常处理四层防线：**
1. **超时机制** — 子Agent执行太久就kill掉，返回兜底结果
2. **重试策略** — 错误时换方式重试或换子Agent，但有最大重试次数
3. **降级方案** — 某个子Agent挂了，主Agent用更简单方式完成（如搜索Agent挂了用本地知识库）
4. **结果校验** — 子Agent输出不直接信任，主Agent校验格式和内容（如代码能不能编译）

**工程实现关键点：**
- 状态持久化：每步结果存DB/Redis，崩溃可恢复
- Checkpoint机制：关键步骤后存检查点，可回滚
- 人工介入点：高风险操作（删数据/发邮件）需确认
