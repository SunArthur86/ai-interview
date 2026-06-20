---
id: "ai-basics-s002"
difficulty: "L1"
category: "ai-basics"
subcategory: "深度学习基础"
images:
  - "svg_training.svg"
feynman:
  essence: "均方误差（MSE）：L = (y - ŷ)² - 用于回归问题 - 假设噪声是高斯分布 - 梯度 = 2(y - ŷ)·∂ŷ/∂θ 交叉熵损失（Cross-En"
  analogy: "Softmax 就像投票分配——把一组分数变成概率分布（总和=1），分最高的获最大概率。"
  key_points:
    - "梯度 = 2(y - ŷ)·∂ŷ/∂θ"
    - "配合Softmax使用"
    - "梯度 = ŷ - y（简洁、稳定）"
first_principle:
  problem: "它们本质上为什么不同？各自的设计目标和适用场景是什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
---

# 交叉熵损失和均方误差有什么区别？什么时候用哪个？

均方误差（MSE）：L = (y - ŷ)²
- 用于回归问题
- 假设噪声是高斯分布
- 梯度 = 2(y - ŷ)·∂ŷ/∂θ

交叉熵损失（Cross-Entropy）：L = -Σ y_i · log(ŷ_i)
- 用于分类问题
- 配合Softmax使用
- 梯度 = ŷ - y（简洁、稳定）

为什么分类不用MSE？
1. MSE + Sigmoid的梯度包含sigmoid导数项（最大0.25），容易梯度消失
2. Cross-Entropy + Softmax的梯度是(ŷ - y)，与预测误差成正比，训练更高效
3. 信息论角度：Cross-Entropy衡量两个概率分布的差异，更适合分类

LLM训练用Cross-Entropy（下一个token预测是多分类问题）。
