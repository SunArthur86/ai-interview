---
id: "mt-ai-008"
difficulty: "L3"
category: "llm-core"
categories:
  - "eng-practice"
  - "llm-core"
subcategory: "模型结构"
tags:
  - "美团"
  - "面经"
  - "Qwen"
  - "模型演进"
feynman:
  essence: "Qwen 的核心贡献是'把每个已知最好的技术都用上 + 用更多数据 + 开源完整生态'，逐步逼近 GPT-4 水平。"
  analogy: "Qwen 的策略像'集齐最强装备'的 RPG 玩家——GQA（加速）、RoPE（位置）、SwiGLU（激活）、YaRN（长上下文）、DPO（对齐）——每件都是当前版本最强，组合起来就是开源 SOTA。"
  key_points:
    - "Qwen-1：开源基线，中英双语强"
    - "Qwen-1.5：引入 GQA"
    - "Qwen-2：128K + 多语言"
    - "Qwen-2.5：18T 数据 + 垂直版本"
    - "生态：Coder/Math/VL 全覆盖"
first_principle:
  problem: "如何在开源框架下，逐步缩小与闭源顶级模型（GPT-4）的差距？"
  axioms:
    - "Scaling Law：更多数据 + 更多参数 = 更强能力"
    - "架构改进是渐进的——GQA/RoPE/SwiGLU 各贡献 5-10%"
    - "数据质量和多样性比参数量更重要"
  rebuild: "从'开源追赶闭源'角度出发：① 哪些架构改进可立即采用？② 数据规模和质量如何突破？③ 长上下文如何实现？④ 如何构建垂直版本（Coder/Math/VL）？"
follow_up:
  - "Qwen 和 LLaMA 架构有什么区别？—— Qwen 用 GQA（1.5起），LLaMA-2 用 MHA，LLaMA-3 才用 GQA"
  - "Qwen 的训练数据有多大？—— Qwen-2.5 约 18T tokens"
  - "Qwen-VL 是怎么做多模态的？—— ViT 编码图像 + 适配层对齐到语言空间"
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

**核心技术贡献汇总：**
| 方面 | 贡献 |
|------|------|
| 架构 | GQA + RoPE + SwiGLU 标准化 |
| 训练 | 大规模数据 + 课程学习 |
| 长度 | YaRN 长度外推 → 原生 128K |
| 多语言 | 29 种语言支持 |
| 对齐 | DPO + 多轮 RLHF |
| 生态 | Coder/Math/VL 多模态全家桶 |
