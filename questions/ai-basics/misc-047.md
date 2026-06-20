---
id: misc-047
difficulty: L2
category: ai-basics
subcategory: 训练与微调
tags:
- IOC
feynman:
  essence: 将大模型的“暗知识”（类间关系和推理过程）迁移给小模型。
  analogy: 老师不只告诉你答案是A，还告诉你B错在哪、C差多少，让你学得更透彻。
  first_principle: 如何保留大模型的知识精髓，同时实现小模型的高效部署？
  key_points:
  - 软标签：包含各类概率的平滑分布，蕴含类间相似度信息。
  - CoT蒸馏：直接学习大模型的思维链步骤，习得推理能力。
  - 目的：在保持性能的前提下，大幅压缩模型参数和推理成本。
follow_up:
- 蒸馏和量化的区别?
- 如何选择Teacher模型?
---

# 知识蒸馏在大模型中如何应用?软标签和硬标签的区别是什么

- **知识蒸馏:** 用大模型(Teacher)的输出训练小模型(Student).

- **软标签 vs 硬标签:**
- **硬标签:** one-hot向量 [0, 0, 1, 0] - 信息量少
- **软标签:** 概率分布 [0.1, 0.05, 0.8, 0.05] - 包含类间关系(dark knowledge)

- **温度参数T:** softmax(logits/T),T越大分布越平滑

- **大模型蒸馏方案:**

1. **输出蒸馏** - Student模仿Teacher的输出分布
- Loss = KL(softmax(z_T/T) || softmax(z_S/T))

2. **CoT蒸馏** - 用Teacher生成的思维链训练Student
- DeepSeek-R1-Distill:R1的推理能力蒸馏到7B/14B/32B

3. **特征蒸馏** - Student模仿Teacher的中间层表示

- **效果:**
- R1-Distill-7B 在AIME上达到55.5%(接近o1-mini的56.4%)
- 小模型+蒸馏可以接近大模型的推理能力
