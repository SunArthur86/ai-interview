---
id: misc-033
difficulty: L2
category: ai-basics
subcategory: Prompt Engineering
tags:
- IOC
feynman:
  essence: 通过在提示词中给范例，让模型模仿完成任务，无需训练。
  analogy: 像学书法，给字帖照着描红（给例子），描多了自然就会写了，不用改大脑结构。
  first_principle: 如何在模型参数不变的情况下，利用提示工程让模型快速适应新的下游任务？
  key_points:
  - 不需要梯度下降，仅靠上下文学习
  - 示例的顺序、格式和内容影响巨大
  - Self-Consistency通过多路径投票提升稳定性
follow_up:
- 为什么示例顺序影响这么大?
- 如何自动选择最优示例?
---

# In-Context Learning (ICL) 的原理是什么?Few-shot示例如何选择

- **ICL (In-Context Learning):** 模型从prompt中提供的示例学习模式,无需参数更新.

- **示例选择策略:**

1. **随机选择** - 基线,效果不稳定
2. **相似度选择** - 用embedding找与输入最相似的示例
3. **投票选择** - 多组示例投票,选一致性最高的(Self-Consistency)
4. **多样性选择** - 选择覆盖不同模式的示例

- **关键发现:**
- 示例**顺序**影响巨大(准确率波动>10%)
- 示例**格式**必须一致
- **3-5个**示例通常效果最好
- 负面示例(错误答案)可能比正面示例更有效

- **Self-Consistency:**
1. 用不同示例生成多个答案
2. 对答案进行多数投票
3. 准确率提升5-15%
