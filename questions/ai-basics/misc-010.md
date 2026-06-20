---
id: misc-010
difficulty: L2
category: ai-basics
subcategory: 训练与微调
tags:
- IO
feynman:
  essence: 冻结主干,通过低秩矩阵旁路更新,实现高效参数微调。
  analogy: 给大衣打补丁,不用重做整件衣服,只需缝几块小布料就能改样式。
  first_principle: 如何在极小显存开销下实现大模型的高效适配?
  key_points:
  - 只训练新增的低秩矩阵,大幅降低显存需求
  - 秩r越大,表达能力越强
  - QLoRA将基座量化至4bit,进一步降低门槛
follow_up:
- LoRA为什么用零初始化的高斯初始化?
- QLoRA的NF4量化为什么比INT4好?
---

# LoRA的原理是什么?rank r 如何选择?QLoRA做了什么改进

- **LoRA (Low-Rank Adaptation):**

冻结原始权重W,在旁路添加低秩矩阵ΔA和ΔB:
h = Wx + ΔA·ΔB·x
其中 ΔA∈ℝ^(d×r), ΔB∈ℝ^(r×d), r << d

- **核心思想:** 模型适配的权重更新ΔW是低秩的

- **参数量对比:**
- 全量微调: d×d 参数
- LoRA: 2×d×r 参数(r=8时仅0.1%)

- **rank r选择:**
- r=4-8:简单任务/风格迁移
- r=16-64:复杂任务/知识注入
- r>64:基本接近全量微调效果

- **QLoRA改进:**
1. 基座模型4-bit量化(NF4)
2. LoRA层保持FP16/BF16
3. Paged Optimizer防止显存溢出
4. **效果:** 70B模型可在单张48GB GPU微调,质量接近全量

- **适用场景:** 资源有限/多任务部署/快速实验
