---
id: "mt-ai-002"
difficulty: "L4"
category: "llm-core"
categories:
  - "eng-practice"
  - "llm-core"
subcategory: "位置编码"
tags:
  - "美团"
  - "面经"
  - "RoPE"
  - "位置编码"
feynman:
  essence: "RoPE 把每个位置想象成一个角度，把 Q/K 向量按这个角度旋转，这样两个位置的注意力计算自然包含了它们的相对角度差（相对位置）。"
  analogy: "想象时钟上的指针——每个位置对应一个角度，两个位置的注意力大小取决于它们指针的夹角。距离近的角度差小（注意力大），距离远的角度差大（注意力小），天然实现了远程衰减。"
  key_points:
    - "绝对位置旋转编码 → 内积自动包含相对位置"
    - "逐元素乘法，计算高效"
    - "支持长度外推（配合 NTK/YaRN）"
    - "只旋转 Q/K，不旋转 V"
    - "远程衰减特性"
first_principle:
  problem: "Self-Attention 本身是排列不变的（permutation-invariant），需要位置编码来注入顺序信息。什么样的位置编码既高效又通用？"
  axioms:
    - "Attention = softmax(QK^T/√d)·V —— 位置信息必须通过 Q/K 或直接加在 score 上"
    - "相对位置比绝对位置更本质 —— 语言中'第3个词和第5个词'比'第3个词'更有意义"
    - "旋转保持向量范数不变 —— RoPE 只改方向不改大小，不破坏 Q·K 的尺度"
  rebuild: "从 Attention 的排列不变性出发：① 位置信息可以在哪注入（输入嵌入、Q/K、Attention Score）？② 绝对 vs 相对位置哪个更本质？③ 如何让编码同时满足高效计算和长度泛化？④ 旋转操作为什么满足所有约束？"
follow_up:
  - "RoPE 怎么做长度外推？—— NTK-aware / YaRN / Dynamic NTK 等方法调整旋转基座"
  - "ALiBi 和 RoPE 对比？—— ALiBi 外推更简单但表达能力弱，RoPE 灵活但外推需技巧"
  - "RoPE 为什么对 Q/K 旋转而不对 V？—— 因为 attention 只用 Q·K 算权重，位置信息只需在相似度计算中体现"
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
