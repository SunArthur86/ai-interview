---
id: ai-basics-s005
difficulty: L1
category: ai-basics
subcategory: 深度学习基础
images:
- svg_attention.svg
feynman:
  essence: 通过查询、键、值的交互动态聚合信息，解决长距离依赖并实现并行计算。
  analogy: 读文章时，看到某句话会回头找相关的上下文来理解它。
  first_principle: 如何让模型在处理序列时聚焦于最相关的信息？
  key_points:
  - QK相似度决定权重，加权聚合V得到输出
  - 解决了RNN无法并行和长距离遗忘的问题
  - 是Transformer架构的核心组件
---

# 什么是注意力机制？为什么在NLP中有效？

注意力机制（Attention）让模型在处理一个元素时，'关注'其他相关元素，动态分配权重。

核心公式：Attention(Q, K, V) = softmax(QKᵀ / √d_k) · V
- Q（Query）：当前位置的查询
- K（Key）：其他位置的键
- V（Value）：其他位置的值
- softmax(QKᵀ)计算相关性权重
- 加权求和V得到最终表示

为什么有效：
1. 长距离依赖：直接连接任意两个位置，不像RNN需要逐步传递
2. 动态权重：不同任务/输入有不同的关注点
3. 并行计算：所有位置可以同时计算（RNN必须顺序计算）
4. 可解释性：attention权重可视化模型关注了什么

从RNN+Attention到纯Attention（Transformer）的演进是NLP最重要的突破。
