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

**Prefill阶段（预填充）：**
- 处理输入prompt的所有token
- 一次性并行计算所有token的KV Cache
- 计算密集型（compute-bound）：大量矩阵乘法
- GPU利用率高

**Decode阶段（解码）：**
- 逐个生成输出token
- 每步用之前所有token的KV Cache（从缓存读取）
- 内存密集型（memory-bound）：瓶颈在KV Cache读取带宽
- GPU利用率低（大模型通常<10%）

**优化策略：**
- Prefill优化：FlashAttention、Chunked Prefill（将长prompt分块处理）
- Decode优化：KV Cache量化、GQA/MQA、投机采样
- 调度优化：将Prefill和Decode请求混合批处理（vLLM的continuous batching）

**TTFT（Time To First Token）= Prefill时间**
**TPOT（Time Per Output Token）= Decode时间**

- **补充：计算与访存瓶颈的量化分析**
- **Prefill**: 算术强度高，FLOPs 随序列长度平方增长（$O(N^2)$），GPU 计算单元满载。
- **Decode**: 仅处理单个 Token，计算量小但需加载巨大的 KV Cache（$O(N)$），主要受限于 HBM 带宽。
- **混合调度**: 为了避免 Decode 阶段长请求阻塞短请求的 TTFT，vLLM 等框架会采用迭代级调度，优先保证新请求的 Prefill 资源。

## 常见考点
1. **为什么长文本生成时 Decode 越来越慢？**
   - KV Cache 随生成长度线性增加，每次迭代读取显存量增加，且 Attention 计算量增加（尽管有 Mask，但访存开销增大）。
2. **FlashAttention 主要优化了哪个阶段？**
   - 主要优化 Prefill 阶段，通过 Tiling 技术减少 HBM 访问，提升 Attention 计算速度。
3. **如何降低首字延迟（TTFT）？**
   - 使用 Streaming Prefill（边生成边处理输入）、增加 GPU 并行度或使用更快的 Prefill 专用算子。
