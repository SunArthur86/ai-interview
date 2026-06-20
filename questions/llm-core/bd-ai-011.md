---
id: "bd-ai-011"
difficulty: "L3"
category: "llm-core"
categories:
  - "ai-agent"
  - "eng-practice"
  - "llm-core"
subcategory: "Prompt工程"
tags:
  - "字节"
  - "面经"
  - "幻觉"
  - "Hallucination"
  - "RAG"
feynman:
  essence: "幻觉=模型在'猜'而不是在'查'。减轻幻觉=减少猜测空间（给事实/给工具/约束格式/允许说不知道）。"
  analogy: "模型幻觉像学生考试瞎蒙——RAG=开卷考试（可以查资料），Function Calling=允许用计算器（可以算），Structured Output=只填选择题（不能自由发挥）。"
  key_points:
    - "本质=概率预测不是事实检索"
    - "RAG+FC+SO+Prompt组合拳"
    - "不能消除只能减轻"
    - "多轮验证双重保险"
first_principle:
  problem: "LLM的训练目标是预测下一个Token，不是检索事实。如何在不改变模型本质的情况下减少事实错误？"
  axioms:
    - "LLM=概率生成器不是知识库"
    - "减少自由度=减少幻觉空间"
    - "外部验证>内部约束"
  rebuild: "从概率生成出发：为什么会幻觉（预测而非检索）？怎么减少猜测空间（给事实/给工具/约束格式）？怎么验证（多轮检查/fact-check）？"
follow_up:
  - "幻觉能完全消除吗？——不能，只能减轻，因为LLM本质是概率生成"
  - "RAG为什么能减轻幻觉？——给了模型事实依据，概率分布集中在正确答案上"
  - "怎么评估幻觉率？——人工标注 + LLM-as-Judge + Factual Consistency Score"
---

# 【字节面经】幻觉是怎么产生的？你有哪些方法可以减轻模型幻觉？

**幻觉产生原因：** 大模型本质是在预测下一个最可能出现的Token，不是在检索事实，所以它天然就会编。

**减轻幻觉的核心思路：减少模型自由发挥的空间。**

1. **RAG** — 把真实资料塞进上下文，让模型基于事实回答而不是凭记忆瞎编
2. **Function Calling** — 让模型调真实接口查数据，别自己编答案（问天气就调天气API）
3. **Structured Output** — 约束输出格式，格式越固定自由发挥空间越小
4. **Prompt明确说不知道** — '如果不知道就说不知道'，虽然不是100%管用但能降低编造概率
5. **多轮验证** — 让模型自己检查一遍输出，或用另一个模型做fact-check

**实际项目组合使用：** RAG提供事实背景 + Function Calling获取实时数据 + Structured Output约束格式 + Prompt声明不知道就说不知道。单靠一个方法很难彻底解决幻觉。
