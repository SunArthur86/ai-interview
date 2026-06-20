---
id: "misc-012"
difficulty: "L2"
category: "ai-basics"
subcategory: "训练与微调"
tags:
  - "IO"
  - "IOC"
feynman:
  essence: "- *DPO (Direct Preference Optimization) 核心:** 利用RLHF的闭式解,将奖励模型隐式地包含在策略模型中. - *推导"
  analogy: "微调就像给通才毕业生做岗前培训——已有基础能力（预训练），再针对具体岗位做专项训练（指令/偏好对齐）。"
  key_points:
    - "DPO (Direct Preference Optimization) 核心:"
    - "RLHF目标:max E[r(x,y)] - beta * KL(pi||pi_ref)"
    - "最优策略闭式解可反解出奖励函数"
first_principle:
  problem: "为什么需要 DPO的数学推导核心?为什么能跳过奖励模型？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "DPO的beta参数如何调节?"
  - "IPO和KTO是DPO的什么改进?"
---

# DPO的数学推导核心是什么?为什么能跳过奖励模型

- **DPO (Direct Preference Optimization) 核心:**

利用RLHF的闭式解,将奖励模型隐式地包含在策略模型中.

- **推导关键步骤:**
1. RLHF目标:max E[r(x,y)] - beta * KL(pi||pi_ref)
2. 最优策略闭式解可反解出奖励函数
3. 代入Bradley-Terry偏好模型
4. 得到**无需RM的损失函数**

- *L_DPO = -log sigma(beta * log(pi(y_w)/pi_ref(y_w)) - beta * log(pi(y_l)/pi_ref(y_l)))**

其中 y_w=偏好回答, y_l=不偏好回答

- **优势:**
- 只需2个模型(当前策略+参考策略),PPO需要4个
- 无需训练和推理奖励模型
- 训练更稳定(无reward hacking)
- 效果接近PPO
