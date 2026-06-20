---
id: "mt-ai-005"
difficulty: "L3"
category: "llm-core"
categories:
  - "eng-practice"
  - "llm-core"
subcategory: "训练与微调"
tags:
  - "美团"
  - "面经"
  - "SFT"
  - "RLHF"
  - "后训练"
feynman:
  essence: "后训练 = 让预训练的'博学但不会对话'的模型变成'博学且有用无害'的助手。先教它听指令（SFT），再用人类偏好调教（RLHF/DPO），最后加安全护栏。"
  analogy: "预训练模型像刚毕业的大学生（知识丰富但不会沟通）→ SFT = 职场礼仪培训 → RLHF = 导师根据表现给反馈持续改进 → 安全对齐 = 合规培训。"
  key_points:
    - "SFT → 学会指令跟随和格式输出"
    - "RM → 学习人类偏好打分"
    - "RLHF/DPO → 对齐优化"
    - "安全对齐 → 防有害输出"
    - "质量 > 数量，数据是关键"
first_principle:
  problem: "预训练模型有知识但不会对话。如何用最少的标注数据，让模型变得有用（helpful）、诚实（honest）、无害（harmless）？"
  axioms:
    - "预训练模型已具备知识——后训练只需调整行为而非注入知识"
    - "人类偏好是稀疏且主观的——需要 RM 或直接偏好优化"
    - "对齐三目标（HHH）之间可能冲突——需要权衡"
  rebuild: "从'行为调整'角度出发：① 最小化行为调整需要什么数据（指令跟随）？② 如何高效利用偏好数据（RLHF vs DPO）？③ 安全边界怎么定义和执行？④ 如何避免灾难性遗忘？"
follow_up:
  - "DPO 和 PPO 的区别？—— DPO 无需 RM、无需在线采样，直接离线优化偏好"
  - "SFT 数据怎么构建？—— 人工标注 + 强模型蒸馏 + Self-Instruct"
  - "为什么需要安全对齐？—— 防止越狱攻击、有害内容、隐私泄露"
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
