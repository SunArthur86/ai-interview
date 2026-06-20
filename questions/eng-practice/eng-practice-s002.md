---
id: "eng-practice-s002"
difficulty: "L2"
category: "eng-practice"
subcategory: "工程化实战"
feynman:
  essence: "LLM应用评估是多维度的： 1. 基准测试（Benchmark）： - MMLU：多任务理解 - HumanEval：代码生成 - GSM8K：数学推理 - C"
  analogy: "大语言模型就像读过整个互联网的学者——通过预测「下一个词」生成文本，积累了海量语言模式和知识。"
  key_points:
    - "基准测试（Benchmark）："
    - "HumanEval：代码生成"
    - "C-Eval/CMMLU：中文评测"
first_principle:
  problem: "如果要解决这个问题，最本质的方法论是什么？先理解问题约束，再找最优路径。"
  axioms:
    - "模型本质是数学函数的参数优化——所有能力都来自数据和参数"
    - "质量 > 数量：数据质量决定模型上限，算法决定达到上限的效率"
  rebuild: "从 AI 系统出发：① 核心挑战是什么？② 现有方案如何解决？③ 有哪些 trade-off？④ 如果重新设计你会怎么做？"
---

# 如何评估LLM应用的效果？

LLM应用评估是多维度的：

1. 基准测试（Benchmark）：
- MMLU：多任务理解
- HumanEval：代码生成
- GSM8K：数学推理
- C-Eval/CMMLU：中文评测

2. 自动评估：
- Exact Match / F1
- BLEU / ROUGE（文本生成）
- LLM-as-Judge：用GPT-4评分
- RAGAS：RAG专用评估（Faithfulness、Relevancy、Context Recall）

3. 人工评估：
- Elo Rating（人机对比）
- Pairwise Comparison（两个回答比较）
- 标注质量评估

4. 在线指标：
- 用户反馈（点赞/点踩）
- 任务完成率
- 平均交互轮数
- 重试率

关键原则：评估要与业务目标对齐。如客服系统看任务完成率，创作系统看用户满意度。
