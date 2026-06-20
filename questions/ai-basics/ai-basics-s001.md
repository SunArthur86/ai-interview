---
id: ai-basics-s001
difficulty: L2
category: ai-basics
subcategory: 深度学习基础
images:
- svg_training.svg
feynman:
  analogy: 传声筒游戏中，声音传得太远就听不见（消失）或变刺耳（爆炸）。
  first_principle: 如何在深层网络中保证有效信号反向传播？
  key_points:
  - 链式法则连乘导致梯度指数级变化
  - ReLU缓解消失，残差连接提供直通通路
  - 梯度裁剪是解决爆炸的有效手段
---

# 梯度消失和梯度爆炸的原因和解决方案？

梯度消失：深层网络中梯度通过反向传播逐层衰减，接近输入层的梯度几乎为0，导致参数无法更新。
梯度爆炸：梯度逐层放大，导致参数更新过大，模型不收敛。

原因：链式法则中多个梯度相乘。如果每层梯度<1，连乘后趋近0；如果>1，连乘后趋近无穷。

解决方案：
1. 激活函数：用ReLU（梯度为1）替代Sigmoid（最大梯度0.25）
2. 残差连接（ResNet）：梯度可以直接跳过层传播，解决深层梯度消失
3. BatchNorm/LayerNorm：归一化使梯度分布更稳定
4. 梯度裁剪：clip grad norm防止爆炸
5. 合理的权重初始化：Xavier初始化、He初始化
6. 残差连接是Transformer中使用残差连接的根本原因之一
