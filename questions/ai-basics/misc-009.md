---
id: "misc-009"
difficulty: "L2"
category: "ai-basics"
subcategory: "训练与微调"
feynman:
  essence: "- *RLHF (Reinforcement Learning from Human Feedback) 三阶段:** 1. **SFT (Supervised"
  analogy: "微调就像给通才毕业生做岗前培训——已有基础能力（预训练），再针对具体岗位做专项训练（指令/偏好对齐）。"
  key_points:
    - "RLHF (Reinforcement Learning from Human Feedback) 三阶段:"
    - "SFT (Supervised Fine-Tuning) - 人类标注高质量问答对"
    - "奖励模型训练 - 人类对模型输出排序,训练RM预测人类偏好"
first_principle:
  problem: "它们本质上为什么不同？各自的设计目标和适用场景是什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "GRPO和PPO有什么区别?"
  - "RLHF可能引入什么偏见?"
---

# RLHF的完整流程是什么?为什么需要它?PPO和DPO有什么区别

- **RLHF (Reinforcement Learning from Human Feedback) 三阶段:**

1. **SFT (Supervised Fine-Tuning)** - 人类标注高质量问答对
2. **奖励模型训练** - 人类对模型输出排序,训练RM预测人类偏好
3. **强化学习优化** - PPO/DPO优化策略模型

- **为什么需要RLHF:**
- 预训练模型只会「续写」,不会「对话」
- SFT学习格式,RLHF学习「好」的定义
- 减少幻觉/有害输出/不对齐行为

- **PPO vs DPO:**
| | PPO | DPO |
|--|-----|-----|
| 奖励模型 | 需要 | **不需要** |
| 训练稳定性 | 差(4个模型同时训练)| **好** |
| 流程 | 复杂 | **简单** |
| 效果 | 好 | **接近PPO** |
| 原理 | 策略梯度 | 直接偏好优化 |

- **DPO核心:** 跳过RM,直接从偏好数据对优化策略模型

- **趋势:** GRPO(DeepSeek)等新方法正在取代PPO
