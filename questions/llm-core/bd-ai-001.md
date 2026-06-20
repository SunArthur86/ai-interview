---
id: bd-ai-001
difficulty: L2
category: llm-core
categories:
- ai-agent
- eng-practice
- llm-core
subcategory: AI编程
tags:
- 字节跳动
- 面经
- AI编程
- Cursor
- Copilot
- Claude Code
feynman:
  essence: Copilot 补全行，Cursor 改全库，Claude Code 自主执行任务。
  analogy: 自动纠错、改全卷、请个助教代写作业。
  first_principle: 如何利用不同的自动化层级最大化编码效率？
  key_points:
  - Copilot 适合单行补全，低延迟流式编码
  - Cursor 适合跨文件重构，具备项目级上下文
  - Claude Code 可自主执行命令和测试，处理多步任务
  - Web 端适合架构设计和非编码思考任务
follow_up:
- Copilot的补全有时会"跑偏"，怎么提高准确率？—— 用注释引导意图、保持函数签名清晰、用@引用相关文件
- Cursor的Codebase索引和纯RAG有什么区别？—— Cursor结合AST+嵌入检索，能理解import关系和调用链
- 如何评估一个AI编程工具的ROI？—— 从编码效率提升、Bug率变化、Onboarding时间缩短三个维度量化
---

# 【字节面经】平常用什么AI编程工具？各自的特点和使用场景是什么？

在日常开发中，我根据不同场景组合使用多种AI编程工具，核心原则是"让工具匹配场景"。

**1. GitHub Copilot — 行级/函数级补全**
- **特点：** IDE深度集成（VS Code/JetBrains），实时单行/多行补全，延迟低（<200ms），基于Codex/GPT模型
- **场景：** 写样板代码（CRUD、DTO、测试用例）、补全已知API调用、快速生成正则/SQL
- **局限：** 上下文窗口短（~2048 tokens），无法跨文件理解项目结构

**2. Cursor — 全文件/多文件编辑**
- **特点：** Fork自VS Code，内置Claude/GPT-4，支持`@file`、`@codebase`引用，Cmd+K局部重写，Cmd+L全项目对话
- **场景：** 重构跨文件逻辑、生成新模块、Code Review、理解陌生代码库
- **优势：** Codebase Indexing用嵌入检索+AST分析，能"看到"整个项目

**3. Claude Code (CLI Agent) — 自主任务执行**
- **特点：** 终端运行，能自主读写文件、执行命令、运行测试，支持多轮自主迭代
- **场景：** 批量迁移代码（如Python 2→3）、搭建项目骨架、修复CI失败、做复杂的多步骤重构

**4. ChatGPT/Claude Web — 设计讨论/方案验证**
- **场景：** 架构设计讨论、技术选型对比、写文档/PR描述、debug思路探讨
- **优势：** 不受IDE限制，适合"思考型"任务而非"编码型"任务

**5. Windsurf/Continue — 开源替代**
- **特点：** Continue可接入任意模型（本地Ollama/远程API），Windsurf强调Cascade多步编辑

**工具选型决策树：**
```
需要写代码？
├─ 单行/函数补全 → Copilot
├─ 跨文件重构 → Cursor (Cmd+K/L)
├─ 自主完成多步任务 → Claude Code
└─ 只讨论不写 → ChatGPT/Claude Web
```

**实践心得：** 工具不是越多越好。日常80%时间用Cursor（编辑+对话）+ Copilot（补全），遇到复杂批量任务才启动Claude Code。关键在于建立"AI工具肌肉记忆"——每个工具的快捷键、引用语法、上下文边界都要熟练，才能在编码心流中无缝切换。
