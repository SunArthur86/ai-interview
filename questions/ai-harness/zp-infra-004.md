---
id: zp-infra-004
difficulty: L4
category: ai-harness
subcategory: 推理优化
tags:
- 智谱
- 面经
- KV Cache
- PagedAttention
- vLLM
feynman:
  essence: 通过分页管理、动态批处理和前缀复用优化显存
  analogy: 像餐厅管理桌子，有人走立刻收台（Paged），拼桌坐人（CB），同点一份菜（Prefix）
  first_principle: 如何在高并发下最小化显存占用并最大化吞吐？
  key_points:
  - PagedAttention解决内存碎片和浪费问题
  - Continuous Batching提升GPU利用率
  - 前缀复用避免重复计算相同Prompt
  - 量化（INT8/FP8）和GQA直接压缩KV体积
follow_up:
- PagedAttention 的 block size 怎么选？—— 通常 16，太小则块表开销大，太大则碎片多
- Continuous Batching 和 Static Batching 区别？—— Static 等最慢请求完成，Continuous 动态进出
- KV Cache 量化会影响精度吗？—— INT8 几乎不影响，INT4 可能损失 1-3%
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

2. **连续批处理**
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
