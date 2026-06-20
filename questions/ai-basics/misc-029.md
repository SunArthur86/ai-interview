---
id: misc-029
difficulty: L2
category: ai-basics
subcategory: RAG与向量检索
tags:
- IOC
feynman:
  essence: 把模糊的用户提问转化为高质量、多样化的检索指令。
  analogy: 像去饭店点菜，把“随便来点好吃的”翻译成具体的“宫保鸡丁和鱼香肉丝”，厨师（检索系统）才好做。
  first_principle: 如何解决用户提问模糊、信息不全，导致检索系统找不到正确文档的问题？
  key_points:
  - HyDE生成假答案去反搜，语义更准
  - Step-Back Prompting先查背景再回答细节
  - Multi-Query多路召回防止遗漏
follow_up:
- HyDE在什么场景下效果最好?
- Multi-Query会增加多少延迟?
---

# RAG中的查询改写技术有哪些?HyDE和Step-Back Prompting分别解决什么问题

- **查询改写技术:**

- **1. Query Rewriting(查询改写):**
- 用LLM将用户模糊问题改写为更精确的检索查询
- 例:「怎么用那个东西」→「如何使用React Hooks」

- **2. HyDE (Hypothetical Document Embeddings):**
- 先让LLM生成一个假想答案
- 用假想答案的embedding去检索(而不是用原问题)
- 原理:答案比问题更接近目标文档的语义
- 效果:对于事实型问题检索质量大幅提升

- **3. Step-Back Prompting:**
- 将具体问题抽象为更宽泛的问题
- 例:「Google 2024 Q4收入」→「Google最近4个季度收入趋势」
- 先检索背景知识,再回答具体问题

- **4. Multi-Query:**
- 用LLM生成同一问题的多个变体
- 分别检索后取并集+去重+重排
