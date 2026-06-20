---
id: misc-023
difficulty: L2
category: ai-basics
subcategory: 推理优化
tags:
- IO
- IOC
feynman:
  essence: 量化显存、分片计算与稀疏化注意力，突破长上下文的计算与存储限制。
  analogy: 看书只记重点笔记，厚书变薄，遇到需要时再翻详细章节。
  first_principle: 如何打破Attention机制O(n²)计算复杂度和KV Cache显存爆炸的瓶颈？
  key_points:
  - KV Cache量化与Offloading省显存
  - Ring Attention跨机分布式计算
  - 滑动窗口与稀疏注意力降复杂度
  - StreamingLLM支持无限流式输入
follow_up:
- Attention Sink是什么?为什么 StreamingLLM需要它?
- YaRN长度外推的原理?
---

# 处理100K+长上下文推理时,KV Cache和Attention如何优化

- **挑战:** 128K上下文,KV Cache可达80GB+(70B模型),Attention O(n²)计算

- **KV Cache优化:**
1. **量化KV Cache** - INT8/FP8,减少50%显存
2. **PagedAttention** - 分页管理消除碎片
3. **KV Cache Offloading** - 不活跃部分放到CPU/SSD

- **Attention优化:**
1. **Ring Attention** - 多GPU环形分片,支持百万token
2. **稀疏Attention** - 只关注局部窗口+全局token
3. **滑动窗口注意力** - Mistral用SWA,固定窗口大小
4. **StreamingLLM** - 保留attention sink + 滑动窗口,支持无限长度推理
