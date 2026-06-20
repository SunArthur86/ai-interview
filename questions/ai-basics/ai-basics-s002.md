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
