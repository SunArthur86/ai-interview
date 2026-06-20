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
