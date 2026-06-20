---
id: mt-ai-006
difficulty: L4
category: llm-core
categories:
- eng-practice
- llm-core
subcategory: 位置编码
tags:
- 美团
- 面经
- Qwen
- 长度外推
feynman:
  essence: 利用YaRN等插值技术，动态调整RoPE频率以适应更长文本。
  analogy: 像拉伸皮筋，不同部位拉伸力度不同（频率相关），保证拉长后不断裂也不变形。
  first_principle: 如何让基于短文本训练的位置编码，平滑地扩展到长文本而不产生崩塌？
  key_points:
  - 早期：NTK-aware RoPE 插值
  - Qwen2：引入YaRN，分频率插值
  - Qwen2.5：直接增加长文本训练数据
  - 核心：平衡高频局部信息和低频全局信息
follow_up:
- NTK-aware 和 YaRN 的区别？—— NTK 统一缩放所有维度，YaRN 分频段处理
- 长度外推会损失质量吗？—— 会，特别是长序列的精确召回任务（如 needle-in-haystack）
- 为什么不直接训练更长的序列？—— 训练成本随序列长度平方增长（Attention 复杂度）
---

# 【美团面经】Qwen 是怎么做长度外推的？

**Qwen 系列在长度外推上的方案演进：**

**1. 早期 Qwen（7B/14B）：**
- 基础训练长度 2K/8K
- 使用 RoPE + NTK-aware 插值
- 对超过训练长度的输入做位置缩放

**2. Qwen2（2024）：**
- 引入 **Dual Chunk Attention (DCA)**（与 YARN 类似）
- 将注意力分为 chunk 内和 chunk 间两部分
- 训练长度 32K → 推理可达 128K
- 使用 **YaRN**（Yet another RoPE extensioN）：
  - 对 RoPE 的不同频率维度采用不同插值策略
  - 高频维度（局部信息）：直接外推
  - 低频维度（全局信息）：线性插值
  - 中频维度：平滑过渡

**3. Qwen2.5（2024末）：**
- 训练阶段直接加入长序列数据
- 支持 128K 原生长度
- 配合 GQA 减少 KV Cache

**核心技术：YaRN 原理**
```
原始 RoPE: θ_i = base^(-2i/d)
YaRN:      θ_i' = θ_i / s(λ_i)

λ_i 控制插值强度:
  λ → 0: 高频维度不缩放（保留局部精度）
  λ → 1: 低频维度线性缩放（安全外推）
```
