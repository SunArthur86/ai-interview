---
id: misc-037
difficulty: L2
category: ai-basics
subcategory: Prompt Engineering
tags:
- IO
- Elasticsearch
feynman:
  essence: 将Prompt Engineering转变为编程问题，通过算法自动优化提示词。
  analogy: 像写代码定义接口，让编译器自动优化底层实现，而不是手写汇编。
  first_principle: 如何解决手工调试Prompt效率低、难复现且难以规模化的问题？
  key_points:
  - 用Signature声明输入输出接口
  - 用Teleprompter自动寻找最优示例
  - 程序化替代手工调试Prompt
follow_up:
- DSPy的BootstrapFewShot如何选择示例?
- DSPy和LangChain有什么本质区别?
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
