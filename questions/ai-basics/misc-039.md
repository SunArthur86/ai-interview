---
id: misc-039
difficulty: L2
category: ai-basics
subcategory: 多模态
tags:
- IO
- IOC
feynman:
  essence: 通过简单的投影层将视觉特征对齐到语言模型的词向量空间。
  analogy: 像给只有文字界面的电脑接个“显卡转接头”，让它能看懂图片。
  first_principle: 如何赋予纯语言大模型“看懂”图像并生成语言描述的能力？
  key_points:
  - CLIP提取图像特征
  - 投影层映射特征到词嵌入空间
  - 两阶段训练：特征对齐+指令微调
follow_up:
- Projection Layer用线性层还是MLP好?
- BLIP-2的Q-Former和LLaVA的Projection有什么区别?
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
