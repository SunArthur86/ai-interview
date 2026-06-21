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
- 计算密集型：大量矩阵乘法
- GPU利用率高

**Decode阶段（解码）：**
- 逐个生成输出token
- 每步用之前所有token的KV Cache（从缓存读取）
- 内存密集型：瓶颈在KV Cache读取带宽
- GPU利用率低（大模型通常<10%）

- **阶段对比**

| 维度 | Prefill 阶段 | Decode 阶段 |
|------|-------------|-------------|
| 输入处理 | 一次处理所有 Prompt Token | 逐个生成 Output Token |
| 计算模式 | 并行计算 | 自回归串行计算 |
| 瓶颈资源 | GPU 算力 (Compute Bound) | 显存带宽 (Memory Bound) |
| 延迟特征 | 决定 TTFT (首字延迟) | 决定 TPOT (生成速度) |
| 优化手段 | FlashAttention, 分块预填充 | KV Cache 量化, Speculative Decoding |

- **实战案例**：在长文档总结任务中，Prefill 占用了总时间的 80%（由于 Prompt 极长）。通过采用分块 Prefill 策略，用户能在 1 秒内看到第一个生成的字，极大改善了“即时反馈”体验。踩坑：若 Decode 阶段显存带宽不足，即使显卡算力很强，生成速度也会被锁死在 20 tokens/s 以下。

- **代码示例**：
```python
# 伪代码：模拟 Prefill 和 Decode 的资源消耗差异
import torch

def profile_phase(stage, input_ids, past_kv=None):
    if stage == "prefill":
        # Prefill: 矩阵大，计算量 O(N^2)
        logits, kv_cache = model.forward(input_ids)
        print(f"Prefill: High FLOPs, GPU Compute Load: {torch.cuda.utilization()}%")
        return logits, kv_cache
    else:
        # Decode: 矩阵小，需加载巨大 KV Cache，带宽瓶颈 O(N)
        logits, kv_cache = model.forward(input_ids[-1:], past_kv)
        print(f"Decode: Low FLOPs, HBM Bandwidth Load: High")
        return logits, kv_cache
```

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
