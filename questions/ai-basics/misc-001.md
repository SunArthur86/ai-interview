---
id: misc-001
difficulty: L2
category: ai-basics
subcategory: 大模型原理
tags:
- IO
feynman:
  essence: 序列内元素通过QK计算相关性并加权聚合V，实现全局并行信息交互。
  analogy: 每个人同时看一眼全场，决定听谁的；RNN像传声筒一个个传。
  first_principle: 如何打破序列计算的串行限制并捕捉全局上下文？
  key_points:
  - Q、K、V由输入线性变换得到
  - 计算复杂度随序列长度平方增长
  - 相比RNN能直接捕捉长距离依赖
follow_up:
- 为什么除以√d_k?--防止点积过大导致softmax梯度消失
- Multi-Head Attention的作用?--不同head学习不同子空间的注意力模式
---

# Transformer中的Self-Attention机制是什么?为什么比RNN更高效

Self-Attention允许序列中每个位置直接关注所有其他位置,计算加权求和.

- **核心公式:**
Attention(Q,K,V) = softmax(QKᵀ/√d_k)·V

- **Q/K/V的来源:** 输入X分别乘以三个权重矩阵Wq/Wk/Wv

- **优势:**
1. **并行计算** - RNN必须串行处理,Self-Attention可并行
2. **长距离依赖** - 任意两个token间距离为O(1),RNN为O(n)
3. **可解释性** - 注意力权重矩阵可视化理解模型关注点

- **复杂度对比:**
- Self-Attention: O(n²·d) - 序列长度平方,但可并行
- RNN: O(n·d²) - 序列长度线性,但必须串行
