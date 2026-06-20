---
id: "misc-001"
difficulty: "L2"
category: "ai-basics"
subcategory: "大模型原理"
tags:
  - "IO"
feynman:
  essence: "Self-Attention 让序列中每个 token 直接「看到」所有其他 token 并加权汇总信息，公式是 softmax(QKᵀ/√d_k)·V；因为所有位置可并行计算、任意两 token 距离为 O(1)，所以比必须串行处理的 RNN 高效得多。"
  analogy: "注意力机制就像在聚会上听人说话——自动聚焦到感兴趣的声音，给不同人不同关注度，数学上就是加权的加权求和。"
  key_points:
    - "Q/K/V的来源: 输入X分别乘以三个权重矩阵Wq/Wk/Wv"
    - "并行计算 - RNN必须串行处理,Self-Attention可并行"
    - "长距离依赖 - 任意两个token间距离为O(1),RNN为O(n)"
first_principle:
  problem: "为什么需要 Transformer中的Self-Attention机制?为什么比RNN更高效？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "为什么除以√d_k?--防止点积过大导致softmax梯度消失"
  - "Multi-Head Attention的作用?--不同head学习不同子空间的注意力模式"
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
