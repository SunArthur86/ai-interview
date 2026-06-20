---
id: bd-ai-010
difficulty: L2
category: llm-core
categories:
- ai-agent
- eng-practice
- llm-core
subcategory: Prompt工程
tags:
- 字节
- 面经
- Prompt Engineering
- System Prompt
- CoT
feynman:
  essence: 通过精准指令引导概率分布，将模糊意图转化为确定输出。
  analogy: 像是对着只会听指令的机器人说话，指令越具体，它动作越精准。
  first_principle: 如何最大化压缩模型的输出概率空间以匹配人类意图？
  key_points:
  - 核心是压缩概率空间，减少随机性
  - System Prompt定基调，Few-shot给范例
  - CoT展开推理链，提升复杂任务准确率
  - 明确角色、任务和约束
follow_up:
- Zero-shot vs Few-shot怎么选？——简单任务Zero-shot够，复杂格式用Few-shot
- CoT为什么有效？——中间步骤能纠偏，相当于增加推理深度
- Prompt越写越长好吗？——不是，太长会稀释注意力（Lost in the Middle）
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
- 给出示例
- 要求推理过程

**Prompt 概率分布示意：**
```text
Prompt: "写个介绍"           Prompt: "你是个资深Java面试官，写一段包含泛型、
                          多线程和JVM调优的自我介绍，100字以内。"
   ↓                              ↓
[???] ---------------->       [Target] <--- 概率密度尖峰
   概率分布平坦                   概率分布集中
   (输出不可控)                   (输出高度可控)
```

## 常见考点
1. **CoT的局限**：为什么在某些任务上CoT反而会降低效果？（简单任务反而引入了噪声，模型可能在思考过程中产生幻觉）
2. **Few-shot排序**：Few-shot示例的顺序对结果有影响吗？（有，最后给出的示例权重通常更高，且存在“Lost in the Middle”现象）
3. **提示词注入防御**：如何设计System Prompt使其在用户恶意输入下保持稳定？（使用分隔符和防御性指令）
