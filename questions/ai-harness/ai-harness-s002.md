---
id: ai-harness-s002
difficulty: L3
category: ai-harness
subcategory: 推理优化
images:
- svg_kvcache.svg
feynman:
  essence: Prefill并行读题，Decode逐字答题，两者计算和访存瓶颈不同。
  analogy: 读题时大脑飞速运转，写字时手速受限而大脑等待。
  first_principle: 如何区分并优化LLM推理中"理解输入"和"生成输出"这两个不同性质的阶段？
  key_points:
  - Prefill阶段计算密集，并行处理Prompt生成KV Cache
  - Decode阶段访存密集，逐Token生成受限于显存带宽
  - Prefill决定首字延迟(TTFT)，Decode决定生成速度(TPOT)
  - 优化需针对不同阶段的瓶颈分别采取措施
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
