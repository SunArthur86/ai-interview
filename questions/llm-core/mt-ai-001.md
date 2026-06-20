---
id: mt-ai-001
difficulty: L3
category: llm-core
categories:
- eng-practice
- llm-core
subcategory: 企业面试问答
tags:
- 美团
- 面经
- LLaMA
- 架构
feynman:
  essence: 移除冗余设计，用更优架构和更多数据提升小模型性能。
  analogy: 像给赛车减重（去Bias）并换高标号汽油（更多数据），让小排量引擎跑赢大排量。
  first_principle: 如何通过架构优化和数据配比，突破模型性能与参数规模的线性关系？
  key_points:
  - 架构：RMSNorm、RoPE、SwiGLU、去Bias
  - 策略：增加数据量胜过增加参数量
  - 影响：确立了现代开源LLM的标准架构
  - 训练：验证了Chinchilla缩放定律
follow_up:
- RMSNorm 和 LayerNorm 的区别是什么？—— RMSNorm 去掉了均值中心化，只做方差归一化，计算量更少
- SwiGLU 为什么比 GeLU 好？—— 门控机制让 FFN 有选择性传递信息，表达能力更强
- Pre-Norm 和 Post-Norm 哪个训练更稳定？—— Pre-Norm 更稳定，但理论上 Post-Norm 上限更高
---

# 【美团面经】说一下 LLaMA 的结构吧，它在结构和训练上都做了哪些贡献？

LLaMA 是 Meta 开源的一系列高效大语言模型，核心贡献在于"用更少参数+更多数据"达到甚至超越更大模型的性能。

**结构改进：**
1. **Pre-Norm 架构** — 使用 RMSNorm 替代 LayerNorm，且放在 Attention/FFN 之前（Pre-Norm），训练更稳定
2. **RoPE 旋转位置编码** — 替代绝对位置编码，支持长度外推，是当前主流位置编码方案
3. **SwiGLU 激活函数** — FFN 使用 SwiGLU（Swish + Gated Linear Unit），比 GeLU 表现更好
4. **无偏置** — 所有线性层去掉 bias，减少参数量，推理更快
5. **KV Cache 友好** — 标准自回归解码，KV Cache 高效

**训练贡献：**
1. **数据效率** — 证明用更多公开数据（1T~1.4T tokens）训练更小模型，推理成本更低
2. **开源生态** — 完整开源权重，推动整个开源社区发展（LLaMA → Alpaca → Vicuna → ...）
3. **Scaling Laws 验证** — 实际验证了 Chinchilla 的数据配比建议
