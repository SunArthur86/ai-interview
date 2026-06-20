---
id: mt-ai-012
difficulty: L4
category: llm-core
categories:
- eng-practice
- llm-core
subcategory: 企业面试问答
tags:
- 美团
- 面经
- 论文阅读
- 技术深度
feynman:
  essence: 通过精读经典论文掌握技术本质，并具备工程化落地的转化能力。
  analogy: 像练武功要练马步一样，Transformer、LoRA 是基础内功，练好了才能学新招式。
  first_principle: 如何从海量文献中提取核心原理，并将其转化为解决实际工程问题的工具？
  key_points:
  - Transformer 是大模型的基石
  - LoRA 是高效微调的必修课
  - DPO 是当前对齐的主流方案
  - 不仅要读，还要复现和批判思考
  - 能将论文原理应用到实际工程中
follow_up:
- 论文那么多怎么选？—— 关注 NeurIPS/ICML/ACL/ICLR + arXiv 热门 + Hugging Face 趋势
- 怎么高效读论文？—— 第一遍只读 Abstract+Intro+Conclusion+Figure，值得深入再精读
- 要不要复现论文？—— 核心论文建议复现关键实验，加深理解
---

# 【美团面经】近一年读过什么 AI 论文/技术报告两次以上？对你有什么帮助？

**高频阅读论文推荐（面试回答参考）：**

**必读论文（建议读 3 遍以上）：**

1. **"Attention Is All You Need"** (2017)
   - Transformer 原始论文，理解 Self-Attention/Multi-Head/Positional Encoding
   - 帮助：理解所有后续大模型（BERT/GPT）的架构基础，掌握 Q/K/V 机制

2. **"RoFormer: Enhanced Transformer with Rotary Position Embedding"** (2021)
   - RoPE 原始论文
   - 帮助：理解位置编码设计原理和长度外推，现在主流模型（Llama/Qwen）都在用

3. **"LoRA: Low-Rank Adaptation of Large Language Models"** (2021)
   - 参数高效微调经典
   - 帮助：理解微调的数学原理和工程实现，节省显存

4. **"Direct Preference Optimization"** (DPO, 2023)
   - 无需 RM 的对齐方法
   - 帮助：理解 RLHF 的替代方案和偏好优化数学原理，SFT 后必备

5. **DeepSeek-V2/V3 技术报告** (2024) / Llama 3 Report
   - MLA + MoE + 训练细节
   - 帮助：理解 SOTA 开源模型的工程创新（如 MLA 如何节省 KV Cache 显存）

**Transformer 计算流程可视化（对应 Attention 论文）：**

```
┌──────────────────────────────────────────────────────────────────┐
│                    Self-Attention Mechanism                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Input X (Seq_Len, Dim)                                         │
│      │                                                           │
│      ├──> W_Q  (Linear) ──> Query (Q)                            │
│      ├──> W_K  (Linear) ──> Key   (K)                            │
│      └──> W_V  (Linear) ──> Value (V)                            │
│                      │                                           │
│                      ▼                                           │
│            Attention Score = Q * K^T / sqrt(d_k)                 │
│                      │                                           │
│                      ▼                                           │
│            Weighted Score = Softmax(Score)                      │
│                      │                                           │
│                      ▼                                           │
│              Output = Weighted Score * V                         │
│                      │                                           │
└──────────────────────────────────────────────────────────────────┘
```

**## 常见考点**
1. **RoPE 细节**：面试官常问 RoPE 如何实现相对位置编码？（通过复数域的旋转矩阵相乘，将绝对位置编码转换为相对位置感知）。
2. **长度外推**：为什么 Llama 用 RoPE 后还是会有长度限制？（旋转角度的 base 值导致远距离位置区分度下降，解决方案如 NTK-aware scaling）。
3. **KV Cache 优化**：DeepSeek 的 MLA（Multi-Head Latent Attention）是如何省显存的？（将 Key/Value 压缩到低维 latent vector，推理时再解压，大幅减少 Cache 大小）。
4. **DPO vs PPO**：DPO 为什么不需要训练 Reward Model？（DPO 通过解析 RLHF 的目标函数，推导出可以直接用偏好数据优化的 Loss 函数，隐式包含了奖励模型）。
5. **MoE 负载均衡**：在 DeepSeek MoE 架构中，如何避免专家负载不均？（Auxiliary Loss 均衡专家负载，以及细粒度专家切分策略）。
