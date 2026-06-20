---
id: "mt-ai-001"
difficulty: "L3"
category: "llm-core"
categories:
  - "eng-practice"
  - "llm-core"
subcategory: "企业面试问答"
tags:
  - "美团"
  - "面经"
  - "LLaMA"
  - "架构"
feynman:
  essence: "LLaMA 的贡献是用 RoPE + RMSNorm + SwiGLU + Pre-Norm 四个架构优化，加上\"小模型大数据\"策略，证明了 7B 参数也能媲美 13B+ 模型。"
  analogy: "就像造跑车——不靠堆排量（参数量），而是靠更轻的车身（去bias）、更好的空气动力学（RoPE）、更高效的引擎（SwiGLU），用更少燃料跑出同样速度。"
  key_points:
    - "RMSNorm 替代 LayerNorm，Pre-Norm 布局"
    - "RoPE 旋转位置编码替代绝对编码"
    - "SwiGLU 激活函数提升 FFN 效果"
    - "去掉所有 bias 减参数"
    - "核心思想：小模型 + 大数据 = 高效率"
first_principle:
  problem: "为什么 LLaMA 用更少参数能超越更大的模型？架构上哪些改进是必要的？"
  axioms:
    - "Chinchilla Law：最优训练需要 ~20 tokens/参数，数据量比参数量更重要"
    - "Pre-Norm 梯度流更直接 → 深层网络训练更稳定"
    - "RoPE 的旋转不变性 → 自然支持相对位置 + 长度外推"
  rebuild: "从 Scaling Law 出发：① 参数 vs 数据的最优配比是什么？② 哪些架构组件可以提升参数效率？③ 推理时哪些计算可以省去（bias/均值）？④ 位置编码如何同时满足训练效率和泛化？"
follow_up:
  - "RMSNorm 和 LayerNorm 的区别是什么？—— RMSNorm 去掉了均值中心化，只做方差归一化，计算量更少"
  - "SwiGLU 为什么比 GeLU 好？—— 门控机制让 FFN 有选择性传递信息，表达能力更强"
  - "Pre-Norm 和 Post-Norm 哪个训练更稳定？—— Pre-Norm 更稳定，但理论上 Post-Norm 上限更高"
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
