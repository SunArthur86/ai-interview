---
id: "zp-infra-012"
difficulty: "L3"
category: "ai-harness"
subcategory: "工程化"
tags:
  - "智谱"
  - "面经"
  - "AI Infra"
  - "求职准备"
  - "学习路线"
feynman:
  essence: "AI Infra 岗位的核心竞争力 = 系统级思维 + 工程实战 + 量化成果。不是'知道多少算法'，而是'能把模型跑多快、多省、多稳'。"
  analogy: "AI Infra 工程师是'修高速公路的人'——算法岗研究'造什么车'（模型），Infra 岗研究'怎么让车跑得更快更省油'（训练/推理优化）。路修得好不好，看吞吐（车流量）和延迟（车速）。"
  key_points:
    - "4 大模块：Transformer + 推理 + 训练 + CUDA"
    - "必读：FlashAttention / ZeRO / PagedAttention / 量化"
    - "项目深挖占 40% — — 必须有量化指标"
    - "6-8 周准备：基础→论文→源码→模拟"
first_principle:
  problem: "AI Infra 是一个高度实践导向的岗位。面试官想看的是：你能否把'纸上的原理'变成'跑得快的系统'。"
  axioms:
    - "Infra 岗重工程实战 > 论文复现"
    - "量化成果（MFU/吞吐/延迟）是通用语言"
    - "系统设计能力是高级岗分水岭"
  rebuild: "从面试官视角出发：① 他需要什么能力（工程/系统/性能优化）？② 怎么证明你有（量化项目 + 开源贡献）？③ 怎么高效准备（论文→源码→实验→总结）？④ 怎么展示（STAR 结构 + trade-off 讨论）？"
follow_up:
  - "没有 Infra 实习经验怎么办？ — — 自己复现 vLLM/DeepSpeed 实验，做 benchmark 对比"
  - "CUDA 编程零基础怎么入门？ — — NVIDIA 官方教程 + 简单 GEMM/softmax kernel 练习"
  - "Infra 和算法岗的区别？ — — Infra 重工程/系统/性能优化，算法重模型/训练/数据"
---

# 【智谱面经】大模型 Infra 岗位怎么准备？必看资料有哪些？面试考察重点是什么？

**大模型 AI Infra 岗位准备全攻略：**

**一、核心知识树（4 大模块）**

1. **Transformer 架构原理**
   - Self-Attention / Multi-Head / GQA / MLA
   - FlashAttention v1/v2/v3
   - 位置编码（RoPE / ALiBi / YaRN）
   - MoE 架构与路由

2. **推理优化**
   - KV Cache + PagedAttention + RadixAttention
   - 量化（SmoothQuant / AWQ / GPTQ / FP8 / NVFP4）
   - 投机解码（Speculative Decoding / Medusa / EAGLE）
   - 推理引擎（vLLM / SGLang / TensorRT-LLM）

3. **训练优化**
   - 分布式训练（DDP / FSDP / ZeRO / 3D Parallelism）
   - 混合精度（BF16 / FP8）
   - 性能诊断（MFU / Profiler / Nsight / NCCL）
   - 检查点与容错

4. **CUDA / Kernel**
   - GPU 执行模型（warp / occupancy / memory hierarchy）
   - Roofline 分析
   - 常见 Kernel 优化（GEMM / Attention / Softmax）
   - Tensor Core / WMMA

**二、必看资料（🔺 高优先级）**

**论文：**
- "Attention Is All You Need" (Transformer)
- "FlashAttention" v1/v2/v3
- "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models"
- "PagedAttention / vLLM"
- "SmoothQuant" / "AWQ" / "GPTQ"
- "Speculative Decoding" / "Medusa" / "EAGLE"
- DeepSeek-V2/V3 技术报告（MLA / MoE）

**开源项目（读源码）：**
- **vLLM** — PagedAttention + Continuous Batching
- **DeepSpeed** — ZeRO 实现
- **FlashAttention** — IO-aware Attention Kernel
- **Megatron-LM** — 3D Parallelism

**工具/教程：**
- NVIDIA CUDA C++ Programming Guide
- Nsight Compute / Systems 教程
- PyTorch Profiler 文档

**三、面试考察重点**

| 维度 | 占比 | 说明 |
|------|------|------|
| **项目深挖** | 40% | STAR 结构 + 量化成果（MFU 提升多少、推理加速多少倍）|
| **原理追问** | 30% | 量化粒度、KV Cache 原理、投机解码实现 |
| **系统设计** | 15% | 设计百万 QPS Serving / 万卡训练系统 |
| **手撕代码** | 10% | MoE 路由、KV Cache 管理、Attention 实现 |
| **行为/文化** | 5% | 为什么选 AI Infra、职业规划 |

**四、准备时间线（6-8 周）**

```
Week 1-2: 基础（Transformer + CUDA + 分布式原理）
Week 3-4: 论文精读（FlashAttention / ZeRO / PagedAttention）
Week 5-6: 源码实践（vLLM / DeepSpeed / FlashAttention）
Week 7-8: 项目总结 + 模拟面试
```

**五、简历建议**
- 准备 2-3 个 STAR 结构项目
- 必须有量化指标（"MFU 从 45% 提至 72%"、"推理吞吐提升 3x"）
- 突出工程实战（不是只读论文）
- 开源贡献加分（vLLM/DeepSpeed PR）
