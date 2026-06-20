---
id: misc-003
difficulty: L2
category: ai-basics
subcategory: 大模型原理
feynman:
  essence: 将模型拆分为多个专家，推理时只激活部分专家，以大参数量换取低计算成本。
  analogy: 医院分科室看病，只挂相关科室的号，不用所有医生都看一遍。
  first_principle: 如何在不增加推理计算量的前提下扩大模型容量？
  key_points:
  - 通过Router门控网络动态选择激活的专家
  - 增加参数量同时控制激活计算量
  - DeepSeek引入共享专家隔离通用与专业知识
follow_up:
- MoE的负载均衡如何实现?
- 为什么MoE推理时显存占用高?
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
