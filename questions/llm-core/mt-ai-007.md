---
id: "mt-ai-007"
difficulty: "L2"
category: "llm-core"
categories:
  - "eng-practice"
  - "llm-core"
subcategory: "推理优化"
tags:
  - "美团"
  - "面经"
  - "解码策略"
  - "采样"
feynman:
  essence: "解码策略就是在'确定性'和'创造性'之间找平衡——Greedy 太死板（重复），纯随机太混乱（跑题），Temperature/Top-K/Top-P 是各种'有控制的随机'。"
  analogy: "写作文时——Greedy = 只用最常用的词（无聊）；纯随机 = 闭眼翻词典（胡言乱语）；Top-P = 从最贴切的几个词里随机选（自然又有变化）。"
  key_points:
    - "Greedy：确定性但易重复"
    - "Top-P/Nucleus：动态截断，最自然"
    - "Temperature 控制随机性强度"
    - "Speculative Decoding 加速推理"
first_principle:
  problem: "大模型输出的是整个词表的概率分布。如何从分布中选出一个 token，既保证质量又保证多样性？"
  axioms:
    - "概率分布的熵反映不确定性——高熵=不确定=应该多样"
    - "尾部低概率 token 通常是噪声——截断提升质量"
    - "不同任务对确定性 vs 多样性的需求不同"
  rebuild: "从概率分布出发：① 直接取 argmax 有什么问题（重复/模式坍塌）？② 纯采样有什么问题（不连贯）？③ 如何截断分布去掉噪声？④ 如何控制截断的激进程度？"
follow_up:
  - "Top-K 和 Top-P 怎么选？—— Top-P 更自适应，通常优先"
  - "为什么 Temperature=0 时结果不一定完全一致？—— 浮点精度 + batch padding 影响"
  - "Speculative Decoding 怎么加速？—— 小模型快速生成候选，大模型批量验证"
---

# 【美团面经】了解大模型的解码策略吗？简要说一说

**大模型解码策略总结：**

| 策略 | 原理 | 特点 |
|------|------|------|
| **Greedy** | 每步选概率最高的 token | 确定性、易重复 |
| **Beam Search** | 维护 top-k 候选序列 | 平衡质量与多样性 |
| **Temperature Sampling** | 按温度缩放概率后采样 | T↑多样性↑，T↓确定性↑ |
| **Top-K Sampling** | 只从概率最高的 K 个中采样 | 截断尾部噪声 |
| **Top-P (Nucleus)** | 从累积概率≥P的最小集合中采样 | 动态截断，更自然 |
| **Contrastive Search** | 结合概率 + 惩罚重复 | 减少重复，保持连贯 |

**关键参数：**
- **Temperature (T)**：T=0 等价 Greedy；T=1 标准采样；T>1 更随机
  - 公式：p_i' = softmax(logit_i / T)
- **Top-P**：通常设 0.9~0.95
- **Repetition Penalty**：对已出现 token 降权，减少重复
- **Frequency Penalty**：按出现次数惩罚

**实用建议：**
- 代码/数学：T=0~0.3（确定性优先）
- 创意写作：T=0.7~1.0（多样性优先）
- 对话：T=0.5~0.7 + Top-P=0.9

**进阶：**
- **Speculative Decoding** — 小模型草拟+大模型验证，加速 2-3×
- **Medusa** — 多头并行预测多个 token
