---
id: misc-032
difficulty: L2
category: ai-basics
subcategory: Prompt Engineering
feynman:
  essence: 通过引导模型展示中间思考过程，提升复杂逻辑推理的准确性。
  analogy: 像解数学题，写出解题过程比只写答案更不容易算错，也更容易检查。
  first_principle: 如何激活LLM的推理能力，使其能处理多步逻辑而非仅靠直觉猜测？
  key_points:
  - Zero-shot加一句“一步步思考”即可
  - Few-shot给范例效果更稳
  - 增加推理计算量，减少逻辑跳跃
follow_up:
- Self-Consistency如何提升CoT?
- CoT在什么模型规模下才有效?
---

# Chain-of-Thought (CoT) 提示的原理是什么?Zero-shot CoT vs Few-shot CoT有什么区别

- **CoT核心:** 让模型先输出推理步骤,再输出最终答案,显著提升推理任务准确率.

- **Zero-shot CoT:**
- 在prompt末尾加上「让我们一步一步思考」(Let's think step by step)
- 无需示例

- **Few-shot CoT:**
- 提供带推理过程的示例
- 示例格式:问题→推理步骤→答案
- 效果更好但消耗更多token

- **为什么有效:**
1. **分解问题** - 复杂问题拆为子步骤
2. **利用更多计算** - 更多的中间token = 更多的推理计算
3. **减少跳步错误** - 强制模型展示中间过程

- **CoT效果(GSM8K数学题):**
- 标准prompt: 17.7%
- Zero-shot CoT: 46.9%
- Few-shot CoT: 56.9%
