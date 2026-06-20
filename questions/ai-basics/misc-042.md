---
id: "misc-042"
difficulty: "L2"
category: "ai-basics"
subcategory: "评估与安全"
feynman:
  essence: "C-Eval + GSM8K + HumanEval + MT-Bench + 真实用户A/B测试。"
  analogy: "大语言模型就像读过整个互联网的学者——通过预测「下一个词」生成文本，积累了海量语言模式和知识。"
  key_points:
    - "数据污染 - 训练数据可能包含测试题"
    - "过拟合 - 针对benchmark优化"
    - "覆盖面 - 无法覆盖真实使用场景"
first_principle:
  problem: "为什么需要 大模型的主流评估基准有哪些?各自评估什么能力?有什么局限性？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "如何检测模型是否在benchmark上过拟合?"
  - "LiveBench如何解决数据污染问题?"
---

# 大模型的主流评估基准有哪些?各自评估什么能力?有什么局限性

- **主流评估基准:**

| Benchmark | 评估能力 | 题目数 | 特点 |
|-----------|---------|--------|------|
| MMLU | 多学科知识 | 14K | 学术知识基准 |
| GSM8K | 数学推理 | 8.5K | 小学数学 |
| MATH | 高等数学 | 12.5K | 竞赛数学 |
| HumanEval | 代码生成 | 164 | 函数级编程 |
| MBPP | 代码生成 | 974 | 基础编程 |
| HellaSwag | 常识推理 | 10K | 多选 |
| TruthfulQA | 事实性 | 817 | 反幻觉 |
| **MT-Bench** | 多轮对话 | 80 | **GPT-4评分** |
| **Arena-Hard** | 复杂指令 | 500 | **最强区分度** |
| **C-Eval** | 中文综合 | 14K | 中文基准 |

- **局限性:**
1. **数据污染** - 训练数据可能包含测试题
2. **过拟合** - 针对benchmark优化
3. **覆盖面** - 无法覆盖真实使用场景
4. **多选题偏差** - 真实任务不是选择题

- **推荐组合:** C-Eval + GSM8K + HumanEval + MT-Bench + 真实用户A/B测试
