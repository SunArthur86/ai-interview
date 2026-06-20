---
id: "misc-013"
difficulty: "L2"
category: "ai-basics"
subcategory: "训练与微调"
tags:
  - "IO"
feynman:
  essence: "- *GRPO (Group Relative Policy Optimization):** PPO需要一个Critic模型估计baseline,GRPO用*"
  analogy: "RLHF 就像给 AI 请人类老师——先让人类给 AI 回答打分排序，训练奖励模型，再用强化学习让 AI 越来越懂事。"
  key_points:
    - "GRPO (Group Relative Policy Optimization):"
    - "对同一个问题x,采样G个回答"
    - "组内归一化:advantage_i = (r_i - mean(r)) / std(r)"
first_principle:
  problem: "从第一性原理看：DeepSeek提出的GRPO算法?相比PPO有什么优势 的根本优势/劣势来源于什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "GRPO的组大小G如何选择?"
  - "GRPO为什么能涌现长链推理?"
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
