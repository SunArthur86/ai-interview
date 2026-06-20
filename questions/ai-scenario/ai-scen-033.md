---
id: "ai-scen-033"
difficulty: "L2"
category: "ai-scenario"
subcategory: "AI评测与监控"
tags:
  - "LLM-as-Judge"
  - "自动评测"
  - "偏差校准"
  - "Pairwise"
  - "Cohen's Kappa"
  - "评分标准"
feynman:
  essence: "【场景分析】 LLM-as-Judge是用大模型自动评测其他模型输出的方法，可大幅提升评测效率，但有固有偏差"
  analogy: "AI 评测体系就像学校的考试系统——Golden Set 是标准试题，LLM-as-Judge 是 AI 老师自动阅卷，持续监测模型质量。"
  key_points:
    - "单答案评分（Single Answer Scoring）："
    - "输入：问题 + 答案 + 评分标准"
    - "输出：1-5分 + 评分理由"
first_principle:
  problem: "如果要解决这个问题，最本质的方法论是什么？先理解问题约束，再找最优路径。"
  axioms:
    - "模型本质是数学函数的参数优化——所有能力都来自数据和参数"
    - "质量 > 数量：数据质量决定模型上限，算法决定达到上限的效率"
  rebuild: "从 AI 系统出发：① 核心挑战是什么？② 现有方案如何解决？③ 有哪些 trade-off？④ 如果重新设计你会怎么做？"
follow_up:
  - "如何选择合适的Judge模型？"
  - "LLM-as-Judge的评分如何与人工评分对齐？"
  - "在什么场景下LLM-as-Judge不可靠？"
---

# 如何设计LLM-as-Judge评测管道？用大模型自动评测其他模型的输出质量。

【场景分析】
LLM-as-Judge是用大模型自动评测其他模型输出的方法，可大幅提升评测效率，但有固有偏差。

【LLM-as-Judge模式】
1. 单答案评分（Single Answer Scoring）：
   - 输入：问题 + 答案 + 评分标准
   - 输出：1-5分 + 评分理由
   - Prompt设计：详细的Rubric评分细则
2. 答案对比（Pairwise Comparison）：
   - 输入：问题 + 答案A + 答案B
   - 输出：A更好/B更好/平手 + 理由
   - 优势：相对评价比绝对评分更稳定
3. 参考对比（Reference-based）：
   - 输入：问题 + 答案 + 参考答案
   - 评估：答案与参考答案的语义匹配度

【已知偏差与校准】
1. Position Bias（位置偏差）：
   - 倾向于选择第一个或最后一个答案
   - 校准：交换A/B位置跑两次，取一致结果
2. Verbosity Bias（冗长偏差）：
   - 倾向于给更长的答案高分
   - 校准：在评分标准中明确「简洁性」权重
3. Self-Enhancement Bias（自我增强偏差）：
   - GPT-4评价GPT-4的输出时分数偏高
   - 校准：使用不同供应商的模型作为Judge
4. Domain Bias（领域偏差）：
   - Judge模型在某些领域（如法律、医疗）能力不足
   - 校准：领域专家定期抽检校准

【生产实践】
- Judge模型选择：GPT-4o / Claude-3.5-Sonnet（效果最好但贵）
- 成本优化：日常CI用GPT-4o-mini，正式评测用GPT-4o
- 人工校准：每周抽5%样本人工复核，计算Judge与人工的一致性
- 一致性指标：Cohen's Kappa > 0.6 为可接受
- 持续迭代：将人工修正的评分作为Few-shot示例优化Judge Prompt
