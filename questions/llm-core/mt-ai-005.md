---
id: mt-ai-005
difficulty: L3
category: llm-core
categories:
- eng-practice
- llm-core
subcategory: 训练与微调
tags:
- 美团
- 面经
- SFT
- RLHF
- 后训练
feynman:
  essence: 从“读书”到“做题”再到“讲规矩”的过程。
  analogy: SFT是教学生做题格式，RLHF是给回答打分纠偏，最后变成懂礼貌的优等生。
  first_principle: 如何让一个博学但不懂礼貌的基座模型，变成符合人类价值观的助手？
  key_points:
  - SFT：学会遵循指令和格式
  - RM：训练打分员判断回答好坏
  - RLHF/DPO：基于人类偏好优化对齐
  - 趋势：DPO因无需显式RM逐渐普及
follow_up:
- DPO 和 PPO 的区别？—— DPO 无需 RM、无需在线采样，直接离线优化偏好
- SFT 数据怎么构建？—— 人工标注 + 强模型蒸馏 + Self-Instruct
- 为什么需要安全对齐？—— 防止越狱攻击、有害内容、隐私泄露
---

# 【美团面经】说一说大模型后训练（Post-training）的流程？

大模型训练分为**预训练（Pre-training）** 和**后训练（Post-training）** 两大阶段。

**后训练完整流程：**

```
预训练模型（Base Model）
  │
  ├─ ① SFT（监督微调）
  │    用高质量指令-回答对微调
  │    让模型学会'听懂指令'并按格式输出
  │
  ├─ ② 奖励模型训练（Reward Model）
  │    用人类偏好数据训练打分模型
  │    输入：(prompt, response) → 输出：标量分数
  │
  ├─ ③ RLHF / DPO 对齐
  │    RLHF：用 RM 的分数做 PPO 强化学习
  │    DPO：直接用偏好对优化，无需显式 RM
  │
  ├─ ④ 安全对齐（可选）
  │    Red-teaming + Constitutional AI
  │    防止有害输出
  │
  └─ ⑤ 模型合并 / 量化
       DARE / TIES 合并，GPTQ / AWQ 量化
```

**关键细节：**
- **SFT 数据量**：通常 1万~100万条，质量 > 数量
- **RLHF vs DPO**：RLHF 需要训练 RM + PPO（复杂），DPO 直接从偏好对优化（简单高效）
- **DeepSeek-R1 的创新**：跳过 SFT 直接 RL（RL first），用 GRPO 替代 PPO
- **迭代对齐**：GPT-4 / Claude 等顶级模型都经过多轮 RLHF 迭代
