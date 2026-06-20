---
id: ai-harness-s005
difficulty: L3
category: ai-harness
subcategory: 推理优化
images:
- svg_kvcache.svg
feynman:
  essence: 通过分块、量化、共享和裁剪手段压缩KV Cache显存占用。
  analogy: 做笔记：只记重点(GQA)、用缩写(量化)、撕掉旧页、共用开头。
  first_principle: 如何在不显著影响模型效果的前提下，最大程度减少推理过程中的显存占用？
  key_points:
  - PagedAttention解决显存碎片和浪费问题
  - GQA/MQA通过减少KV头数大幅降低显存占用
  - 量化将FP16降至INT8/4，显著节省内存
  - 滑动窗口和Offloading进一步处理长序列低频数据
---

# LLM中的KV Cache如何优化？

KV Cache是LLM推理的主要显存开销（可达总显存的80%+）：

1. **PagedAttention**：
- 分块管理KV Cache
- 消除内部碎片
- 按需分配

2. **GQA/MQA**：
- 减少KV的头数
- MQA极端减少（1个KV头）
- GQA折中（如Llama3-8B用8个KV头vs32个Q头）

3. **KV Cache量化**：
- FP16 → INT8：减少50%内存
- KV Cache INT4量化：减少75%

4. **Sliding Window Attention**：
- 只保留最近W个token的KV Cache
- 超出窗口的丢弃（如Mistral用4096窗口）

5. **KV Cache Offloading**：
- 将不活跃的KV Cache移到CPU内存
- 需要时再加载回GPU

6. **Prefix Sharing**：
- 多请求共享相同system prompt的KV Cache

- **补充：量化与精度权衡**
- **静态量化**: 校准集确定量化参数，部署简单。
- **动态量化**: 运行时计算量化参数，精度略高但计算开销增加。
- **INT4 KV 陷阱**: 极低比特可能导致注意力计算出现显著的精度损失，通常需要配合 SmoothQuant 或类似的激活值平滑技术。

- **KV Cache 数据流示意图**

```text
输入 Token (T_i)
   │
   ▼
┌──────────────┐
│  QKV Projection │
└───┬──────┬────┘
    │      │
    │      ▼
    │  [Store K_i, V_i] ────> KV Cache (Memory)
    │      ▲
    │      │ (Load History K_0...K_{i-1})
    │      │
    ▼      │
┌──────────────┐
│ Attention Calc │ (Score = Q * K^T)
└──────────────┘
```

## 常见考点
1. **GQA 相比 MHA 能节省多少显存？**
   - 假设 Attention 头数为 H，GQA 的 KV 头数为 G，显存节省比例约为 $(1 - G/H)$，同时显著提升 Decode 阶段带宽利用率。
2. **KV Cache Offloading 为什么会导致性能骤降？**
   - PCIe 带宽远小于 GPU 显存带宽，每次换入换出 KV Cache 的延迟会极大拖慢 TPOT。
3. **FlashAttention 对 KV Cache 有影响吗？**
   - FlashAttention 优化的是计算过程（减少 HBM 访问），不改变 KV Cache 的存储机制，但通常与其配套使用。
