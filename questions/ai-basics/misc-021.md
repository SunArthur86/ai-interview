---
id: misc-021
difficulty: L2
category: ai-basics
subcategory: 推理优化
images:
- svg_beam_search.svg
feynman:
  essence: 调节随机性与确定性的平衡，控制生成内容的多样性与质量。
  analogy: 调温水龙头，温度低就是固定的冷水，温度高就是随机混搭的热水。
  first_principle: 如何在模型生成的确定性与创造性之间找到最佳平衡点？
  key_points:
  - Temperature控制输出随机平滑度
  - Top-k限制候选词数量
  - Top-p限制累积概率质量
  - 通常组合使用Temp+Top-p
follow_up:
- 为什么Temperature=0不等于确定性输出?
- repetition_penalty如何影响生成质量?
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
