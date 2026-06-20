---
id: misc-013
difficulty: L2
category: ai-basics
subcategory: 训练与微调
tags:
- IO
feynman:
  essence: 用组内采样的相对优势替代Critic模型估计,大幅降低显存。
  analogy: PPO找裁判打分,GRPO让几个人互相比,不用裁判,看谁相对更好就给谁加分。
  first_principle: 如何在去除Critic模型的情况下准确估计策略优势?
  key_points:
  - 去掉了PPO中的Critic(Value)模型
  - 优势值来自同组输出的归一化分数
  - 显存减半,训练更快,适合强化学习推理
follow_up:
- GRPO的组大小G如何选择?
- GRPO为什么能涌现长链推理?
---

# DeepSeek提出的GRPO算法是什么?相比PPO有什么优势

- **GRPO (Group Relative Policy Optimization):**

PPO需要一个Critic模型估计baseline,GRPO用**组内相对奖励**替代Critic.

- **核心区别:**
| | PPO | GRPO |
|--|-----|------|
| Critic模型 | 需要(额外显存) | **不需要** |
| Baseline | Critic估计 | 组内均值 |
| 显存占用 | 高(4个模型) | **低(2个模型)** |
| 训练速度 | 慢 | **快** |

- **GRPO流程:**
1. 对同一个问题x,采样G个回答
2. 计算每个回答的奖励
3. 组内归一化:advantage_i = (r_i - mean(r)) / std(r)
4. 用advantage替代Critic估计

- **优势:**
- 省显存 - 去掉Critic模型
- 更稳定 - 组内归一化消除奖励尺度问题
- 效果好 - DeepSeek-R1证明GRPO可训练出顶级推理能力
