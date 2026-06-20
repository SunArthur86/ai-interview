---
id: bd-ai-014
difficulty: L4
category: llm-core
categories:
- ai-agent
- eng-practice
- llm-core
subcategory: 训练与微调
tags:
- 字节
- 面经
- SFT
- RLHF
- DPO
feynman:
  essence: SFT靠优质数据快速成型，RLHF靠反馈奖励对齐偏好，正向自动化发展。
  analogy: SFT像照着模范书练习（有样学样），RLHF像老师根据表现打分（纠正偏差）。
  first_principle: 如何高效地将基础模型能力转化为符合人类价值观的高质量智能？
  key_points:
  - SFT迭代快，适合注入知识能力；RLHF效果上限高，适合对齐
  - 基模强时，SFT核心是数据质量而非数量
  - RLHF趋向自动验证（如代码运行结果）替代人工打分
  - DPO简化RL流程，成为新主流
follow_up:
- DPO和PPO的区别？——DPO无需RM、无需在线采样，直接离线优化偏好
- RLHF的Reward Model怎么训？——用人类偏好对（chosen/rejected）做排序学习
- 基模强了还需要微调吗？——需要，但重点从知识注入转向行为对齐
---

# 【字节面经】SFT和RLHF哪个更适合快速迭代？在基模能力越来越强的情况下，这两者的破局点是什么？

**SFT更适合快速迭代。**

**对比：**
- **SFT**（监督微调）：流程简单——准备问答对直接训。几个小时到一天出结果。
- **RLHF**：需要先训Reward Model再做PPO。链路长、工程复杂、稳定性差，一个迭代周期可能是SFT的好几倍。

**但RLHF的优势是能对齐人类偏好。** SFT只能学到数据里的模式，RLHF能学到什么是好的。

**基模变强后的破局点：**

**SFT的破局点 = 数据质量而非数量。**
- 几百条高质量数据的效果可能比几万条普通数据好
- 关键是构造出模型自己想不出来的优质回答
- DeepSeek-R1验证了：少量推理链数据可以做SFT蒸馏

**RLHF的破局点 = 从人工标注走向自动反馈。**
- 用Verifiable Reward（可验证奖励）替代人工打分
- 代码能不能跑通、数学题对不对——自动验证
- DeepSeek-R1用GRPO+规则奖励实现RL，无需人工标注
- DPO简化了RLHF流程（无需显式RM），成为快速对齐首选
