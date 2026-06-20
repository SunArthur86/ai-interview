---
id: "misc-045"
difficulty: "L2"
category: "ai-basics"
subcategory: "大模型原理"
images:
  - "svg_normalization.svg"
feynman:
  essence: "- *RMSNorm vs LayerNorm:** - *LayerNorm:** y = gamma * (x - mean) / √(var + e"
  analogy: "归一化就像统一度量衡——把不同量级的数据拉到同一尺度，训练更稳定。"
  key_points:
    - "RMSNorm vs LayerNorm:"
    - "LayerNorm: y = gamma * (x - mean) / √(var + eps) + beta"
    - "RMSNorm: y = gamma * x / √(mean(x²) + eps)"
first_principle:
  problem: "追根溯源：为什么LLaMA用RMSNorm而不是LayerNorm?Pre-Norm和Post-Norm有什么区别 的根本原因是什么？背后的设计哲学是什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "DeepNorm如何解决Post-Norm的稳定性问题?"
  - "为什么Post-Norm在浅层模型中效果更好?"
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
