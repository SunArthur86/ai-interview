---
id: "eng-practice-s005"
difficulty: "L3"
category: "eng-practice"
subcategory: "工程化实战"
images:
  - "svg_rag.svg"
feynman:
  essence: "生产级 LLM 应用架构通常分层：API Gateway（路由/限流/认证）→ LLM 服务层（模型路由、多供应商 failover、缓存）→ 编排层（RAG/Agent/工具调用）→ 可观测性层（日志/指标/链路追踪），核心是把「调用模型」包装成可治理、可灰度、可降级的服务。"
  analogy: "大语言模型就像读过整个互联网的学者——通过预测「下一个词」生成文本，积累了海量语言模式和知识。"
  key_points:
    - "API Gateway："
    - "模型路由（大/小模型分流）"
    - "多供应商failover"
first_principle:
  problem: "如果要解决这个问题，最本质的方法论是什么？先理解问题约束，再找最优路径。"
  axioms:
    - "模型本质是数学函数的参数优化——所有能力都来自数据和参数"
    - "质量 > 数量：数据质量决定模型上限，算法决定达到上限的效率"
  rebuild: "从 AI 系统出发：① 核心挑战是什么？② 现有方案如何解决？③ 有哪些 trade-off？④ 如果重新设计你会怎么做？"
---

# 如何设计一个LLM应用的生产架构？

生产级LLM应用架构关键组件：

1. API Gateway：
- 请求路由（不同模型）
- 限流、认证
- 日志记录

2. LLM服务层：
- 模型路由（大/小模型分流）
- 重试机制（指数退避）
- 超时控制
- 多供应商failover

3. RAG管道：
- 文档处理（离线）
- 向量检索（在线）
- Reranking

4. 缓存层：
- 语义缓存（Redis + embedding）
- KV Cache（推理层）

5. 监控告警：
- Token用量监控
- 延迟监控（P50/P99）
- 质量监控（LLM-as-Judge）
- 成本告警

6. 安全：
- 输入过滤（Prompt Injection防护）
- 输出过滤（有害内容）
- PII脱敏

7. CI/CD：
- Prompt版本管理
- A/B测试
- 灰度发布
