---
id: "misc-037"
difficulty: "L2"
category: "ai-basics"
subcategory: "Prompt Engineering"
tags:
  - "IO"
  - "Elasticsearch"
feynman:
  essence: "- *DSPy核心:** 用声明式编程替代手写prompt,让框架自动搜索最优prompt. - *传统方式:** 手写prompt → 人工调优 → 效果不稳"
  analogy: "Prompt 就像给 AI 的工作指令——指令越清晰、上下文越充分，AI 完成质量越高。"
  key_points:
    - "DSPy核心: 用声明式编程替代手写prompt,让框架自动搜索最优prompt."
    - "传统方式: 手写prompt → 人工调优 → 效果不稳定"
    - "DSPy方式: 定义输入输出 → 选择模块 → 自动优化 → 验证效果"
first_principle:
  problem: "从第一性原理看：DSPy框架的核心思想?它如何自动优化Prompt 的根本优势/劣势来源于什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "DSPy的BootstrapFewShot如何选择示例?"
  - "DSPy和LangChain有什么本质区别?"
---

# DSPy框架的核心思想是什么?它如何自动优化Prompt

- **DSPy核心:** 用声明式编程替代手写prompt,让框架自动搜索最优prompt.

- **传统方式:** 手写prompt → 人工调优 → 效果不稳定
- **DSPy方式:** 定义输入输出 → 选择模块 → 自动优化 → 验证效果

- **核心概念:**
1. **Signature** - 声明输入输出(类似函数签名)
2. **Module** - 可组合的处理单元(类似神经网络层)
3. **Teleprompter (Optimizer)** - 自动优化模块参数
4. **Metric** - 评估函数

- **优化流程:**
```python
# 声明式定义
class QA(dspy.Signature):
"""回答问题"""
question = dspy.InputField()
answer = dspy.OutputField()

# 自动优化
teleprompter = dspy.BootstrapFewShot(metric=my_metric)
compiled = teleprompter.compile(QA(), trainset=data)
```

- **优势:**
- Prompt版本可追溯、可复现
- 自动搜索Few-shot示例
- 适配不同模型(GPT/Claude/GLM)
