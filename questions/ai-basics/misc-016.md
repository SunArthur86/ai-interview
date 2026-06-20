---
id: "misc-016"
difficulty: "L2"
category: "ai-basics"
subcategory: "训练与微调"
tags:
  - "IO"
feynman:
  essence: "**Flash Attention核心:减少HBM(显存)读写**"
  analogy: "注意力机制就像在聚会上听人说话——自动聚焦到感兴趣的声音，给不同人不同关注度。"
  key_points:
    - "Flash Attention核心:减少HBM(显存)读写"
    - "问题: 标准Attention中QKᵀ产生n*n矩阵,频繁读写HBM(慢)"
    - "解决方案:Tiling(分块)"
first_principle:
  problem: "剥离所有术语：Flash Attention的原理?为什么能同时加速和省显存 底层在做什么？为什么这样做是最优的？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "Flash Attention如何处理在线Softmax?"
  - "Flash Attention v3有什么改进?"
---

# Flash Attention的原理是什么?为什么能同时加速和省显存

- **Flash Attention核心:减少HBM(显存)读写**

- **问题:** 标准Attention中QKᵀ产生n*n矩阵,频繁读写HBM(慢)

- **解决方案:Tiling(分块)**
1. 将Q/K/V分成小块加载到SRAM(片上高速缓存)
2. 在SRAM中计算部分Attention
3. 使用在线Softmax技巧
4. 只将最终结果写回HBM

- **效果:**
- **速度:** 快2-4倍(减少HBM IO)
- **显存:** O(n) 而非 O(n²)
- **精确:** 数学上完全等价,非近似

- **Flash Attention v2改进:** 更好的GPU利用率,支持长序列(128K+)
