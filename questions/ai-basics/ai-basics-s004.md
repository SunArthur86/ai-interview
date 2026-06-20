---
id: ai-basics-s004
difficulty: L2
category: ai-basics
subcategory: 深度学习基础
feynman:
  essence: BN对batch归一化适合CV，LN对样本特征归一化适合NLP，Transformer选LN因独立于batch。
  analogy: BN是全班同学的成绩归一化，LN是你自己各科成绩的归一化。
  first_principle: 如何在训练中稳定数据分布以加速收敛？
  key_points:
  - BN依赖batch大小，受变长序列影响大
  - LN针对单个样本归一化，适合序列处理
  - RMSNorm是LN的去均值简化版，计算更高效
---

# Batch Normalization和Layer Normalization有什么区别？

BatchNorm：在batch维度上归一化。
- 对每个特征，计算batch内所有样本的均值和方差
- 适合CNN（图像分类）：同一channel的所有像素归一化
- 依赖batch size：batch太小时统计量不准
- 训练/推理不一致（推理用running统计量）

LayerNorm：在特征维度上归一化。
- 对每个样本，计算所有特征的均值和方差
- 适合RNN/Transformer：序列数据
- 不依赖batch size
- 训练/推理一致

为什么Transformer用LayerNorm不用BatchNorm？
1. 序列长度可变，BatchNorm在不同位置上统计量不一致
2. BatchNorm依赖batch size，LLM训练batch size可能很小
3. LayerNorm对每个token独立归一化，适合自回归生成

RMSNorm是LayerNorm的简化版，去掉中心化步骤，计算更快。
