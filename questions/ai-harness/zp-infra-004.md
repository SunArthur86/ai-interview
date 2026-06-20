---
id: "zp-infra-004"
difficulty: "L4"
category: "ai-harness"
subcategory: "推理优化"
tags:
  - "智谱"
  - "面经"
  - "KV Cache"
  - "PagedAttention"
  - "vLLM"
feynman:
  essence: "KV Cache 像图书馆的书架——传统方式每个读者预订一整排书架（预分配），大部分空着。PagedAttention 把书架拆成小格子（block），按需分配，谁用谁占，利用率从 40% 飙到 96%。"
  analogy: "PagedAttention 就像共享办公位——不需要给每个人固定工位（浪费），而是谁来了谁坐（动态分配），走了解放位置。多人讨论同一主题时还可以共享会议资料（Radix Tree 前缀复用）。"
  key_points:
    - "PagedAttention：分页管理 KV，消除碎片"
    - "连续批处理：动态进出请求"
    - "Radix Tree：共享前缀 KV"
    - "KV 量化 + GQA 进一步减半"
first_principle:
  problem: "自回归推理每生成一个 token 都要读取所有之前的 K/V。KV Cache 大小 = 2 × n_layers × n_heads × d_head × seq_len，长序列下爆炸。如何最小化内存浪费？"
  axioms:
    - "KV Cache 是推理内存的主要占用者——不是权重"
    - "预分配导致 50%+ 的内存浪费——请求长度差异大"
    - "前缀重复在 Agent/对话场景普遍——可共享"
  rebuild: "从内存利用率出发：① 浪费在哪（碎片/预分配/重复）？② 如何消除碎片（分页管理）？③ 如何动态调度（连续批处理）？④ 如何复用（前缀树）？⑤ 如何压缩（量化/减头）？"
follow_up:
  - "PagedAttention 的 block size 怎么选？—— 通常 16，太小则块表开销大，太大则碎片多"
  - "Continuous Batching 和 Static Batching 区别？—— Static 等最慢请求完成，Continuous 动态进出"
  - "KV Cache 量化会影响精度吗？—— INT8 几乎不影响，INT4 可能损失 1-3%"
---

# 【智谱Infra面经】KV Cache 导致推理成本远高于预期，如何诊断和修复？

**KV Cache 是大模型推理的核心瓶颈。**

**问题诊断：**

1. **内存碎片**
   - 传统预分配：每个请求预留 max_seq_len 的 KV 空间
   - 实际只用一部分 → 大量浪费
   - 诊断：监控 GPU 内存利用率 vs 实际 KV 使用率

2. **预分配浪费**
   - 短请求（如 50 token）却分配了 2048 token 的空间
   - 诊断：比较实际生成长度 vs 预分配长度

3. **无法共享前缀**
   - 多轮对话中相同 system prompt 的 KV Cache 重复计算
   - 诊断：分析请求的前缀重复率

**修复方案（组合使用）：**

1. **PagedAttention（vLLM 核心创新）**
   - 类似操作系统虚拟内存分页
   - KV Cache 分成固定大小 block（如 16 token/block）
   - 块表（Block Table）映射逻辑序列 → 物理块
   - 非连续存储、动态分配/释放
   - **内存利用率从 ~40% → ~96%**

2. **连续批处理（Continuous Batching）**
   - 动态加入/移除请求
   - 不需要等待同一 batch 的所有请求完成
   - **吞吐提升 2-8x**

3. **Radix Tree 前缀复用**
   - 识别相同前缀的请求
   - 共享前缀部分的 KV Cache
   - 多轮对话/Agent 场景效果显著

4. **KV Cache 量化**
   - INT8/FP8 量化 KV
   - 内存减半，精度损失 <1%

5. **GQA/MQA 减少 KV 头数**
   - GLM-4 用 GQA（4-8 组）→ KV Cache 减少 4-8x
