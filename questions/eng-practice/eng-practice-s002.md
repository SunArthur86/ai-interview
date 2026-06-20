---
id: eng-practice-s002
difficulty: L2
category: eng-practice
subcategory: 工程化实战
feynman:
  essence: 建立多维度体系判断模型表现是否满足业务需求。
  analogy: 像体检，既要做常规检查（基准测试），也要看主观感受（人工评估），还要关注日常工作状态（在线指标）。
  first_principle: 如何全面、客观地衡量一个复杂AI系统在实际应用中的真实效果？
  key_points:
  - 结合离线基准测试与在线业务指标
  - 利用LLM-as-Judge实现低成本自动评估
  - 针对RAG场景关注忠实度与上下文召回
  - 评估标准需与具体业务目标对齐
---

# 如何评估LLM应用的效果？

LLM应用评估是多维度的：

1. **基准测试**：
   - MMLU: 多任务理解
   - HumanEval: 代码生成
   - GSM8K: 数学推理
   - C-Eval/CMMLU: 中文评测

2. **自动评估**：
   - Exact Match / F1
   - BLEU / ROUGE（文本生成）
   - LLM-as-Judge: 用GPT-4评分
   - RAGAS: RAG专用评估（Faithfulness、Relevancy、Context Recall）

3. **人工评估**：
   - Elo Rating（人机对比）
   - Pairwise Comparison（两个回答比较）
   - 标注质量评估

4. **在线指标**：
   - 用户反馈（点赞/点踩）
   - 任务完成率
   - 平均交互轮数
   - 重试率

**关键原则**: 评估要与业务目标对齐。如客服系统看任务完成率，创作系统看用户满意度。
