---
id: ai-scen-034
difficulty: L3
category: ai-scenario
subcategory: AI评测与监控
tags:
- 可观测性
- OpenTelemetry
- Trace追踪
- Grafana
- 质量看板
- 告警体系
feynman:
  essence: 监控基建、模型行为和业务质量，全链路洞察系统健康度。
  analogy: 不仅看服务器有没有挂，还要看AI是不是在胡说八道，以及用户满不满意。
  first_principle: 如何透过黑盒模型，全面感知系统的实时状态和用户体验？
  key_points:
  - 三层监控：基础设施+模型行为+业务质量
  - 全链路：用OpenTelemetry追踪每一步耗时
  - 分级告警：P0到P3区分故障和体验下降
  - 质量看板：实时展示核心指标和Bad Case
follow_up:
- 如何平衡Trace详细程度和存储成本？
- 模型行为监控与基础设施监控如何整合？
- 如何设计有效的Bad Case分析流程？
---

# 如何设计AI系统的可观测性方案？监控模型行为、输出质量和用户体验。

【场景分析】
AI系统可观测性比传统系统更复杂：不仅要监控基础设施，还要监控模型行为、输出质量、成本。

**实战案例**：某次线上故障中，虽然P99延迟显示正常，但“工具调用成功率”指标突然下跌。排查发现是Rerank服务异常导致检索结果为空，LLM频繁尝试调用不存在的工具。业务指标比延迟指标更早暴露了问题。

【三层可观测性】
1. 基础设施层：
   - GPU利用率、显存占用、温度
   - 请求QPS、延迟分布（P50/P95/P99）
   - 错误率、重试率、熔断次数
   - 工具：Prometheus + Grafana
2. 模型行为层：
   - Token消耗趋势（按模型/功能/租户）
   - 拒答率：模型拒绝回答的比例
   - 幻觉率：基于Golden Set的实时监控
   - 安全拦截率：有害内容触发拦截的比例
   - 工具调用成功率：Function Calling的成功/失败
3. 业务质量层：
   - 用户满意度：点赞率/点踩率/评分
   - 任务完成率：对话是否达到用户目标
   - 人工转接率：AI无法处理转人工的比例
   - 用户留存：AI体验对留存的影响

**代码示例（Python：Prometheus Metrics记录业务指标）**
```python
from prometheus_client import Counter, Histogram

# 定义指标
llm_tokens_total = Counter('llm_tokens_consumed_total', 'Total tokens consumed', ['model', 'tenant'])
user_feedback = Counter('user_feedback_total', 'User feedback count', ['type']) # type: like/dislike

# 在代码中埋点
def log_llm_usage(model, tenant, input_tokens, output_tokens):
    llm_tokens_total.labels(model=model, tenant=tenant).inc(input_tokens + output_tokens)

def log_user_action(action_type):
    user_feedback.labels(type=action_type).inc()
```

【Trace全链路追踪】
OpenTelemetry标准，一次请求的完整Trace：
用户请求 → API网关(5ms) → 鉴权(2ms) → Query改写(50ms)
→ 向量检索(15ms) → 关键词检索(8ms) → Rerank(30ms)
→ Prompt组装(5ms) → LLM推理(800ms) → 输出校验(10ms) → 返回
每个Span记录：耗时、输入、输出、状态码、Token数

【告警体系】
| 级别 | 指标 | 阈值 | 动作 |
| P0 | 服务不可用 | 错误率>10% | 电话告警 |
| P1 | 延迟恶化 | P99>5s | 飞书告警 |
| P2 | 质量下降 | 差评率>15% | 邮件告警 |
| P3 | 成本异常 | 日消耗>预算120% | 仪表盘标记 |

【质量看板】
- 实时大屏：QPS、延迟、错误率、满意度
- 趋势分析：日/周/月维度的质量变化趋势
- 对比分析：不同模型/Prompt版本的效果对比
- Bad Case分析：差评案例的分类统计和根因分析

**对比表格：传统监控 vs AI可观测性**

| 维度 | 传统监控 (APM) | AI可观测性 (LLMOps) |
| :--- | :--- | :--- |
| **核心指标** | QPS, Latency, Error, CPU/Mem | Token/成本, 幻觉率, 拒答率, 引用准确度 |
| **数据类型** | 结构化日志、数值型 | 非结构化文本、概率分布、Embedding向量 |
| **故障排查** | 查看Error Stack Trace | 分析Prompt上下文、检索相关性、模型推理逻辑 |
| **成本归因** | 计算资源成本 | 模型推理成本 (Token计费) + 检索成本 |
| **质量评价** | 服务可用性 (SLA) | 答案正确性、安全性、有用性 |

## 常见考点
1. **非结构化数据的监控难点**：如何量化监控“幻觉率”或“逻辑错误”？
   *答案要点*：无法直接通过日志指标监控。通常采用“抽检机制”或“离线评测回溯”。在线上通过设定规则（如事实性校验、引用完整性）作为代理指标；或者使用轻量级Judge模型实时流式抽样打分。
2. **Trace ID透传**：在微服务架构中，如何保证从网关到LLM调用的全链路Trace ID一致？
   *答案要点*：遵循OpenTelemetry标准，在HTTP Headers（如`traceparent`）中传递Trace ID。在异步调用（如消息队列）或工具调用时，需手动将Trace Context写入消息体或Metadata中，确保断链也能追踪。
3. **成本监控的精细化**：如何区分不同租户或不同功能的Token消耗？
   *答案要点*：在写入Metric时打上丰富的Tag（Labels），如`tenant_id`, `feature`, `model_name`。注意控制Cardinality（基数）数量，防止将`user_id`这种高基数标签直接带入Prometheus，可能导致内存溢出，可先聚合存入OLAP数据库（如ClickHouse）进行成本分析。
