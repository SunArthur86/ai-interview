---
id: "ai-scen-016"
difficulty: "L3"
category: "ai-scenario"
subcategory: "AI对话系统设计"
tags:
  - "ChatGPT"
  - "流式输出"
  - "多轮对话"
  - "Function Calling"
  - "模型网关"
  - "SSE"
feynman:
  essence: "【场景分析】 ChatGPT级对话系统的核心：低延迟流式输出、上下文管理、工具集成、安全过滤、高并发"
  analogy: "流式输出就像水龙头接水——不用等整桶水接满（全部生成），边接边用（逐字输出），体验更流畅。"
  key_points:
    - "WebSocket/SSE长连接，支持流式输出"
    - "负载均衡：Nginx + 一致性Hash（会话粘滞）"
    - "限流：每用户QPS限制 + 全局并发限制"
first_principle:
  problem: "如果要解决这个问题，最本质的方法论是什么？先理解问题约束，再找最优路径。"
  axioms:
    - "模型本质是数学函数的参数优化——所有能力都来自数据和参数"
    - "质量 > 数量：数据质量决定模型上限，算法决定达到上限的效率"
  rebuild: "从 AI 系统出发：① 核心挑战是什么？② 现有方案如何解决？③ 有哪些 trade-off？④ 如果重新设计你会怎么做？"
follow_up:
  - "如何实现首Token延迟<500ms？"
  - "多轮对话的上下文压缩策略有哪些？"
  - "如何设计模型路由策略降低成本？"
---

# 如何设计一个类似ChatGPT的对话系统？支持流式输出、多轮对话、插件调用。

【场景分析】
ChatGPT级对话系统的核心：低延迟流式输出、上下文管理、工具集成、安全过滤、高并发。

【整体架构】
1. 接入层：
   - WebSocket/SSE长连接，支持流式输出
   - 负载均衡：Nginx + 一致性Hash（会话粘滞）
   - 限流：每用户QPS限制 + 全局并发限制
2. 对话管理层：
   - 上下文窗口管理：滑动窗口 + 历史摘要
   - Token预算：系统Prompt + 历史 + 当前消息 + 预留输出空间
   - 多轮压缩：超出窗口时用小模型总结早期对话
3. 模型推理层：
   - 模型网关：路由不同模型（GPT-4/Claude/开源）
   - vLLM/TGI推理引擎：PagedAttention + Continuous Batching
   - 流式生成：逐Token推送到前端
4. 插件/工具层：
   - Function Calling：LLM决定何时调用工具
   - 工具注册中心：插件发现、权限管理
   - 异步执行：工具调用不阻塞流式输出
5. 安全层：
   - 输入过滤：Prompt注入检测、敏感词过滤
   - 输出审核：有害内容检测、PII脱敏
   - 用量控制：Token配额、费用归因

【流式输出优化】
- TTFT（Time To First Token）< 500ms
- 逐Token SSE推送，前端逐字渲染
- 推理中断：用户停止生成时立即取消推理
- KV Cache复用：多轮对话前缀复用

【多轮对话上下文管理】
上下文结构：[System Prompt(固定)] + [Summary of earlier turns(动态压缩)] + [Recent N turns(完整保留)] + [Current user message] + [预留output token空间]

【高并发设计】
- 水平扩展：无状态API节点 + Redis存会话
- 推理集群：GPU节点动态扩缩容
- 队列缓冲：高峰期请求排队，避免OOM
- 成本控制：模型路由（简单→小模型，复杂→大模型）
