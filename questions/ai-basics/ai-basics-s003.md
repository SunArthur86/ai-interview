---
id: "ai-basics-s003"
difficulty: "L1"
category: "ai-basics"
subcategory: "深度学习基础"
images:
  - "svg_training.svg"
feynman:
  essence: "过拟合指模型在训练集上表现很好但在测试集/新数据上泛化差，本质是模型把训练数据的噪声也「记住了」。防止方法：① 增加数据量与数据增强；② 正则化（L1/L2、Dropout）；③ 早停（Early Stopping）；④ 降低模型复杂度；⑤ Batch Normalization；⑥ 交叉验证选模型。"
  analogy: "Batch Size 就像大巴车座位数——太少跑得频繁效率低，太多转弯难（内存不够）。"
  key_points:
    - "数据增强：翻转、裁剪、Mixup"
    - "正则化：L1/L2正则化（权重衰减）"
    - "Dropout：随机丢弃神经元（训练时）"
first_principle:
  problem: "为什么需要 过拟合？如何防止？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
---

# 什么是过拟合？如何防止？

过拟合：模型在训练集表现好但泛化差。

原因：模型容量太大、训练数据少、训练时间太长。

防止方法：

1. 数据层面：
- 数据增强：翻转、裁剪、Mixup
- 更多数据：收集或生成
- 正则化：L1/L2正则化（权重衰减）

2. 模型层面：
- Dropout：随机丢弃神经元（训练时）
- 降低模型复杂度：减少层数/参数
- BatchNorm/LayerNorm

3. 训练层面：
- Early Stopping：验证集loss上升时停止
- 学习率调度：余弦退火、warmup

4. 集成方法：
- Bagging、Boosting、模型集成

LLM中的正则化：Dropout、权重衰减（weight decay）、Label Smoothing。
