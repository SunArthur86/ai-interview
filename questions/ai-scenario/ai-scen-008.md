---
id: ai-scen-008
difficulty: L3
category: ai-scenario
subcategory: RAG系统设计
tags:
- 增量索引
- 实时RAG
- CDC
- 时效性
- 缓存失效
- 双缓冲
feynman:
  essence: 基于CDC监听和增量Upsert机制，实现文档变更的秒级同步。
  analogy: 像即时通讯，发消息立刻推送，而不是等收信人手动刷新。
  first_principle: 如何在保障查询性能的同时，最小化数据从变更到可检索的时间延迟？
  key_points:
  - 变更检测：CDC或Webhook实时触发
  - 增量处理：仅计算和更新变动部分
  - 索引策略：Near Real-Time + Shadow切换
  - 缓存失效：文档变动自动清理相关缓存
follow_up:
- 如何处理高频小批量更新导致的索引碎片化？
- 如果向量库支持的事务较弱，如何保证一致性？
- 文档删除后，已生成的回答中的引用如何处理？
---

# 设计一个支持实时更新和增量索引的RAG系统。当知识库文档频繁变更时，如何保证检索结果的时效性？

【场景分析】
实时RAG的核心矛盾：索引更新需要时间，用户期望立即检索到最新内容。关键指标：索引延迟（文档更新到可检索的时间差）。

【增量索引架构】
1. 变更检测：
   - CDC（Change Data Capture）：监听数据库binlog或文件系统事件
   - Webhook：文档管理系统主动推送变更事件
   - 定时扫描+内容Hash比对：兜底方案
2. 增量处理Pipeline：
   - 变更事件 → Kafka → 并行Consumer
   - 仅处理变更部分：文档Diff → 变更chunk识别
   - 差异Embedding：只对变更chunk重新计算向量
   - 增量插入：Milvus upsert（删除旧向量+插入新向量）
3. 索引刷新策略：
   - Near Real-Time：向量库写入后立即可查（Milvus支持）
   - Soft Refresh：定期merge segment，优化查询性能
   - 双缓冲：新索引构建在影子集合 → 原子切换

【时效性保障】
- SLA：文档更新后30秒内可检索
- 监控：索引延迟P99 < 30s
- 补偿机制：若异步索引延迟，提供强制刷新API

【一致性挑战与方案】
- 删除延迟：软删除标记 → 后台清理 → 查询时过滤
- 部分更新：文档分chunk，仅更新变更chunk及其向量
- 并发冲突：乐观锁（版本号）处理并发更新

【缓存失效】
- 语义缓存：文档变更时，关联Query缓存自动失效
- 策略：按文档ID反查影响的缓存Key，精准失效
