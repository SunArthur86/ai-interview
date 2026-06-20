---
id: ai-harness-s001
difficulty: L3
category: ai-harness
subcategory: 推理优化
images:
- svg_kvcache.svg
feynman:
  essence: PagedAttention管理显存碎片，Continuous Batching动态调度计算。
  analogy: 像把仓库格子化管理货物，且送货员走完一单立刻接下一单，不空跑。
  first_principle: 如何突破显存浪费和计算空闲两大瓶颈，实现LLM的高吞吐推理？
  key_points:
  - PagedAttention将KV Cache分块，极大提高显存利用率
  - Continuous Batching让变长请求在同批次高效流转
  - 支持张量并行等分布式推理技术
  - 引入前缀缓存和投机采样进一步加速
---

# vLLM的核心优化技术有哪些？

vLLM是当前最流行的开源LLM推理框架，核心优化：

1. PagedAttention：
- 将KV Cache分块管理（类似OS虚拟内存分页）
- 消除显存碎片，显存利用率从60%提升到96%+
- 支持Copy-on-Write，Parallel Sampling共享前缀

2. Continuous Batching（连续批处理）：
- 传统Static Batching：一个batch中所有请求要同时完成
- Continuous Batching：每个iteration动态调度，完成一个请求立即放入新请求
- GPU利用率大幅提升

3. Tensor Parallelism（张量并行）：
- 将模型权重切分到多GPU
- 支持NCCL通信

4. 其他优化：
- Prefix Caching：缓存相同前缀的KV（如system prompt）
- Speculative Decoding：投机采样加速
- Quantization：支持AWQ、GPTQ量化模型

性能：比HuggingFace Transformers快14-24倍，接近商用API吞吐量。

- **补充：PagedAttention 内部机制**
- **Block 表**: vLLM 为每个 Sequence 维护一个 Block 表，映射逻辑 Block 到物理 Block，支持非连续内存分配，解决内存碎片。
- **迭代级调度**: 调度器在每个解码步骤结束后，根据已完成和新加入的请求重组 Batch，无需等待 Batch 中所有请求结束。

## 常见考点
1. **vLLM 的 Block Size 如何选择？**
   - 通常设为 16，需权衡显存管理开销和内存粒度。太小导致 Block Table 过大，太大致内部浪费。
2. **Continuous Batching 和 Orca 有什么区别？**
   - Orca 是 Continuous Batching 的一种早期实现，vLLM 结合 PagedAttention 进一步提升了显存管理效率。
3. **vLLM 如何处理 Prefix Caching 的失效？**
   - 引用计数管理，当所有引用该 Prefix 的请求结束后，释放对应的物理 Block。
