---
id: "misc-044"
difficulty: "L2"
category: "ai-basics"
subcategory: "评估与安全"
tags:
  - "IO"
feynman:
  essence: "- *Constitutional AI (Anthropic提出):** - *核心思想:** 用一组「宪法原则」(不要有害/要诚实/要公平等)指导模型自我修"
  analogy: "RLHF 就像给 AI 请人类老师——人类给回答打分排序，训练奖励模型，再用强化学习让 AI 越来越符合人类偏好。"
  key_points:
    - "Constitutional AI (Anthropic提出):"
    - "核心思想: 用一组「宪法原则」(不要有害/要诚实/要公平等)指导模型自我修正,减少对人工标注的依赖."
    - "监督学习阶段 (SL-CAI):"
first_principle:
  problem: "它们本质上为什么不同？各自的设计目标和适用场景是什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "宪法原则如何设计?"
  - "CAI会不会引入AI偏见?"
---

# Constitutional AI (CAI)是什么?它和RLHF有什么区别

- **Constitutional AI (Anthropic提出):**

- **核心思想:** 用一组「宪法原则」(不要有害/要诚实/要公平等)指导模型自我修正,减少对人工标注的依赖.

- **两阶段:**
1. **监督学习阶段 (SL-CAI):**
- 模型生成回复 → 用宪法原则自我评价 → 修改后的回复作为SFT数据
2. **强化学习阶段 (RL-CAI):**
- 模型A生成回复 → 模型B(遵循宪法)评估哪个更好 → 用偏好对做RL(类似RLHF但RM是模型而非人)

- **CAI vs RLHF:**
| | RLHF | CAI |
|--|------|-----|
| 偏好来源 | 人类标注 | **AI自我评估** |
| 成本 | 高(人工) | **低** |
| 一致性 | 低(标注者分歧) | **高** |
| 可扩展性 | 差 | **好** |
| 价值观 | 隐式(标注者) | **显式(宪法)** |

- **效果:** Claude系列用CAI训练,在安全性和有用性之间取得更好平衡
