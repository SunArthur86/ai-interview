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

- **Greedy Search (贪婪搜索)**
  - **原理**：每一步选择概率最高的 token。
  - **优点**：计算速度快，确定性强。
  - **缺点**：容易陷入重复循环，缺乏多样性，可能漏掉全局最优序列（如“The weather is nice”可能比“The weather is good”整体概率更高，但第一步greedy选了good）。

- **Beam Search (集束搜索)**
  - **原理**：每一步保留 Top-$k$ 个候选序列（beam width），直到结束。
  - **优点**：比 Greedy 找到更优序列的概率大，结果更稳定。
  - **缺点**：计算量大（$k$倍显存和算力）；容易生成通用的、平庸的废话；在开放域生成中往往不如 Sampling 灵活。
  - **参数**：`num_beams` (通常2-10)，`length_penalty` (惩罚过短或过长的序列)。

- **Contrastive Search (对比搜索)**
  - **原理**：结合概率模型和退化惩罚。选择下一个 token $x_t$，最大化 $p(x_t|context) - \alpha \cdot \max sim(v(x_t), v(x_{<t}))$。即在保证高概率的同时，选择与已生成序列相似度最低的 token，避免重复。
  - **优点**：解决了大模型生成中的“重复退化”问题，人类评估质量通常高于 Beam Search 和 Nucleus Sampling。
  - **参数**：`top_k` (候选集大小)，`alpha` (退化惩罚系数，通常0.5-0.7)。

- **Nucleus Sampling (Top-p 采样)**
  - **原理**：从累积概率达到 $p$ (如0.9) 的最小集合中随机采样。
  - **优点**：生成的文本多样性高，适合创意写作。
  - **缺点**：不可控，可能产生幻觉或逻辑断裂。

```text
策略选择决策树:
┌───────────────────┐
│   生成任务类型?   │
└─────────┬─────────┘
          │
   ┌──────┴──────┐
   │             │
   ▼             ▼
┌─────────┐  ┌──────────┐
│  事实性  │  │ 创意/对话 │
│  问答/翻译 │  │  (开放域) │
└────┬────┘  └─────┬────┘
     │             │
     ▼             ▼
┌─────────┐  ┌──────────┐
│Greedy/  │  │ Nucleus  │
│Contrast │  │ Sampling │
└─────────┘  └──────────┘
```

- **## 常见考点**
1. **为何 Beam Search 在人类评估中常不如 Sampling？**（因为 Beam Search 倾向于保守、高概率但“无聊”的文本）
2. **Contrastive Search 中 $\alpha$ 参数的作用**？($\alpha$ 过大导致不连贯，过小导致重复)
3. **Temperature 参数的影响**？（Temperature > 1 平滑概率分布增加随机性，< 1 尖锐分布使其更确定，接近0即变为Greedy）
