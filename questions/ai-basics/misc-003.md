---
id: "misc-003"
difficulty: "L2"
category: "ai-basics"
subcategory: "大模型原理"
feynman:
  essence: "MoE将FFN层替换为多个专家网络,通过Router动态选择激活部分专家. - *核心机制:** 1. Router(gate)计算输入与每个专家的匹配度 2."
  analogy: "MoE（混合专家）就像医院分诊台——根据病症分给不同专家（专家网络），每次只激活相关专家。"
  key_points:
    - "Router(gate)计算输入与每个专家的匹配度"
    - "选Top-K个专家(通常K=2或K=8)"
    - "加权融合选中专家的输出"
first_principle:
  problem: "它们本质上为什么不同？各自的设计目标和适用场景是什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "MoE的负载均衡如何实现?"
  - "为什么MoE推理时显存占用高?"
---

# MoE(Mixture of Experts)架构是什么?DeepSeek-MoE和Mixtral有什么区别

MoE将FFN层替换为多个专家网络,通过Router动态选择激活部分专家.

- **核心机制:**
1. Router(gate)计算输入与每个专家的匹配度
2. 选Top-K个专家(通常K=2或K=8)
3. 加权融合选中专家的输出

- **Mixtral 8x7B:**
- 8个专家,每次激活2个
- 总参数47B,推理时只激活13B
- 均匀路由策略

- **DeepSeek-MoE:**
- **细粒度专家** - 更多更小的专家(如64选8)
- **共享专家** - 保留部分专家始终激活,处理通用知识
- 更好的专家专业化,减少冗余

- **优势:** 以更少的推理计算量达到更大模型的效果
- **挑战:** 显存占用大(所有专家都在显存),通信开销
