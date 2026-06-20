---
id: "ai-basics-s004"
difficulty: "L2"
category: "ai-basics"
subcategory: "深度学习基础"
feynman:
  essence: "BatchNorm依赖batch size，LLM训练batch size可能很小。"
  analogy: "归一化就像统一度量衡——把不同量级的数据拉到同一尺度，让训练更稳定、梯度流动更顺畅。"
  key_points:
    - "BatchNorm：在batch维度上归一化"
    - "- 对每个特征，计算batch内所有样本的均值和方差 - 适合CNN（图像分类）：同一channel的所有像素归一化 - 依赖batch size：batch太小时统计量不准 - 训练/推理不一致（推"
    - "- 对每个样本，计算所有特征的均值和方差 - 适合RNN/Transformer：序列数据 - 不依赖batch size - 训练/推理一致 为什么Transformer用LayerNorm不用Ba"
first_principle:
  problem: "它们本质上为什么不同？各自的设计目标和适用场景是什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
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
