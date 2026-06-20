---
id: misc-031
difficulty: L2
category: ai-basics
subcategory: RAG与向量检索
tags:
- IO
- IOC
- 索引
- Elasticsearch
feynman:
  essence: 利用LLM作为裁判，自动量化检索和生成的质量。
  analogy: 像老师批改作业，不只看答案对不对，还要检查是不是抄的书（来源）以及有没有跑题。
  first_principle: 在没有人工标注标准答案的情况下，如何科学、自动化地衡量RAG系统的好坏？
  key_points:
  - 检索看精准率和召回率
  - 生成看忠实度和相关性
  - Ragas利用LLM实现自动化评估
follow_up:
- 如何减少RAG的幻觉?
- Faithfulness如何自动计算?
---

# 如何评估RAG系统的质量?Ragas框架的核心指标有哪些

- **RAG评估维度:**

- **检索质量(Retrieval):**
- **Context Precision** - 检索到的文档中有多少是相关的
- **Context Recall** - 所有相关文档中有多少被检索到

- **生成质量(Generation):**
- **Faithfulness** - 答案是否忠于检索到的文档(无幻觉)
- **Answer Relevancy** - 答案是否回应了用户问题

- **Ragas框架:**
- 开源RAG评估工具
- 无需人工标注,用LLM自动评估
- 支持 grounding(忠实度) / relevance(相关性) / recall(召回)

- **评估流程架构:**

```text
Question + Ground Truth (Optional)
      │
      ▼
┌──────────────────┐
│   RAG System     │
└────┬────────┬─────┘
     │        │
     ▼        ▼
Context   Answer
     │        │
     ▼        ▼
┌─────────────────────────┐
│   LLM-as-a-Judge        │
│ (Ragas Evaluation)      │
└────────┬────────────────┘
         │
         ▼
   Metrics Scores
```

- **其他评估工具:** TruLens、LlamaIndex Evaluation、LangSmith

## 常见考点
1. **Context Recall 和 Context Precision 的计算逻辑是什么？**
   - **Precision** = 检索到的文档中，被标注为相关的比例（不查错）。
   - **Recall** = 标注为相关的文档中，被成功检索到的比例（不漏查）。

2. **Faithfulness 和 Answer Relevancy 评分的原理？**
   - **Faithfulness**: 将答案拆解为多个陈述，让 LLM 判断每个陈述是否能在 Context 中找到依据。
   - **Answer Relevancy**: 基于生成的答案反向生成一个问题，计算该问题与原问题的 Embedding 相似度。

3. **Ragas 评估的缺点是什么？**
   - 评估本身依赖于 LLM（LLM-as-a-Judge），因此不仅成本高，而且评估结果可能受到 Judge 模型偏见的影响，且速度较慢，不适合实时监控。
