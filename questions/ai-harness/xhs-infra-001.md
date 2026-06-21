---
id: xhs-infra-001
difficulty: L4
category: ai-harness
subcategory: 推理与部署
tags:
- vLLM
- PagedAttention
- KV Cache
- 推理优化
- 小红书
feynman:
  essence: 借鉴操作系统虚拟内存分页管理KV Cache，解决显存碎片问题。
  analogy: 像电脑管理内存一样，把KV Cache切成固定页，哪里有空位放哪里。
  first_principle: 如何解决变长序列KV Cache存储导致的显存碎片和浪费问题？
  key_points:
  - 将KV Cache切块（Block）非连续存储，消除显存碎片
  - 通过Block Table管理逻辑到物理的映射
  - 结合Continuous Batching实现动态批处理
  - 支持前缀复用（Radix Tree）共享计算结果
follow_up:
- PagedAttention的block大小如何选择？
- 连续批处理和静态批处理有什么本质区别？
- Radix Tree如何实现多轮对话前缀复用？
---

# 为什么vLLM能加快大模型推理速度？PagedAttention的核心原理是什么？

vLLM通过PagedAttention机制大幅提升推理效率。

## PagedAttention核心机制
1. **块表映射**：借鉴OS虚拟内存分页，将KV Cache分成固定大小block（如16 token/block），用block table映射逻辑序列→物理block
2. **消除碎片**：按需分配block，非连续存储，内存利用率提升30%+
3. **连续批处理（Continuous Batching）**：动态加入/退出请求，GPU利用率接近100%

## 其他关键优化
- Radix Tree前缀复用（多轮对话共享KV）
- 高效attention kernel融合
- 动态batch填充

## 性能提升
- 吞吐量提升2-4x（vs HuggingFace Transformers）
- 内存浪费从60%+降至<4%
- 支持长上下文高并发Serving

### 实战案例
- **OOM 问题解决**：在某次支持 32k 上下文长度的模型部署中，使用 HuggingFace Transformers 的 `transformers` 库在 Batch Size=4 时就显存溢出（OOM）。切换到 vLLM 后，由于 PagedAttention 的物理块非连续分配特性，同样的显卡能支持 Batch Size=30 且长文本互不干扰。
- **Prefill 阶段卡顿**：在高并发下，vLLM 的 Block Manager 可能成为瓶颈。遇到 GPU 利用率低但延迟高的情况，通常是因为 `gpu_memory_utilization` 设置过高导致留给 KV Cache 的空间碎片化，调整至 0.9 并预留显存给系统后，P99 延迟下降了 15%。

### 代码示例 (Python - vLLM 离线推理)
```python
from vllm import LLM, SamplingParams

# 初始化 LLM 引擎，启用 block 16
llm = LLM(model="meta-llama/Llama-2-7b-hf", block_size=16)

# 配置采样参数
sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=100)

# 批量推理 prompts
prompts = ["你好，请介绍一下vLLM。", "什么是PagedAttention？"]
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    print(f"Output: {output.outputs[0].text}")
```

### 传统 vs vLLM 内存管理对比
| 特性 | 传统 KV Cache (如 HF Transformers) | vLLM PagedAttention |
| :--- | :--- | :--- |
| **内存分配** | 预分配连续整块内存 | 动态分配固定大小 Block |
| **内存碎片** | 严重（Sequence 长度不一导致内部/外部碎片） | 极低（非连续存储，类似虚拟内存） |
| **显存利用率** | 低（通常浪费 20%-60%） | 高（接近物理上限） |
| **长文本支持** | 差（需按最大长度预留） | 强（动态扩展 Block） |
| **缓存共享** | 难（Prefix Caching 实现复杂） | 易（通过 RadixTree 引用计数共享） |
