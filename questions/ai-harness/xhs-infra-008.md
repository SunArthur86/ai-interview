---
id: xhs-infra-008
difficulty: L4
category: ai-harness
subcategory: 推理与部署
tags:
- 系统设计
- Serving
- 推荐系统
- LLM
- 小红书
feynman:
  essence: 分级调度与弹性异构资源组合，平衡高并发与成本。
  analogy: 像餐厅运营，大厨（大模型）做难菜，帮厨（小模型）做快餐，合理排队。
  first_principle: 如何在保证低延迟和高吞吐的前提下，最小化推理服务成本？
  key_points:
  - 动态批处理（Continuous Batching）提升吞吐
  - 请求路由实现大小模型分级处理
  - 会话亲和性复用KV Cache降低延迟
  - 利用混合异构GPU和Spot实例降低成本
follow_up:
- 模型路由器如何决策用大模型还是小模型？
- KV Cache在多轮对话中如何管理？
- 推荐场景的冷启动如何用LLM优化？
---

# 设计一个支持百万QPS的大模型Serving系统（结合推荐场景）。如何做负载均衡和成本优化？

## 整体架构
请求 → API Gateway → 负载均衡 → GPU推理集群 → 结果聚合 → 返回

## 核心组件

### 1. 负载均衡
- **L7 LB**：按请求类型/长度路由
- **模型路由器**：简单请求→小模型，复杂请求→大模型
- **会话亲和**：相同用户路由到同一节点（KV Cache复用）

### 2. 批处理策略
- **动态批（Continuous Batching）**：vLLM
- **混合批**：推荐+生成请求混合调度
- **超时控制**：等待窗口（如50ms）平衡吞吐和延迟

### 3. 成本优化
- **GPU池异构**：A100（重模型）+ T4（轻模型）
- **Speculative Decoding**：减少大模型调用次数
- **量化**：INT8/FP8减少推理成本
- **KV Cache复用**：多轮对话/相似请求共享前缀
- **Spot实例 + 弹性扩缩容**

### 4. 推荐场景特化
- **召回→精排→LLM重排** 三级pipeline
- LLM用于：长尾query理解、多样性保证、用户意图分析
- 冷启动：LLM生成candidate，传统推荐精排

## 监控指标
- QPS / P99延迟 / GPU利用率 / 成本/千次请求
