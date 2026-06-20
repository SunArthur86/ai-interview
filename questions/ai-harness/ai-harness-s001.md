---
id: "ai-harness-s001"
difficulty: "L3"
category: "ai-harness"
subcategory: "推理优化"
images:
  - "svg_kvcache.svg"
feynman:
  essence: "vLLM是当前最流行的开源LLM推理框架，核心优化： 1. PagedAttention： - 将KV Cache分块管理（类似OS虚拟内存分页） - 消除显存"
  analogy: "Harness Engineering 就像给 AI 搭建完整的施工脚手架——不只是调 LLM API，而是构建提示词管理、工具编排、错误处理、监控的完整工程框架。"
  key_points:
    - "PagedAttention："
    - "将KV Cache分块管理（类似OS虚拟内存分页）"
    - "消除显存碎片，显存利用率从60%提升到96%+"
first_principle:
  problem: "从第一性原理看：vLLM的核心优化技术有哪些 的根本优势/劣势来源于什么？"
  axioms:
    - "Harness Engineering 的核心是工程化——把 LLM 的潜力通过系统设计转化为可靠的生产力"
    - "评测驱动开发——没有 Golden Set 和持续评测，AI 系统就是黑盒"
    - "LLM 应用的可靠性 = 提示工程 + 错误处理 + 降级策略 + 可观测性"
  rebuild: "从工程化出发：① 为什么 LLM 应用需要 Harness？② 可观测性的核心指标？③ 如何做评测和回归？④ 理想的 AI 工程平台是什么样？"
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
