---
id: "misc-033"
difficulty: "L2"
category: "ai-basics"
subcategory: "Prompt Engineering"
tags:
  - "IOC"
feynman:
  essence: "- *ICL (In-Context Learning):** 模型从prompt中提供的示例学习模式,无需参数更新. - *示例选择策略:** 1. **随机"
  analogy: "Prompt 就像给 AI 的工作指令——指令越清晰、示例越精准、推理步骤越明确（CoT），AI 完成质量越高。"
  key_points:
    - "ICL (In-Context Learning): 模型从prompt中提供的示例学习模式,无需参数更新."
    - "随机选择 - 基线,效果不稳定"
    - "相似度选择 - 用embedding找与输入最相似的示例"
first_principle:
  problem: "剥离所有术语：In-Context Learning (ICL) 的原理?Few-shot示例如何选择 底层在做什么？为什么这样做是最优的？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "为什么示例顺序影响这么大?"
  - "如何自动选择最优示例?"
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
