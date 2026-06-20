---
id: misc-042
difficulty: L2
category: ai-basics
subcategory: 评估与安全
feynman:
  essence: 通过标准化数据集和指标量化模型的各项能力，衡量模型优劣。
  analogy: 像“高考”一样统一出题，给学生打分，但高分未必代表能干好工作。
  first_principle: 如何科学、客观地衡量大模型在特定任务或通用场景下的能力水平？
  key_points:
  - MMLU考知识广度，GSM8K/HumanEval考逻辑
  - MT-Bench侧重对话体验
  - 警惕数据污染，需结合人工评测
follow_up:
- 如何检测模型是否在benchmark上过拟合?
- LiveBench如何解决数据污染问题?
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
