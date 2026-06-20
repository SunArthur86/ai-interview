---
id: zp-infra-011
difficulty: L4
category: ai-harness
subcategory: 工程化
tags:
- 智谱
- 面经
- 分布式训练
- ZeRO
- 3D Parallelism
- 系统设计
feynman:
  essence: 通过KV分层管理和前缀复用最大化算力利用率。
  analogy: 像图书馆管理，热门书放手边（GPU），旧书放书架（CPU），封存书放仓库（SSD）。
  first_principle: 如何在高并发下最大化 GPU 显存利用率和计算效率？
  key_points:
  - KV Cache 分层（GPU/CPU/SSD）
  - 前缀复用减少重复计算
  - 连续批处理提升吞吐
  - 基于KV占用率的负载均衡
follow_up:
- KV Cache 从 CPU 换回 GPU 有多快？—— PCIe 4.0 约 64GB/s，1M token KV（~10GB）约 0.15s
- 怎么监控 Agent Serving 健康？—— P99 延迟、KV 命中率、GPU 利用率、队列深度
- 如何处理突发流量？—— 请求排队 + 优先级调度 + 自动扩缩 GPU 实例
---

# 【智谱Infra面经】设计一个支持 1M 上下文 + 多模态的高并发 Agent Serving 系统，如何处理调度、KV 管理和负载均衡？

**百万级 Agent Serving 系统设计：**

**整体架构：**
```
客户端请求
  │
  ├─ API Gateway（认证/限流/路由）
  │
  ├─ 请求调度层
  │    ├─ 请求分类（单轮/多轮/Agent）
  │    ├─ 前缀分析（Radix Tree 匹配）
  │    └─ 动态批组装
  │
  ├─ GPU 推理集群
  │    ├─ vLLM/SGLang 实例
  │    ├─ PagedAttention KV 管理
  │    └─ 连续批处理
  │
  ├─ KV Cache 存储层
  │    ├─ GPU HBM（热数据）
  │    ├─ CPU RAM（温数据）
  │    └─ SSD/对象存储（冷数据）
  │
  └─ 监控 & 自动扩缩
```

**关键设计点：**

1. **KV Cache 分层管理**
   - 热：当前活跃请求 → GPU HBM
   - 温：Agent 多轮对话历史 → CPU RAM（可快速换回 GPU）
   - 冷：长时间不活跃 → SSD（释放 GPU/CPU 内存）
   - **关键**：Agent 场景中 Tool Calling 间隙 KV 可以卸载到 CPU

2. **前缀复用（RadixAttention）**
   - Agent 系统中 system prompt + tool 定义是公共前缀
   - 多个请求共享前缀 → KV Cache 复用
   - 节省 50%+ 的 prefill 计算

3. **动态批处理**
   - 短请求和长请求不混批（避免 padding 浪费）
   - Agent 多步请求按步骤分组
   - 连续批处理：新请求随时加入、完成的随时退出

4. **负载均衡**
   - 按 KV Cache 使用率路由（不是简单 round-robin）
   - 长上下文请求路由到 KV 充足的 GPU
   - 模型并行：大模型用 TP/PP 切分到多卡

5. **成本优化**
   - Speculative Decoding 加速生成
   - FP8/INT8 量化减少内存
   - 模型路由：简单请求走小模型，复杂请求走大模型
