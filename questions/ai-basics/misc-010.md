---
id: "misc-010"
difficulty: "L2"
category: "ai-basics"
subcategory: "训练与微调"
tags:
  - "IO"
feynman:
  essence: "- *LoRA (Low-Rank Adaptation):** 冻结原始权重W,在旁路添加低秩矩阵ΔA和ΔB: h = Wx + ΔA·ΔB·x 其中 ΔA∈"
  analogy: "微调就像给通才毕业生做岗前培训——已有基础能力（预训练），再针对具体岗位做专项训练（指令/偏好对齐）。"
  key_points:
    - "LoRA (Low-Rank Adaptation):"
    - "核心思想: 模型适配的权重更新ΔW是低秩的"
    - "全量微调: d×d 参数"
first_principle:
  problem: "剥离所有术语：LoRA的原理?rank r 如何选择?QLoRA做了什么改进 底层在做什么？为什么这样做是最优的？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "LoRA为什么用零初始化的高斯初始化?"
  - "QLoRA的NF4量化为什么比INT4好?"
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
