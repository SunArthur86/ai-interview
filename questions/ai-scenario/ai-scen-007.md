---
id: ai-scen-007
difficulty: L2
category: ai-scenario
subcategory: RAG系统设计
tags:
- RAG评测
- RAGAS
- Golden Set
- Faithfulness
- 检索指标
- LLM-as-Judge
feynman:
  essence: 构建检索、生成、端到端三层指标体系，驱动系统持续迭代。
  analogy: 像体检，要查血液（检索）、心脏（生成）和整体机能（端到端），综合判断健康。
  first_principle: 如何科学量化RAG系统各个环节的表现，确保迭代方向正确？
  key_points:
  - 检索层：Recall@K、MRR 衡量召回能力
  - 生成层：Faithfulness、Relevancy 衡量质量
  - 端到端：LLM-as-Judge + 用户反馈
  - CI集成：Golden Set回归阻断劣质发布
follow_up:
- LLM-as-Judge有哪些偏差？如何校准？
- 如何自动构建高质量的评测集？
- 检索指标和生成指标冲突时如何取舍？
---

# 如何为RAG系统设计完整的评测体系？包括检索质量评测和生成质量评测。

【场景分析】
RAG评测最大痛点：没有统一标准，难以量化迭代效果。需要分层评测——检索层、生成层、端到端。

【三层评测架构】
1. 检索质量评测（Retrieval Metrics）：
   - Recall@K：相关文档是否在Top-K中（最关键）
     - MRR（Mean Reciprocal Rank）：第一个相关文档的排名倒数
   - NDCG@K：考虑排序质量的加权指标
   - 评测集构建：人工标注（query → 相关doc列表）
   - 自动化：用强LLM判断doc是否与query相关
2. 生成质量评测（Generation Metrics）：
   - Faithfulness（忠实度）：回答是否完全基于检索文档（反幻觉）
   - Answer Relevancy（答案相关性）：回答是否切题
   - Context Precision：检索到的上下文中有用信息占比
   - Context Recall：回答所需信息是否都在上下文中
   - 工具：RAGAS框架自动计算以上指标
3. 端到端评测（E2E Metrics）：
   - 人工评分：1-5分（相关性、准确性、完整性、流畅性）
   - LLM-as-Judge：GPT-4作为评审打分
   - 用户反馈：点赞/点踩 + 文字反馈
   - 任务完成率：对于对话型系统，用户是否得到满意答案

【Golden Set构建】
- 规模：200~500条标注样本
- 覆盖：常见问题60% + 边缘场景25% + 对抗样本15%
- 标注内容：query, 期望答案, 相关文档ID, 难度等级
- 持续维护：线上bad case回流 → 补充Golden Set

【CI/CD集成】
- 每次Prompt/模型/检索参数变更 → 跑Golden Set回归
- 设定阈值：Faithfulness > 0.85，Recall@5 > 0.80
- 不达标则阻断发布
- 成本控制：Core Set（50条）每次CI跑，Full Set发布前跑
