---
id: "misc-022"
difficulty: "L1"
category: "ai-basics"
subcategory: "推理优化"
tags:
  - "IOC"
images:
  - "svg_speculative.svg"
feynman:
  essence: "- *核心思想:** 用小模型(草稿模型)快速生成候选token,大模型批量验证. - *流程:** 1. 小模型自回归生成k个token(快) 2. 大模型一"
  analogy: "Speculative Decoding 就像老板和助理配合——助理（小模型）快速起草 k 个候选，老板（大模型）一次批量审批，猜对的直接采纳（省 k-1 次推理），猜错的重写，总体快 2-3 倍。"
  key_points:
    - "核心思想: 用小模型(草稿模型)快速生成候选token,大模型批量验证."
    - "小模型自回归生成k个token(快)"
    - "大模型一次前向传播验证这k个token(并行)"
first_principle:
  problem: "剥离所有术语：Speculative Decoding的原理?为什么能加速2-3倍 底层在做什么？为什么这样做是最优的？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "草稿模型如何选择?"
  - "Eagle和Medusa有什么区别?"
---

# Speculative Decoding的原理是什么?为什么能加速2-3倍

- **核心思想:** 用小模型(草稿模型)快速生成候选token,大模型批量验证.

- **流程:**
1. 小模型自回归生成k个token(快)
2. 大模型一次前向传播验证这k个token(并行)
3. 如果小模型猜对了,直接采纳(省k-1次大模型推理)
4. 猜错的部分从小模型重新生成

- **关键:** 大模型验证和生成是并行的,不增加额外计算

- **Medusa改进:** 不用单独草稿模型,在大模型上增加多个head同时预测多个未来token

- **加速效果:** 2-3x(取决于小模型猜测准确率)
