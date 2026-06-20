---
id: "misc-007"
difficulty: "L2"
category: "ai-basics"
subcategory: "大模型原理"
tags:
  - "IOC"
feynman:
  essence: "- *SwiGLU = Swish + GLU (Gated Linear Unit)** - *公式对比:** - ReLU: max(0, x) - GEL"
  analogy: "激活函数就像神经元的开关——ReLU 是硬开关（<0 关 >0 开），GELU/SwiGLU 是带门控的旋钮，更平滑更精细。"
  key_points:
    - "SwiGLU = Swish + GLU (Gated Linear Unit)"
    - "ReLU: max(0, x)"
    - "GELU: x · Φ(x) - BERT/GPT使用"
first_principle:
  problem: "追根溯源：为什么现代大模型(LLaMA/GLM)用SwiGLU替代ReLU/GELU作为FFN激活函数 的根本原因是什么？背后的设计哲学是什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "为什么不用更复杂的激活函数?"
  - "SwiGLU的三个矩阵维度如何设定?"
---

# 为什么现代大模型(LLaMA/GLM)用SwiGLU替代ReLU/GELU作为FFN激活函数

- **SwiGLU = Swish + GLU (Gated Linear Unit)**

- **公式对比:**
- ReLU: max(0, x)
- GELU: x · Φ(x) - BERT/GPT使用
- **SwiGLU:** (xW₁ · Swish(xW₂)) · xW₃
- Swish(x) = x · sigmoid(x)
- 三组权重矩阵,门控机制

- **优势:**
1. **门控机制** - 自适应信息过滤,模型可学习保留/丢弃特征
2. **平滑梯度** - Swish处处可导,无ReLU的死神经元问题
3. **实验验证** - 同等参数量下,SwiGLU下游任务优于ReLU/GELU

- **代价:** FFN参数量增加(从2个矩阵变为3个),可通过缩小hidden_dim补偿

- **实际应用:** LLaMA/GLM/Mistral/Qwen 全部使用SwiGLU
