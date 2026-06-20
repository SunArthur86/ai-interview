---
id: "misc-024"
difficulty: "L2"
category: "ai-basics"
subcategory: "推理优化"
images:
  - "svg_beam_search.svg"
feynman:
  essence: "score = p(x) - beta * max_sim(x, history)。"
  analogy: "解码策略就像选路——Greedy 是每步选最近的（快但可能错过全局最优），Beam Search 是同时探索 K 条路（更优但更慢），Contrastive 是避免和已生成内容重复。"
  key_points:
    - "Contrastive Search核心:"
    - "在选下一个token时,惩罚与已生成token太相似的候选"
    - "公式:score = p(x) - beta * max_sim(x, history)"
first_principle:
  problem: "它们本质上为什么不同？各自的设计目标和适用场景是什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "Beam Search为什么在开放对话中效果不好?"
  - "do_sample=True和False的区别?"
---

# 对比常见解码策略:Greedy/Beam Search/Contrastive Search各自的优缺点

- **解码策略对比:**

| 策略 | 质量 | 多样性 | 速度 | 适用 |
|------|------|--------|------|------|
| Greedy | 一般 | 无 | **最快** | 简单任务 |
| Beam Search | 高 | 低 | 慢 | 翻译/摘要 |
| Top-p采样 | 中 | 高 | 快 | 创意写作 |
| **Contrastive** | **高** | 中 | 中 | **通用最佳** |

- **Contrastive Search核心:**
- 在选下一个token时,惩罚与已生成token太相似的候选
- 公式:score = p(x) - beta * max_sim(x, history)
- 兼顾流畅性(模型概率)和多样性(去重复)

- **实际建议:**
- 代码/数学:Greedy或T=0.1
- 对话/创意:Top-p采样 T=0.7
- 严肃内容:Contrastive Search
