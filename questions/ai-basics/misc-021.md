---
id: "misc-021"
difficulty: "L2"
category: "ai-basics"
subcategory: "推理优化"
images:
  - "svg_beam_search.svg"
feynman:
  essence: "Temperature + Top-p 最常用.代码/数学:T=0.1,p=0.95;创意写作:T=0.7,p=0.9。"
  analogy: "采样策略就像调音响的三个旋钮——Temperature 调随机性（高=即兴发挥、低=稳准狠），Top-k 限制候选数量（只看前 k 名），Top-p 按累积概率圈范围（动态截断尾部）。"
  key_points:
    - "组合建议: Temperature + Top-p 最常用.代码/数学:T=0.1,p=0.95;创意写作:T=0.7,p=0.9"
    - "原理: logits除以T后做softmax,再截断Top-k或Top-p,最后从剩余token按概率采样"
first_principle:
  problem: "为什么需要 Temperature、Top-p、Top-k采样策略各自的作用?如何组合使用？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "为什么Temperature=0不等于确定性输出?"
  - "repetition_penalty如何影响生成质量?"
---

# Temperature、Top-p、Top-k采样策略各自的作用?如何组合使用

- **采样策略:**

| 策略 | 作用 | 推荐值 |
|------|------|--------|
| Temperature | 控制随机性,T越低越确定 | 代码0.1/创意0.7 |
| Top-k | 只从概率最高的k个token中采样 | k=40 |
| Top-p (Nucleus) | 从累积概率超过p的最小token集中采样 | p=0.9 |

- **组合建议:** Temperature + Top-p 最常用.代码/数学:T=0.1,p=0.95;创意写作:T=0.7,p=0.9

- **原理:** logits除以T后做softmax,再截断Top-k或Top-p,最后从剩余token按概率采样
