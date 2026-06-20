---
id: "zp-infra-011"
difficulty: "L4"
category: "ai-harness"
subcategory: "工程化"
tags:
  - "智谱"
  - "面经"
  - "分布式训练"
  - "ZeRO"
  - "3D Parallelism"
  - "系统设计"
feynman:
  essence: "Agent Serving 的核心挑战是'长上下文 + 多轮交互 + 前缀重复'。用分层 KV 存储（GPU/CPU/SSD）、Radix Tree 前缀复用、按 KV 负载路由，在保证延迟的同时最大化吞吐。"
  analogy: "Agent Serving 像高端酒店管理——客人（请求）有长住（长上下文）有短住，有些是团体客（前缀共享），行李（KV Cache）需要分层存放（房间/仓库/冷库），前台根据空房情况（KV 容量）分配房间。"
  key_points:
    - "KV 分层：GPU HBM → CPU RAM → SSD"
    - "RadixAttention 前缀复用节省 prefill"
    - "按 KV 负载路由，不是简单轮询"
    - "Speculative Decoding + 量化降成本"
first_principle:
  problem: "Agent Serving 三个独特挑战：长上下文（KV 大）、多轮交互（KV 需保持）、前缀重复（系统 prompt）。如何在保证低延迟的同时最大化吞吐？"
  axioms:
    - "KV Cache 是内存瓶颈 → 分层存储 + 动态卸载"
    - "前缀重复导致冗余计算 → Radix Tree 复用"
    - "请求长度差异大 → 需要智能批处理和路由"
  rebuild: "从 Agent 请求特征出发：① 为什么 KV 大（长上下文 + 多轮历史）？② 如何管理（分层存储 + 动态交换）？③ 哪些可复用（前缀/工具定义）？④ 怎么调度（按 KV 负载路由）？⑤ 成本怎么控（投机解码 + 量化 + 模型路由）？"
follow_up:
  - "KV Cache 从 CPU 换回 GPU 有多快？—— PCIe 4.0 约 64GB/s，1M token KV（~10GB）约 0.15s"
  - "怎么监控 Agent Serving 健康？—— P99 延迟、KV 命中率、GPU 利用率、队列深度"
  - "如何处理突发流量？—— 请求排队 + 优先级调度 + 自动扩缩 GPU 实例"
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
