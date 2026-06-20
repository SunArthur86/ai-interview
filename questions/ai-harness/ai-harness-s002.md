---
id: "ai-harness-s002"
difficulty: "L3"
category: "ai-harness"
subcategory: "推理优化"
images:
  - "svg_kvcache.svg"
feynman:
  essence: "LLM自回归推理分两个阶段：  Prefill阶段（预填充）： - 处理输入prompt的所有token - 一次性并行计算所有token的KV Cache - 计算密集型（compute-bound）：大量矩阵乘法 - GPU利用率高  Decode阶段（解码）： - 逐个生成输出token - 每步用之前所有token的KV。"
  analogy: "Harness Engineering 就像给 AI 搭建完整的施工脚手架——不只是调 LLM API，而是构建提示词管理、工具编排、错误处理、监控的完整工程框架。"
  key_points:
    - "处理输入prompt的所有token"
    - "一次性并行计算所有token的KV Cache"
    - "计算密集型（compute-bound）：大量矩阵乘法"
first_principle:
  problem: "它们本质上为什么不同？各自的设计目标和适用场景是什么？"
  axioms:
    - "Harness Engineering 的核心是工程化——把 LLM 的潜力通过系统设计转化为可靠的生产力"
    - "评测驱动开发——没有 Golden Set 和持续评测，AI 系统就是黑盒"
    - "LLM 应用的可靠性 = 提示工程 + 错误处理 + 降级策略 + 可观测性"
  rebuild: "从工程化出发：① 为什么 LLM 应用需要 Harness？② 可观测性的核心指标？③ 如何做评测和回归？④ 理想的 AI 工程平台是什么样？"
---

# LLM推理的Prefill和Decode阶段有什么区别？

LLM自回归推理分两个阶段：

Prefill阶段（预填充）：
- 处理输入prompt的所有token
- 一次性并行计算所有token的KV Cache
- 计算密集型（compute-bound）：大量矩阵乘法
- GPU利用率高

Decode阶段（解码）：
- 逐个生成输出token
- 每步用之前所有token的KV Cache（从缓存读取）
- 内存密集型（memory-bound）：瓶颈在KV Cache读取带宽
- GPU利用率低（大模型通常<10%）

优化策略：
- Prefill优化：FlashAttention、Chunked Prefill（将长prompt分块处理）
- Decode优化：KV Cache量化、GQA/MQA、投机采样
- 调度优化：将Prefill和Decode请求混合批处理（vLLM的continuous batching）

TTFT（Time To First Token）= Prefill时间
TPOT（Time Per Output Token）= Decode时间
