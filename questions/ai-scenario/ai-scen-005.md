---
id: ai-scen-005
difficulty: L2
category: ai-scenario
subcategory: RAG系统设计
tags:
- Chunking策略
- 语义分块
- 文档预处理
- 父子chunk
- RAG优化
feynman:
  essence: 平衡语义完整性与检索粒度，针对内容类型选择最佳切分策略。
  analogy: 切面包，太厚不好吃（精度低），太薄易碎（无上下文），要顺着纹理切（语义切分）。
  first_principle: 如何将长文本切分成既包含独立语义又利于检索匹配的最小单元？
  key_points:
  - 语义分块：保持句子完整，优于定长切分
  - 结构化分块：利用标题层级保留上下文
  - 特殊处理：表格、代码按逻辑单元切
  - 父子索引：小粒度检索，大粒度生成
follow_up:
- 如何自动检测最佳chunk大小？
- 对于中英混排的文档，分块策略需要调整吗？
- 父子chunk方案如何影响检索和存储成本？
---

# 在RAG系统中如何设计有效的Chunking策略？不同类型的文档应该用什么分块方法？

【场景分析】
Chunking是RAG最关键的预处理环节——分块太大有信息稀释，太小丢失上下文，错位切分破坏语义完整性。

【分块策略矩阵】
1. 固定窗口分块（Baseline）：
   - 按Token数切分（如500 tokens），滑窗重叠100 tokens
   - 适用：纯文本、FAQ、聊天记录
   - 优点：简单稳定；缺点：可能切断句子
2. 语义分块（推荐）：
   - 基于句子边界 + 语义连贯性检测
   - 工具：spaCy/LangChain RecursiveCharacterTextSplitter
   - 策略：先按段落分，段落内按句子分，保持完整句子
   - 适用：文章、报告、文档
3. 结构化分块（Markdown/HTML）：
   - 按标题层级分块（H1→H2→H3）
   - 每个chunk携带父级标题作为上下文
   - 适用：技术文档、Wiki、产品手册
4. 表格/代码特殊处理：
   - 表格：整表作为chunk + 自然语言摘要
   - 代码：按函数/类边界分块
   - 公式：保留LaTeX完整性
5. 混合粒度分块（Advanced）：
   - 同时生成大chunk（1000t）和小chunk（200t）
   - 大chunk用于生成上下文，小chunk用于精准检索
   - 父子chunk关联：命中子chunk时召回父chunk

【Chunk元数据设计】
- 必须携带：source_doc_id, page_num, section_title, chunk_type
- 权限标签：access_level, department
- 时间戳：created_at, updated_at

【参数调优】
- chunk_size: 256~1024 tokens（根据文档类型）
- overlap: 10%~20%的chunk_size
- 评测：不同参数下的Recall@K和答案质量
