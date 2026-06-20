---
id: misc-026
difficulty: L2
category: ai-basics
subcategory: RAG与向量检索
tags:
- IOC
feynman:
  essence: 将长文档切碎，以便向量检索能精准定位，同时保留上下文语义。
  analogy: 把百科全书撕成小卡片，每张卡片写上索引，方便快速抽取，并附上所属章节以便理解。
  first_principle: 如何将长文本切分，使得检索时最精准，生成时上下文最完整？
  key_points:
  - 固定窗口最简单，语义分块效果最好
  - 父子索引法兼顾检索精度与生成完整性
  - 重叠窗口防止语义切断
follow_up:
- 语义分块如何实现?
- Markdown文档如何结构化分块?
---

# RAG中的文档分块(Chunking)有哪些策略?如何选择最优策略

- **分块策略:**

| 策略 | 方法 | 优点 | 适用 |
|------|------|------|------|
| 固定长度 | 按token数切分 | 简单 | 通用 |
| 递归分割 | 按段落→句子递归 | 保留语义 | 文档 |
| 语义分块 | embedding相似度断句 | **最佳语义** | 高质量RAG |
| 结构化分块 | 按Markdown标题/代码块 | **保留结构** | 技术文档 |
| 父子分块 | 小块检索+大块生成 | **最优方案** | 生产系统 |

- **关键参数:**
- chunk_size: 256-1024 tokens(常用512)
- overlap: chunk_size的10-20%

- **最佳实践 - Parent-Child Chunking:**
1. 文档切成大块(parent, 1024 tokens)
2. 大块再切成小块(child, 256 tokens)
3. **检索用child**(精确匹配)
4. **生成用parent**(完整上下文)
