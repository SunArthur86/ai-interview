---
id: misc-007
difficulty: L2
category: ai-basics
subcategory: 大模型原理
tags:
- IOC
feynman:
  essence: 引入门控机制和平滑激活函数,提升模型非线性表达能力。
  analogy: 神经网络装了智能阀门,能自主决定让哪些信息流过,比只管开关的非线性更好用。
  first_principle: 如何设计更高效的非经变换来提升特征提取能力?
  key_points:
  - SwiGLU = Swish激活 + 门控线性单元
  - 参数量增加3/2,但性能提升显著
  - 解决ReLU神经元"死亡"问题,梯度更平滑
follow_up:
- 为什么不用更复杂的激活函数?
- SwiGLU的三个矩阵维度如何设定?
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
