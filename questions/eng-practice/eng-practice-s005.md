---
id: eng-practice-s005
difficulty: L3
category: eng-practice
subcategory: 工程化实战
images:
- svg_rag.svg
feynman:
  essence: 构建高可用、低延迟且安全的AI服务基础设施。
  analogy: 像装修队：门口有接待，中间有施工队，旁边有材料库，还有监工。
  first_principle: 如何稳定、高效、低成本地将模型能力转化为服务？
  key_points:
  - 网关负责流量控制与路由分发
  - RAG与缓存层保障响应速度与质量
  - 全链路监控与安全是生产底线
  - 多供应商Failover确保服务高可用
---

# 如何设计一个LLM应用的生产架构？

生产级LLM应用架构关键组件：

1. **API Gateway**
- 请求路由（不同模型）
- 限流、认证
- 日志记录

2. **LLM服务层**
- 模型路由（大/小模型分流）
- 重试机制（指数退避）
- 超时控制
- 多供应商failover

3. **RAG管道**
- 文档处理（离线）
- 向量检索（在线）
- Reranking

4. **缓存层**
- 语义缓存（Redis + embedding）
- KV Cache（推理层）

5. **监控告警**
- Token用量监控
- 延迟监控（P50/P99）
- 质量监控（LLM-as-Judge）
- 成本告警

6. **安全**
- 输入过滤（Prompt Injection防护）
- 输出过滤（有害内容）
- PII脱敏

7. **CI/CD**
- Prompt版本管理
- A/B测试
- 灰度发布
