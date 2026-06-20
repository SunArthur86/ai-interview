---
id: ai-scen-009
difficulty: L3
category: ai-scenario
subcategory: AI Agent系统设计
tags:
- 多Agent
- Agent协作
- 任务编排
- LangGraph
- CrewAI
- DAG
feynman:
  essence: 通过角色分工和协作机制，让多个AI Agent像团队一样协同完成复杂任务。
  analogy: 像公司项目组，有PM分配任务，有程序员写代码，有测试找Bug，最后大家一起交付。
  first_principle: 如何让多个独立智能体高效协作，共同解决单一智能体无法完成的复杂问题？
  key_points:
  - 明确角色分工，编排者负责任务分解与分发。
  - 采用黑板或消息传递模式处理通信。
  - 使用DAG图管理任务依赖和并行执行。
  - 设置超时和最大轮次防止死循环。
follow_up:
- 多Agent之间的上下文如何高效共享而不爆炸？
- 如果某个Agent给出错误结果，如何防止错误传播？
- 如何评测多Agent系统的端到端效果？
---

# 如何设计一个多Agent协作系统？例如多个AI Agent协同完成一个复杂的数据分析报告。

【场景分析】
多Agent协作核心挑战：任务分解、Agent间通信、结果聚合、错误传播控制、死锁检测。

【架构设计】
1. Agent角色定义：
   - Orchestrator（编排者）：接收任务 → 分解子任务 → 分配 → 聚合结果
   - Researcher（研究员）：收集数据、查询数据库、调用API
   - Analyst（分析师）：数据清洗、统计分析、生成图表
   - Writer（撰写者）：整合分析结果、撰写报告
   - Reviewer（审核者）：质量检查、事实核查
2. 通信模式：
   - 共享黑板：Agent读写共享状态空间（适合解耦，但可能产生竞争）
   - 消息传递：Agent间直接通信（如点对点，适合明确流程）
   - 事件驱动：任务完成事件触发下一步（适合异步松耦合）
3. 任务编排：
   - DAG任务图：任务依赖关系建模
   - 串行/并行混合：独立任务并行，有依赖的串行
   - 动态分配：根据Agent能力和负载动态调度

【多Agent协作状态流转图】
┌──────────────┐
│   User Query │
└──────┬───────┘
       ▼
┌──────────────┐     1. Plan      ┌───────────────────┐
│Orchestrator  ├─────────────────>│ Task Graph (DAG)  │
│  (Manager)   │                  │ [Task A, B, C...] │
└──────┬───────┘                  └─────────┬─────────┘
       │                                    │
       │ 2. Dispatch                        │ 3. Execute
       ▼                                    ▼
┌──────────────┐                   ┌──────────────────┐
│ Message Queue│<──────────────────│ Agent A / B / C  │
│  (Event Bus) │    Publish Event  │ (Workers)        │
└──────┬───────┘                   └────────┬─────────┘
       │                                    │
       │ 4. Result                          │ 5. Feedback
       ▼                                    ▼
┌──────────────┐                   ┌──────────────────┐
│ Shared State │<──────────────────│ Orchestrator     │
│ (Blackboard) │    Update State   │ (Monitor/Sync)   │
└──────────────┘                   └──────────────────┘

【协作流程示例（数据分析报告）】
用户请求 → Orchestrator分解为[收集数据, 清洗分析, 可视化, 撰写报告]
→ Researcher并行收集多源数据 → Analyst清洗+分析
→ Writer整合 → Reviewer审核 → Orchestrator返回

【关键设计决策】
- Agent数量：3-7个为宜，过多增加协调开销和通信噪音
- 上下文共享：完整共享 vs 摘要传递（避免上下文爆炸，通常传递摘要和引用ID）
- 错误隔离：单个Agent失败不阻塞全局，降级处理（如Analyst失败，Writer基于草稿撰写）
- 超时控制：每个Agent步骤设定最大执行时间，防死锁

【防止死循环】
- 最大轮次限制：max_iterations=10
- 状态追踪：检测重复动作序列（如A->B->A->B）
- 人工介入：连续失败3次或置信度低时自动升级到人工

【技术选型】
- 框架：LangGraph（有状态多Agent，支持循环）/ CrewAI（基于角色的）/ AutoGen（对话式）/ Microsoft Semantic Kernel
- 通信：Redis Pub-Sub / RabbitMQ / Kafka
- 状态管理：集中式状态存储（PostgreSQL/Redis）

## 常见考点
1. **多Agent与单Agent+Tools的区别**：什么情况下必须用多Agent？（答：任务跨度大、需要不同领域专家角色、需要并行处理且逻辑复杂时）
2. **如何解决Agent间上下文爆炸问题**？（答：不传递完整历史，只传递Observation摘要；使用引用机制，让Agent自己去读取共享存储中的详细数据）
3. **状态一致性管理**：如果Agent B 依赖 Agent A 的结果，但 A 失败了，编排器如何处理？（答：DAG中定义重试策略，若重试失败则标记整个分支失败，Orchestrator根据策略决定跳过或中止）
4. **通信机制选型**：共享黑板vs消息队列的优缺点？（答：黑板实现简单，适合状态共享；MQ更适合解耦和异步，但实现复杂度高）
