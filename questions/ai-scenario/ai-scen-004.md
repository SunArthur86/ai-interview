---
id: ai-scen-004
difficulty: L3
category: ai-scenario
subcategory: RAG系统设计
tags:
- 大规模RAG
- 文档Pipeline
- Kafka
- 增量索引
- 批流一体
- 容量规划
feynman:
  essence: 异步解耦流水线结合批处理，实现高吞吐低延迟索引。
  analogy: 像流水线工厂，分工明确，各环节独立扩容，瓶颈在哪加哪里。
  first_principle: 如何在高吞吐写入压力下，保持系统低延迟响应和数据一致性？
  key_points:
  - 接入层：Kafka解耦，削峰填谷
  - 处理层：阶段解耦，独立扩缩容
  - 更新策略：软删除 + 最终一致
  - 读写分离：副本加速查询
follow_up:
- 如何处理超大文档（如500页PDF）的分块和索引？
- 向量库数据量到亿级时，检索性能如何保障？
- 如何实现文档的实时删除和权限回收？
---

# 如何设计大规模文档处理的RAG Pipeline？日均新增10万+文档，需要实时索引和低延迟查询。

【场景分析】
10万/日文档吞吐量 → ~1.2文档/秒平均，峰值可能10+/秒。核心挑战：索引速度、检索延迟、增量更新一致性。

【Pipeline架构】
1. 文档接入层：
   - Kafka消息队列：文档变更事件（create/update/delete）
   - Consumer集群：多worker并行处理
   - 幂等设计：文档ID + 内容hash去重
2. 文档处理Pipeline（批流一体）：
   - Stage 1 - 解析：PDF/Office/HTML → Markdown（unstructured-api）
   - Stage 2 - 分块：语义分块（spaCy句子边界 + 滑动窗口）
   - Stage 3 - 向量化：批量Embedding（GPU推理，batch=64）
   - Stage 4 - 入库：Milvus批量插入 + ES同步
   - 每个Stage通过消息队列解耦，独立扩缩容
3. 增量更新策略：
   - 软删除：标记旧chunk为deleted，不立即物理删除
   - 版本管理：保留文档多版本向量，支持时间旅行查询
   - 最终一致：索引更新延迟<30秒
4. 查询层优化：
   - 读写分离：查询走只读副本
   - 向量量化：IVF-PQ降低内存，保持Top-K召回率
   - 热点缓存：Redis缓存高频Query的检索结果

【容量规划】
- 存储：百万文档 × ~10 chunks/doc × 1536维 × 4字节 ≈ 60GB向量
- Embedding计算：10万文档/日 → GPU推理集群（A10×4）
- 查询QPS：假设1000 QPS → Milvus集群3节点足够

【监控告警】
- 索引延迟监控：P99 < 30s
- 处理失败率：< 0.1%
- 死信队列：失败文档人工介入
