---
id: "misc-040"
difficulty: "L2"
category: "ai-basics"
subcategory: "多模态"
tags:
  - "IO"
  - "IOC"
feynman:
  essence: "- *扩散模型原理:** - *前向过程(加噪):** - 逐步向图像添加高斯噪声 - x_t = √(alpha_t) * x_0 + √(1-a"
  analogy: "Diffusion 就像从噪点中雕刻图片——先撒满噪点再逐步去噪，慢慢浮现目标图像。"
  key_points:
    - "逐步向图像添加高斯噪声"
    - "x_t = √(alpha_t) * x_0 + √(1-alpha_t) * noise"
    - "训练U-Net学习从噪声中恢复图像"
first_principle:
  problem: "为什么需要 扩散模型(Diffusion)的前向和反向过程?为什么U-Net是核心架构？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "Latent Diffusion为什么比像素空间扩散快?"
  - "DALL-E 3和Stable Diffusion有什么区别?"
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
