---
id: mt-ai-007
difficulty: L2
category: llm-core
categories:
- eng-practice
- llm-core
subcategory: 推理优化
tags:
- 美团
- 面经
- 解码策略
- 采样
feynman:
  essence: 从概率分布中选择token的策略，平衡确定性与多样性。
  analogy: 像写作文，是每次只选最顺口的词（Greedy），还是在候选词里随机抽（Sampling），取决于你想要标准答案还是创意。
  first_principle: 如何将模型输出的概率分布转化为高质量的文本序列？
  key_points:
  - Greedy：最稳但死板，适合做题
  - Sampling：引入随机性，适合创作
  - Top-K/Top-P：过滤掉低概率的胡言乱语
  - Temperature：控制随机程度的旋钮
follow_up:
- Top-K 和 Top-P 怎么选？—— Top-P 更自适应，通常优先
- 为什么 Temperature=0 时结果不一定完全一致？—— 浮点精度 + batch padding 影响
- Speculative Decoding 怎么加速？—— 小模型快速生成候选，大模型批量验证
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

**解码流程架构图：**
```text
      Input Prompt
           │
           ▼
┌───────────────────────┐
│   Model Forward Pass  │  ◄── Hidden States
│   (计算 Logits)       │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│   Logits Processing   │
│ 1. Temperature Scale  │
│ 2. Repetition Penalty │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│   Sampling Strategy   │─────► Greedy / Beam / Top-K / Top-P
└───────────┬───────────┘
            │
            ▼
      Selected Token
            │
            ▼ (Append to Input)
      Next Step ...
```

**实用建议：**
- 代码/数学：T=0~0.3（确定性优先）
- 创意写作：T=0.7~1.0（多样性优先）
- 对话：T=0.5~0.7 + Top-P=0.9

**进阶：**
- **Speculative Decoding** — 小模型草拟+大模型验证，加速 2-3×
- **Medusa** — 多头并行预测多个 token

## 常见考点
1. **Top-K 与 Top-P 的区别与联系**：为什么要结合使用（通常 Top-P 更灵活，K 是硬截断）？
2. **Beam Search 的缺点**：为什么在开放式生成（如对话）中效果不如采样（容易导致重复生硬）？
3. **Temperature 为 0 时的数值稳定性**：在代码实现中如何避免除零错误（通常取极小值如 1e-5）？
4. **Speculative Decoding 的加速原理**：它是如何保证输出结果与原模型一致性的（接受率机制）？
