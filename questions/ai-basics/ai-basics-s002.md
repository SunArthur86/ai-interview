---
id: ai-basics-s002
difficulty: L1
category: ai-basics
subcategory: 深度学习基础
images:
- svg_training.svg
feynman:
  essence: MSE测数值距离用于回归，Cross-Entropy测概率分布差异用于分类，后者梯度性质更好。
  analogy: MSE算打靶偏离中心的距离，Cross-Entropy算预测是猫还是狗的概率差。
  first_principle: 如何定义损失函数以最大化模型预测的正确概率？
  key_points:
  - MSE假设高斯噪声，适合回归任务
  - Cross-Entropy导数简单，避免梯度消失
  - 分类本质是概率分布匹配，故用交叉熵
---

# 交叉熵损失和均方误差有什么区别？什么时候用哪个？

均方误差（MSE）：L = 1/N Σ (y - ŷ)²
- **核心原理**：基于最大似然估计（MLE），假设误差服从高斯分布。
- **适用场景**：回归问题（预测连续值）。
- **梯度特性**：∂L/∂ŷ = 2(ŷ - y)。梯度随误差减小而减小，收敛平稳但在极小值附近震荡。
- **凸性质**：对于线性模型是凸函数，有全局最优解；但在非凸（如深层网络）中仍有局部最优。

交叉熵损失：L = - Σ y_i · log(ŷ_i)
- **核心原理**：基于最大似然估计，假设样本服从多项式分布（伯努利分布的推广）。来源于信息论中的KL散度，衡量两个概率分布的差异。
- **适用场景**：分类问题（二分类用Sigmoid，多分类用Softmax）。
- **梯度特性**：配合Softmax时，∂L/∂z_i = ŷ_i - y_i（z为logits）。梯度仅与误差成正比，与Sigmoid导数无关，更新更稳健。

**为什么分类不用MSE？（深入原理）**
1. **梯度消失问题**：
   - MSE + Sigmoid 的梯度链：`(ŷ - y) * Sigmoid'(z)`。
   - Sigmoid导数最大值为0.25（在z=0处），当神经元饱和（|z|大）时趋近0，导致深层网络无法有效更新。
   - Cross-Entropy 梯度中的 `(ŷ - y)` 项直接抵消了Sigmoid导数中的衰减因子，避免了非饱和区域的梯度消失。
2. **优化地形**：MSE在分类问题中通常会产生大量非零梯度的平坦区域（Plateaus），导致收敛极慢；而交叉熵能提供更大的梯度信号，加速收敛。
3. **概率意义**：分类本质是概率分布拟合。Cross-Entropy直接优化概率分布的对数似然，而MSE优化的是数值距离，忽略了分类的概率语义。

**应用扩展**：
- LLM训练：本质上是一个超大规模的多分类任务（词汇表大小V通常为50k+），因此必然使用Cross-Entropy。
- Label Smoothing：Cross-Entropy的改进版，将标签从硬标签（0/1）改为软标签（如0.1/0.9），防止模型过自信，提升泛化能力。

---

## 常见考点
1. **为什么Cross-Entropy比MSE收敛快？**（答：MSE梯度包含导数项，导致平坦区；CE梯度与误差线性相关）
2. **Hinge Loss vs Cross-Entropy？**（答：SVM用Hinge Loss关注支持向量（最大间隔），CE关注概率校准；CE更适合概率输出，Hinge适合硬分类）
3. **二分类用Sigmoid还是Softmax？**（答：数学上等价，Softmax是Sigmoid的归一化形式；多分类必须用Softmax）
