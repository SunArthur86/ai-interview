---
id: "misc-032"
difficulty: "L2"
category: "ai-basics"
subcategory: "Prompt Engineering"
feynman:
  essence: "- *CoT核心:** 让模型先输出推理步骤,再输出最终答案,显著提升推理任务准确率. - *Zero-shot CoT:** - 在prompt末尾加上「让我"
  analogy: "ReAct 框架就像「边想边做」的工作方式——先思考（Thought）→ 行动（Action）→ 观察（Observation）→ 再思考，循环往复直到完成。"
  key_points:
    - "CoT核心: 让模型先输出推理步骤,再输出最终答案,显著提升推理任务准确率."
    - "Zero-shot CoT:"
    - "在prompt末尾加上「让我们一步一步思考」(Let's think step by step)"
first_principle:
  problem: "它们本质上为什么不同？各自的设计目标和适用场景是什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "Self-Consistency如何提升CoT?"
  - "CoT在什么模型规模下才有效?"
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
