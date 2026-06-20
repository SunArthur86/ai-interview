---
id: mt-ai-002
difficulty: L4
category: llm-core
categories:
- eng-practice
- llm-core
subcategory: 位置编码
tags:
- 美团
- 面经
- RoPE
- 位置编码
feynman:
  essence: 通过旋转向量将绝对位置转化为相对位置信息。
  analogy: 像两个人在舞池旋转，他们的角度差（相对位置）决定了他们是否面对面，与他们在舞池的哪个角落无关。
  first_principle: 如何让Transformer感知token间的顺序，同时具备处理未见长度的泛化能力？
  key_points:
  - 原理：对Q/K向量进行旋转变换
  - 优势：内积体现相对位置，支持长度外推
  - 计算：逐元素乘法，计算效率高
  - 地位：当前LLM主流位置编码方案
follow_up:
- RoPE 怎么做长度外推？—— NTK-aware / YaRN / Dynamic NTK 等方法调整旋转基座
- ALiBi 和 RoPE 对比？—— ALiBi 外推更简单但表达能力弱，RoPE 灵活但外推需技巧
- RoPE 为什么对 Q/K 旋转而不对 V？—— 因为 attention 只用 Q·K 算权重，位置信息只需在相似度计算中体现
---

# 【美团面经】说一说 RoPE 的原理，为什么现在 RoPE 更受欢迎？还了解其他位置编码吗？

**RoPE (Rotary Position Embedding) 旋转位置编码** 是目前大模型最主流的位置编码方案。

**核心原理：**
- 通过旋转矩阵将**绝对位置**信息编码到 Q/K 向量中
- 旋转后 Q·K 的内积自然包含了**相对位置**信息
- 公式：q_m = R_θ,m · q, k_n = R_θ,n · k
- 其中 R_θ 是基于位置 m/n 的旋转矩阵

**数学形式：**
```
对位置 m 的第 2i 和 2i+1 维：
q[2i]   = q[2i]·cos(mθ_i) - q[2i+1]·sin(mθ_i)
q[2i+1] = q[2i]·sin(mθ_i) + q[2i+1]·cos(mθ_i)
```

**为什么 RoPE 更受欢迎：**
1. **相对位置感知** — 内积结果只依赖 m-n（相对距离），不依赖绝对位置
2. **长度外推** — 对未见过的更长序列有一定泛化能力
3. **计算高效** — 只需逐元素乘法，无额外矩阵乘法
4. **与 Attention 无缝集成** — 只影响 Q/K，不影响 V
5. **远程衰减** — 理论上随距离增加注意力自然衰减

**其他位置编码：**
- **绝对正弦编码** — Transformer 原版，sin/cos 固定编码
- **可学习位置编码** — BERT/GPT 使用，每个位置一个可训练向量
- **ALiBi** — 直接在 attention score 上加距离偏置，外推能力强
- **NoPE** — 无位置编码（GPT-NeoX 某些实验发现 causal mask 本身含位置信息）
