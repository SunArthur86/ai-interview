---
id: misc-048
difficulty: L2
category: ai-basics
subcategory: RAG与向量检索
tags:
- IOC
images:
- svg_embedding_training.svg
feynman:
  essence: 将文本/图像映射为高维向量，通过向量距离衡量语义相似度。
  analogy: 给每句话贴上唯一的“坐标标签”，意思越近标签贴得越近。
  first_principle: 如何让机器量化计算两个不同内容在语义上的相似程度？
  key_points:
  - 中文首选BGE系列（M3通用，large-zh专项）。
  - 商业可用选OpenAI或Cohere，多语言能力更强。
  - 选型需综合考量语言支持、维度大小和部署成本。
follow_up:
- BGE-M3的「三多」是什么意思?
- Matryoshka Embedding如何实现维度可变?
---

# 如何选择Embedding模型?BGE、E5、Cohere各有什么特点?中文场景推荐什么

- **主流Embedding模型:**

| 模型 | 类型 | 维度 | 中文支持 | 特点 |
|------|------|------|---------|------|
| BGE-M3 | 开源 | 1024 | **优秀** | 多语言/多功能/多粒度 |
| BGE-large-zh | 开源 | 1024 | **优秀** | 中文专项优化 |
| E5-mistral | 开源 | 4096 | 好 | 强通用 |
| GTE | 开源 | 768/1024 | 好 | 阿里达摩院 |
| text-embedding-3 | API | 1536/3072 | 好 | OpenAI |
| Cohere embed v3 | API | 1024 | 好 | 多语言 |

- **选择建议:**

1. **中文优先:** BGE-large-zh-v1.5 或 BGE-M3
2. **多语言:** BGE-M3 或 Cohere
3. **英文/通用:** text-embedding-3-large 或 E5
4. **预算充足:** OpenAI/Cohere API
5. **本地部署:** BGE系列(通过sentence-transformers加载)

- **评估指标:** MTEB Leaderboard(覆盖56个任务的embedding评测)
