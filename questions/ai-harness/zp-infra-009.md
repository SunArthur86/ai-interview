---
id: "zp-infra-009"
difficulty: "L3"
category: "ai-harness"
subcategory: "推理优化"
tags:
  - "智谱"
  - "面经"
  - "vLLM"
  - "SGLang"
  - "推理引擎"
feynman:
  essence: "vLLM 是'内存管理大师'（PagedAttention），SGLang 是'记忆+结构双修'（RadixAttention+结构化生成）。前者通用场景最强，后者多轮对话和 Agent 场景更强。"
  analogy: "vLLM 像高效出租车调度（每辆车充分利用），SGLang 像有记忆的出租车+能按路线约束行驶（记住常客路线+只走指定道路）。"
  key_points:
    - "vLLM：PagedAttention + 连续批处理"
    - "SGLang：RadixAttention + 结构化生成"
    - "多轮/Agent → SGLang 更优"
    - "通用 API → vLLM 更成熟"
first_principle:
  problem: "推理引擎的瓶颈在 KV Cache 管理和请求调度。不同场景（通用/多轮/结构化）的瓶颈不同，如何针对性优化？"
  axioms:
    - "KV Cache 是内存瓶颈 → 分页管理（vLLM）或前缀复用（SGLang）"
    - "多轮对话/Agent 有大量前缀重复 → 自动复用收益大"
    - "结构化输出需要约束 token 采样 → 原生支持比后处理高效"
  rebuild: "从推理场景出发：① 通用场景的瓶颈（碎片/调度）→ vLLM 解决 ② 多轮/Agent 的特殊需求（前缀复用）→ SGLang RadixAttention ③ 结构化输出的需求（JSON约束）→ SGLang 原生支持 ④ 各自适用场景的 trade-off？"
follow_up:
  - "RadixAttention 和 PagedAttention 能一起用吗？—— 可以，SGLang 底层也用分页管理"
  - "结构化生成怎么做？ — — 在 logits 上加 mask，只允许符合约束的 token"
  - "TGI 和 TensorRT-LLM 呢？ — — TGI（HuggingFace）注重易用性，TensorRT-LLM（NVIDIA）注重极致性能"
---

# 【智谱Infra面经】vLLM 和 SGLang 有什么区别？各自的优势和适用场景？

**vLLM vs SGLang 对比：**

| 维度 | vLLM | SGLang |
|------|------|--------|
| **核心创新** | PagedAttention | RadixAttention + 结构化生成 |
| **KV 管理** | 分页块表 | Radix Tree 前缀复用 |
| **批处理** | Continuous Batching | Continuous Batching + 结构化约束 |
| **多轮对话** | 前缀复用有限 | Radix Tree 自动复用（优势大） |
| **结构化输出** | 需后处理 | 原生支持（JSON/Regex/选择） |
| **吞吐** | 高（通用场景） | 更高（多轮/前缀共享场景） |
| **生态** | 更成熟，社区大 | 新兴，增长快 |

**vLLM 核心优势：**
1. **PagedAttention** — 分页管理 KV Cache，消除碎片
2. **连续批处理** — 动态进出请求，最大化 GPU 利用率
3. **广泛模型支持** — HuggingFace 模型零适配
4. **成熟生态** — 最大开源推理社区

**SGLang 核心优势：**
1. **RadixAttention** — Radix Tree 自动识别并共享相同前缀
   - 多轮对话：system prompt 的 KV 自动复用
   - Agent 场景：工具描述的 KV 复用
   - Few-shot：示例前缀复用
2. **结构化生成** — 原生 JSON/Regex 约束解码
   - 直接约束 token 采样，无需后处理
   - 比 outlines/guidance 更高效
3. **前端 DSL** — Python DSL 编排复杂生成流程

**适用场景：**
- **vLLM**：通用推理、单轮对话、API 服务
- **SGLang**：多轮对话、Agent、结构化输出、Few-shot 大量前缀共享
