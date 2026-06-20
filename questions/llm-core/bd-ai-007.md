---
id: "bd-ai-007"
difficulty: "L4"
category: "llm-core"
categories:
  - "ai-agent"
  - "eng-practice"
  - "llm-core"
subcategory: "Agent核心框架"
tags:
  - "字节"
  - "面经"
  - "多Agent"
  - "通信"
  - "异常处理"
feynman:
  essence: "多Agent通信 = 主Agent做项目经理（分解任务、分配、验收），子Agent做专业员工（各干各的），通过结构化消息和四层异常防线保证系统稳定。"
  analogy: "主Agent像餐厅经理——接订单后分配给厨师（做菜）、服务员（上菜）、收银员（结账）。某个厨师请假了，经理自己顶上或换人。出菜前经理要检查质量。"
  key_points:
    - "星型架构推荐：主Agent协调"
    - "四层异常：超时+重试+降级+校验"
    - "状态持久化+Checkpoint"
    - "高风险操作需人工确认"
first_principle:
  problem: "单个Agent能力有限，多Agent协作可处理复杂任务。但多Agent引入了通信复杂性、异常传染、状态一致性等挑战。"
  axioms:
    - "解耦是关键——子Agent不直接通信"
    - "异常是常态——必须有多层防线"
    - "结果不可信——主Agent必须校验"
  rebuild: "从协作效率出发：怎么分解任务（主Agent规划）？怎么分配（路由到子Agent）？怎么保证可靠（超时+重试+降级+校验）？怎么保证一致（状态持久化+Checkpoint）？"
follow_up:
  - "子Agent之间能直接通信吗？——可以但不推荐，容易循环依赖"
  - "多Agent如何做负载均衡？——按子Agent队列深度路由，空闲的优先"
  - "如何防止子Agent无限循环？——最大循环次数 + 超时 + 活跃度检测"
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
