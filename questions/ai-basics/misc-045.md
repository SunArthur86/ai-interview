---
id: misc-045
difficulty: L2
category: ai-basics
subcategory: 大模型原理
images:
- svg_normalization.svg
feynman:
  essence: RMSNorm简化了LayerNorm去掉了均值减法，Pre-Norm解决了深层训练梯度消失。
  analogy: RMSNorm是省略了「平均分」计算的标准化；Pre-Norm是先清理再干活，避免越干越乱。
  first_principle: 如何在保证模型稳定训练的前提下，最大化计算效率并支持更深网络？
  key_points:
  - RMSNorm移去中心化减法，仅保留方差缩放，计算效率高。
  - Pre-Norm将LayerNorm置于残差连接之前，保证梯度顺畅传播。
  - 现代大模型标配：Pre-Norm结构配合RMSNorm归一化。
follow_up:
- DeepNorm如何解决Post-Norm的稳定性问题?
- 为什么Post-Norm在浅层模型中效果更好?
---

# 为什么LLaMA用RMSNorm而不是LayerNorm?Pre-Norm和Post-Norm有什么区别

- **RMSNorm vs LayerNorm:**

- **LayerNorm:** y = gamma * (x - mean) / √(var + eps) + beta
- **RMSNorm:** y = gamma * x / √(mean(x²) + eps)

- **RMSNorm优势:**
1. **计算更快** - 不需要计算均值,减少约7-64%计算
2. **效果相当** - 实验表明去掉减均值操作不影响效果
3. **更稳定** - 大模型训练中更稳定

- **Pre-Norm vs Post-Norm:**
- **Post-Norm**(原始Transformer):x = LayerNorm(x + SubLayer(x))
- 深层训练不稳定
- **Pre-Norm**(GPT-2/LLaMA):x = x + SubLayer(LayerNorm(x))
- **训练更稳定**,支持更深模型
- 效果略差但可通过增加深度补偿

- **所有现代大模型:** Pre-Norm + RMSNorm(LLaMA/GLM/Qwen/Mistral)
