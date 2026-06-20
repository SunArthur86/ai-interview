---
id: misc-024
difficulty: L2
category: ai-basics
subcategory: 推理优化
images:
- svg_beam_search.svg
feynman:
  essence: 平衡模型置信度与生成多样性，避免重复退化。
  analogy: 像写作文，既要写得通顺（听老师的话），又不能一直重复同一句（要有新词）。
  first_principle: 如何在保持语义连贯的同时，避免生成的文本陷入死循环和重复？
  key_points:
  - Greedy贪心最快但无随机性
  - Beam Search保留多条路径质量高
  - Contrastive Search惩罚重复，通用性强
follow_up:
- Beam Search为什么在开放对话中效果不好?
- do_sample=True和False的区别?
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
