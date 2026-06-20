---
id: misc-040
difficulty: L2
category: ai-basics
subcategory: 多模态
tags:
- IO
- IOC
feynman:
  essence: 通过学习从噪声中逐步去噪来生成数据，U-Net负责预测噪声。
  analogy: 像把一杯清水（图像）搅浑成泥水（噪声），再训练魔法倒流还原清水。
  first_principle: 如何从随机噪声中逐步构建出符合真实分布的高质量图像？
  key_points:
  - 前向加噪，反向去噪
  - U-Net预测噪声并通过跳跃连接保留细节
  - 潜空间扩散大幅降低计算成本
follow_up:
- Latent Diffusion为什么比像素空间扩散快?
- DALL-E 3和Stable Diffusion有什么区别?
---

# 扩散模型(Diffusion)的前向和反向过程是什么?为什么U-Net是核心架构

- **扩散模型原理:**

- **前向过程(加噪):**
- 逐步向图像添加高斯噪声
- x_t = √(alpha_t) * x_0 + √(1-alpha_t) * noise
- 经过T步后变成纯噪声

- **反向过程(去噪):**
- 训练U-Net学习从噪声中恢复图像
- 给定x_t,预测噪声epsilon
- p(x_{t-1}|x_t) = N(mu_theta(x_t, t), sigma)

- **U-Net为什么核心:**
1. **编码器-解码器结构** - 捕获多尺度特征
2. **跳跃连接** - 保留高频细节
3. **时间嵌入** - AdaLN注入时间步信息
4. **交叉注意力** - 注入文本条件(文本到图像)

- **Stable Diffusion改进:**
- 在**潜空间**而非像素空间扩散(VAE编码后做扩散)
- 计算量减少64倍(512x512→64x64潜空间)
