---
id: "misc-038"
difficulty: "L2"
category: "ai-basics"
subcategory: "多模态"
feynman:
  essence: "- *CLIP (Contrastive Language-Image Pre-training):** - *核心思想:** 用对比学习将图像和文本对齐到同一"
  analogy: "Transformer 就像高效的读书小组——每个人（注意力头）同时读不同段落，然后交流关键信息，不像 RNN 逐字读。"
  key_points:
    - "CLIP (Contrastive Language-Image Pre-training):"
    - "核心思想: 用对比学习将图像和文本对齐到同一向量空间."
    - "图像编码器(ViT)+ 文本编码器(Transformer)"
first_principle:
  problem: "剥离所有术语：CLIP的原理?为什么它能实现零样本图像分类 底层在做什么？为什么这样做是最优的？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "CLIP的文本编码器和图像编码器维度如何对齐?"
  - "SigLIP相比CLIP有什么改进?"
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
