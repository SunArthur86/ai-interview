---
id: misc-038
difficulty: L2
category: ai-basics
subcategory: 多模态
feynman:
  essence: 通过对比学习打通图像与文本的语义空间，实现跨模态理解。
  analogy: 像训练翻译官，把“猫”的图片和“猫”这个词拉进同一个房间，把“狗”赶出去。
  first_principle: 如何让计算机理解图像内容并关联自然语言的语义概念？
  key_points:
  - 双塔架构分别编码图像和文本
  - 使用对比损失对齐正样本
  - 通过文本描述实现零样本分类
follow_up:
- CLIP的文本编码器和图像编码器维度如何对齐?
- SigLIP相比CLIP有什么改进?
---

# CLIP的原理是什么?为什么它能实现零样本图像分类

- **CLIP (Contrastive Language-Image Pre-training):**

- **核心思想:** 用对比学习将图像和文本对齐到同一向量空间.

- **训练:**
1. 图像编码器(ViT)+ 文本编码器(Transformer)
2. 对N对(图像,文本):匹配的对相似度高,不匹配的相似度低
3. InfoNCE Loss(对比损失)

- **零样本分类:**
1. 将所有类别名构造成文本:「一张{类别}的照片」
2. 编码所有类别文本
3. 编码输入图像
4. 选与图像相似度最高的类别

- **影响:**
- CLIP的图像编码器成为无数多模态模型的视觉骨干
- LLaVA/BLIP-2等VLM都使用CLIP ViT作为视觉编码器
