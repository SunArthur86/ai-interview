---
id: zp-infra-003
difficulty: L5
category: ai-harness
subcategory: 推理优化
tags:
- 智谱
- 面经
- 量化
- NVFP4
- FP8
- 缩放
feynman:
  essence: 利用浮点格式指数特性在4比特内表达更大动态范围
  analogy: 像用科学计数法简写数字，虽位数少但能记很大或很小的数
  first_principle: 如何在4bit极低空间下同时容纳大数值和小数值？
  key_points:
  - 格式为1符号+2指数+1尾数（E2M1）
  - 采用Per-block缩放，32个数值共享一个FP8缩放因子
  - 动态范围远超INT4，适合大模型权重分布
  - Blackwell架构专用硬件支持
follow_up:
- FP4 和 INT4 精度差多少？—— FP4 通常精度损失 <1-2%，INT4 可能 3-5%
- per-block 32 怎么选的？—— 平衡压缩率和精度，32 是 Blackwell 硬件原生支持的 block size
- NVFP4 推理比 INT8 快多少？—— 理论 2x（数据搬运减半），实际依赖 kernel 实现
---

# 【智谱Infra面经】NVFP4 的原理是什么？怎么做缩放的？在哪个维度缩放？保存的格式是什么？

**NVFP4 (NVIDIA FP4) 是 NVIDIA Blackwell 架构（B200/GB200）引入的 4-bit 浮点数量化格式。**

**核心原理：**
- 每个 FP4 值 = 1 bit 符号 + 2 bit 指数 + 1 bit 尾数 = 4 bit
- 动态范围：约 ±448（E2M1 编码）
- 比 INT4 的动态范围更大，精度更好

**缩放机制（关键）：**
- **per-block scaling**：每 32 个 FP4 值共享一个 FP8 缩放因子
- 缩放在 **最后一个维度**（通常对应 channel/feature 维）
- `实际值 = FP4值 × scale(FP8)`

**保存格式：**
```
权重矩阵 W [M, N]:
  存储: W_fp4 [M, N] (4-bit per element)
  缩放: scales [M, N/32] (FP8 per 32-element block)
  
反量化: W[m, n] = W_fp4[m, n] × scales[m, n//32]
```

**与 INT4 对比：**
| 特性 | INT4 | NVFP4 |
|------|------|-------|
| 编码 | 均匀量化 | 浮点量化（指数+尾数）|
| 动态范围 | [-8, 7] | ±448 |
| 缩放 | per-group (128) | per-block (32) + FP8 scale |
| 精度 | 较低 | 更高（浮点分布更均匀）|
| 硬件 | 通用 GPU | Blackwell 专用 |

**应用场景：**
- 推理加速：KV Cache 量化、权重压缩
- 训练加速：梯度/优化器状态压缩
- 与 FP8 Tensor Core 配合实现端到端 FP4 推理
