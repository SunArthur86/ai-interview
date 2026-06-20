---
id: "bd-ai-010"
difficulty: "L2"
category: "llm-core"
categories:
  - "ai-agent"
  - "eng-practice"
  - "llm-core"
subcategory: "Prompt工程"
tags:
  - "字节"
  - "面经"
  - "Prompt Engineering"
  - "System Prompt"
  - "CoT"
feynman:
  essence: "Prompt Engineering不是'哄模型'，是把意图翻译成模型概率分布最集中的表达方式。"
  analogy: "Prompt像给GPS设目的地——说'去东边'（模糊）导航可能带你到荒郊野外，说'北京市海淀区中关村大街1号'（精准）就能精确到达。"
  key_points:
    - "核心=意图翻译"
    - "概率分布集中=好效果"
    - "System Prompt+Few-shot+CoT三大策略"
    - "角色+任务+约束+示例+推理"
first_principle:
  problem: "LLM根据输入按概率分布生成下一个Token。如何设计输入使概率分布集中在期望输出上？"
  axioms:
    - "LLM是概率生成器——输入决定输出分布"
    - "约束越多=概率越集中"
    - "示例>规则——模型从模式中学习比从指令中学习更有效"
  rebuild: "从概率生成模型出发：模糊输入导致什么（概率分散）？怎么集中概率（约束+示例+推理引导）？不同策略解决什么问题（角色/格式/推理）？"
follow_up:
  - "Zero-shot vs Few-shot怎么选？——简单任务Zero-shot够，复杂格式用Few-shot"
  - "CoT为什么有效？——中间步骤能纠偏，相当于增加推理深度"
  - "Prompt越写越长好吗？——不是，太长会稀释注意力（Lost in the Middle）"
---

# 【字节面经】Prompt Engineering的核心目标是什么？为什么模型会对同一件事，换个说法效果差十倍？

**Prompt Engineering的核心目标：把你的意图翻译成模型最容易理解的形式。**

大模型本质是概率生成器，Prompt写得模糊，概率就分散到八百个方向；写得精准，概率就集中到你想要的那条路上。

**三大Prompt策略解决不同问题：**
1. **System Prompt** — 解决始终按某种风格/角色回答的问题，整个对话期间都生效
2. **Few-shot** — 解决格式和模式对齐的问题，给模型看几个例子比写一堆规则管用
3. **Chain-of-Thought (CoT)** — 解决复杂推理容易出错的问题，让模型把思考过程写出来而不是直接给结论

**效果差异的根本原因：**
- 好的Prompt = 概率分布集中 → 输出确定性高
- 差的Prompt = 概率分布分散 → 输出随机性大

**实用技巧：**
- 明确角色（你是一个XX专家）
- 明确任务（帮我做XX）
- 明确约束（字数/格式/风格）
- 给出示例（Few-shot）
- 要求推理过程（CoT）
