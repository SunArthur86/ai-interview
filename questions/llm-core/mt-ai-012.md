---
id: "mt-ai-012"
difficulty: "L4"
category: "llm-core"
categories:
  - "eng-practice"
  - "llm-core"
subcategory: "企业面试问答"
tags:
  - "美团"
  - "面经"
  - "论文阅读"
  - "技术深度"
feynman:
  essence: "面试官问这个问题，是在考察你是否有'深度学习'的习惯——不是泛泛浏览，而是反复精读、批判思考、工程转化。"
  analogy: "就像厨师试菜——吃一口知道好不好吃（第一遍），研究配料和做法（第二遍），自己改良做出更好的菜（第三遍+实践）。"
  key_points:
    - "三遍法：快速浏览→精读方法→批判思考"
    - "必读：Transformer/RoPE/LoRA/DPO/DeepSeek"
    - "联系项目实践是加分项"
    - "能说局限和改进方向"
first_principle:
  problem: "论文阅读的目的不是'读过'，而是建立从理论到工程的转化能力。面试官想看你如何把论文变成生产力。"
  axioms:
    - "深度 > 广度——精读 3 篇比泛读 30 篇更有价值"
    - "理论→实践的转化能力是稀缺的"
    - "批判性思维——能说局限比能复述更有价值"
  rebuild: "从'论文的价值'出发：① 为什么有些论文值得读 3 遍（底层原理 vs 小改进）？② 每遍读的目标不同（了解→理解→批判）？③ 怎么从论文中提取工程价值？④ 怎么在面试中高效展示这种能力？"
follow_up:
  - "论文那么多怎么选？—— 关注 NeurIPS/ICML/ACL/ICLR + arXiv 热门 + Hugging Face 趋势"
  - "怎么高效读论文？—— 第一遍只读 Abstract+Intro+Conclusion+Figure，值得深入再精读"
  - "要不要复现论文？—— 核心论文建议复现关键实验，加深理解"
---

# 【美团面经】近一年读过什么 AI 论文/技术报告两次以上？对你有什么帮助？

**高频阅读论文推荐（面试回答参考）：**

**必读论文（建议读 3 遍以上）：**

1. **"Attention Is All You Need"** (2017)
   - Transformer 原始论文，理解 Self-Attention/Multi-Head/Positional Encoding
   - 帮助：理解所有后续大模型的架构基础

2. **"RoFormer: Enhanced Transformer with Rotary Position Embedding"** (2021)
   - RoPE 原始论文
   - 帮助：理解位置编码设计原理和长度外推

3. **"LoRA: Low-Rank Adaptation of Large Language Models"** (2021)
   - 参数高效微调经典
   - 帮助：理解微调的数学原理和工程实现

4. **"Direct Preference Optimization"** (DPO, 2023)
   - 无需 RM 的对齐方法
   - 帮助：理解 RLHF 的替代方案和偏好优化数学

5. **DeepSeek-V2/V3 技术报告** (2024)
   - MLA + MoE + 训练细节
   - 帮助：理解 SOTA 开源模型的工程创新

**面试回答模板：**
```
我重点读了 XX 论文/技术报告。

第一遍（快速浏览）：
  - 了解核心贡献和创新点
  - 判断是否值得深入

第二遍（精读方法）：
  - 逐节理解技术细节
  - 推导关键公式
  - 复现核心实验

第三遍（批判性思考）：
  - 这篇论文的局限性？
  - 和 XX 方法对比优劣？
  - 在我们项目中能怎么用？

帮助：
  - 理解了 XX 原理，在项目 YY 中解决了 ZZ 问题
  - 建立了从论文到工程的转化能力
```

**加分点：**
- 能说出论文的**局限和改进方向**
- 能联系到**自己的项目实践**
- 能对比**相关工作**的异同
- 能讨论**工程落地**的细节
