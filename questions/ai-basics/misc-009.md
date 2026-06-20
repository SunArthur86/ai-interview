---
id: misc-009
difficulty: L2
category: ai-basics
subcategory: 训练与微调
feynman:
  essence: 利用人类反馈训练奖励模型,再通过强化学习对齐模型偏好。
  analogy: 像训狗,预训练让它学认字,SFT教它握手,RLHF给它奖励或惩罚让它懂礼貌。
  first_principle: 如何让模型的输出分布与人类的偏好分布对齐?
  key_points:
  - 三步走:SFT学形式 -> RM打分 -> RL学价值观
  - DPO不用显式训练奖励模型,更稳更简单
  - 解决的是模型输出是否"对人类友好"的问题
follow_up:
- GRPO和PPO有什么区别?
- RLHF可能引入什么偏见?
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
