---
id: mt-ai-008
difficulty: L3
category: llm-core
categories:
- eng-practice
- llm-core
subcategory: 模型结构
tags:
- 美团
- 面经
- Qwen
- 模型演进
feynman:
  essence: 阿里通义千问系列的开源演进史，核心是架构标准化与数据规模扩展。
  analogy: 像汽车迭代，从普通轿车（Qwen-1）升级到超跑（Qwen-2.5），引擎架构优化且燃料更多。
  first_principle: 如何在保持开源领先的同时，平衡模型性能、长上下文能力与推理成本？
  key_points:
  - Qwen-1 奠定双语基础架构
  - Qwen-1.5 引入 GQA 推理加速
  - Qwen-2 实现长文本与多语言突破
  - Qwen-2.5 数据堆至 18T 达到 SOTA
follow_up:
- Qwen 和 LLaMA 架构有什么区别？—— Qwen 用 GQA（1.5起），LLaMA-2 用 MHA，LLaMA-3 才用 GQA
- Qwen 的训练数据有多大？—— Qwen-2.5 约 18T tokens
- Qwen-VL 是怎么做多模态的？—— ViT 编码图像 + 适配层对齐到语言空间
---

# 【美团面经】串一下 Qwen 系列，几版模型都做了哪些贡献？

**Qwen（通义千问）系列演进路线：**

**Qwen-1（2023.8）：**
- 参数：1.8B ~ 72B
- 架构：标准 Decoder-only + RoPE + SwiGLU
- 贡献：中英双语强、代码能力强、开源完整

**Qwen-1.5（2024.2）：**
- 参数：0.5B ~ 110B
- 改进：GQA（Grouped Query Attention）减少 KV Cache
- 训练：更大规模数据 + 更长上下文（32K）
- 贡献：性能接近 LLaMA-2，部分超越

**Qwen-2（2024.6）：**
- 参数：0.5B ~ 72B
- 改进：
  - 支持 128K 上下文（YaRN + DCA）
  - 多语言（29 种语言）
  - 更强的代码和数学能力
- 贡献：开源 SOTA，72B 接近 GPT-4 水平

**Qwen-2.5（2024.11）：**
- 参数：0.5B ~ 72B
- 改进：
  - 训练数据 18T tokens（大规模扩展）
  - 原生 128K 上下文
  - 代码能力接近专精模型（Qwen2.5-Coder）
  - 数学能力大幅提升（Qwen2.5-Math）
- 贡献：全面开源 SOTA，多个垂直版本

**核心技术架构演进：**
```text
┌─────────────┐    ┌───────────────────────┐    ┌───────────────────────┐
│  Qwen-1     │    │     Qwen-1.5          │    │    Qwen-2 / 2.5       │
│─────────────│    │───────────────────────│    │───────────────────────│
│ MHA / MQA   │───►│ GQA (Grouped Query)   │───►│ GQA + Rope Scaling     │
│ SwiGLU      │    │ SwiGLU                │    │ SwiGLU                │
│ 8K Context  │    │ 32K Context           │    │ 128K (YaRN/DCA)       │
└─────────────┘    └───────────────────────┘    └───────────────────────┘
       │                    │                            │
       ▼                    ▼                            ▼
  Base Release      Cache Effort Up         Long Context & Multilingual
```

**核心技术贡献汇总：**
| 方面 | 贡献 |
|------|------|
| 架构 | GQA + RoPE + SwiGLU 标准化 |
| 训练 | 大规模数据 + 课程学习 |
| 长度 | YaRN 长度外推 → 原生 128K |
| 多语言 | 29 种语言支持 |
| 对齐 | DPO + 多轮 RLHF |
| 生态 | Coder/Math/VL 多模态全家桶 |

## 常见考点
1. **GQA (Grouped Query Attention) 的优势**：相比 MHA 和 MQA，它在推理速度和模型效果之间是如何取得平衡的（KV Cache 显存占用减少，同时保持性能）？
2. **长文本外推技术 YaRN**：它是如何在不重新训练全量长度的情况下扩展上下文窗口的（RoPE 基于位置插值的改进）？
3. **MoE 架构相关**：Qwen2 是否引入了 MoE？（当前版本 Qwen2 主要是 Dense，但 Qwen1.5-MoE 曾尝试，注意区分）
4. **数据规模效应**：Qwen2.5 使用 18T tokens 训练，体现了 Scaling Laws（缩放定律）的什么结论？
