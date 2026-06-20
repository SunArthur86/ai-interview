---
id: ai-basics-s003
difficulty: L1
category: ai-basics
subcategory: 深度学习基础
images:
- svg_training.svg
feynman:
  essence: 模型死记硬背训练数据噪声，通过增大数据、限制容量和早停来提升泛化。
  analogy: 像背书只背了例题，换道题就不会了；多刷题、抓重点能治好。
  first_principle: 如何让模型学到通用规律而非训练集的特有噪声？
  key_points:
  - 过拟合源于模型复杂度超过数据蕴含的信息
  - 正则化限制模型权重幅度，增加约束
  - Early Stopping在泛化能力开始下降前停止
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
