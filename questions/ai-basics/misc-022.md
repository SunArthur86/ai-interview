---
id: misc-022
difficulty: L1
category: ai-basics
subcategory: 推理优化
tags:
- IOC
images:
- svg_speculative.svg
feynman:
  essence: 小模型写草稿，大模型审核，并行验证大幅提升生成速度。
  analogy: 实习生先写好初稿，主编一次性批量审阅，比主编逐字写快得多。
  first_principle: 如何利用并行计算替代串行自回归生成，突破推理速度瓶颈？
  key_points:
  - Draft Model负责快速猜测
  - Target Model并行验证
  - 猜测准确率决定加速比
  - Medusa用多头替代小模型
follow_up:
- 草稿模型如何选择?
- Eagle和Medusa有什么区别?
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
