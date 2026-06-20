---
id: "misc-039"
difficulty: "L2"
category: "ai-basics"
subcategory: "多模态"
tags:
  - "IO"
  - "IOC"
feynman:
  essence: "LLaVA 的架构：视觉编码器（CLIP ViT-L/14）把图片编码成 patch token → 一个可训练的投影层（MLP）把视觉 token 对齐到 LLM 的词嵌入空间 → 拼接到文本 token 后喂给 LLM（Vicuna/LLaMA）做理解与生成；训练分两阶段：特征对齐预训练 + 指令微调。"
  analogy: "大语言模型就像读过整个互联网的学者——通过预测「下一个词」生成文本，积累了海量语言模式和知识。"
  key_points:
    - "视觉编码器 - CLIP ViT-L/14,输出576个patch token"
    - "投影层 - 线性层/MLP,将视觉特征映射到LLM的embedding空间"
    - "LLM - LLaMA/Vicuna,处理文本+视觉token"
first_principle:
  problem: "为什么需要 LLaVA的架构?它是如何将视觉信息接入LLM的？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "Projection Layer用线性层还是MLP好?"
  - "BLIP-2的Q-Former和LLaVA的Projection有什么区别?"
---

# LLaVA的架构是什么?它是如何将视觉信息接入LLM的

- **LLaVA架构:**

```
图像 → CLIP ViT编码器 → 图像特征 → Projection Layer → LLM(Vicuna/LLaMA)
↓
文本输出
```

- **核心组件:**
1. **视觉编码器** - CLIP ViT-L/14,输出576个patch token
2. **投影层** - 线性层/MLP,将视觉特征映射到LLM的embedding空间
3. **LLM** - LLaMA/Vicuna,处理文本+视觉token

- **训练阶段:**
1. **Stage 1(对齐)** - 只训练Projection Layer,用595K图文对
2. **Stage 2(指令微调)** - 冻结视觉编码器,训练Projection+LLM

- **为什么有效:**
- CLIP已经对齐了图文语义
- 只需一个简单投影层就能接入LLM
- 用GPT-4生成多模态指令数据训练

- **后续发展:** LLaVA-1.5 (MLP投影), LLaVA-NeXT (高分辨率), LLaVA-Video
