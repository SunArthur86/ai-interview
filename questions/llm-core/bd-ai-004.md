---
id: bd-ai-004
difficulty: L4
category: llm-core
categories:
- ai-agent
- eng-practice
- llm-core
subcategory: AI编程
tags:
- 字节跳动
- 面经
- Agent框架
- OpenClaw
- Hermes
- Claude Code
- 上下文管理
feynman:
  essence: Claude Code重集成易用，Hermes重技能封装，OpenClaw重可定制审计。
  analogy: 像办公软件：Claude是Mac（生态好开箱用），Hermes是瑞士军刀（功能全），OpenClaw是工作站（可折腾）。
  first_principle: 如何在有限的上下文窗口内高效管理记忆与工具？
  key_points:
  - Claude Code：自动压缩上下文，MCP集成最深
  - Hermes：结构化记忆与Skill能力包
  - OpenClaw：事件溯源，Plugin灵活
  - 编程选Claude，复杂业务流程选Hermes
follow_up:
- Agent的上下文压缩会丢失信息，怎么缓解？—— 用结构化记忆（如Hermes的memories/）保存关键事实，不依赖对话窗口
- 多Agent系统如何共享记忆？—— 用共享Memory Store（如向量数据库）或MCP Memory Server
- Claude Code的自动摘要质量如何保证？—— 用专门的summarization prompt + 保留关键代码块和决策点
---

# 【字节面经】对比OpenClaw/Hermes/Claude Code等Agent框架，从记忆机制、工具调用、上下文管理三个维度分析。

以下从三个核心维度深度对比当前主流的Agent框架。这里的"OpenClaw"指的是开源通用Agent框架（如OpenHands/类似项目），Hermes是Nous Research的Agent框架，Claude Code是Anthropic的CLI Agent。

**维度一：记忆机制**

| 框架 | 短期记忆 | 长期记忆 | 跨会话记忆 |
|------|---------|---------|-----------|
| Claude Code | 对话窗口 + 自动摘要压缩 | CLAUDE.md（项目级） | --resume 恢复会话 |
| Hermes | 对话窗口 + Skills记忆体 | Memories目录（JSON持久化） | Profile隔离的多Profile记忆 |
| OpenClaw | 对话窗口 + 事件流 | Workspace状态持久化 | 可选向量数据库集成 |

**关键差异：**
- **Claude Code** 采用"对话窗口+自动压缩"——超过上下文窗口时自动对早期对话做摘要，保留最近N轮原文。优点是无缝，缺点是早期细节可能丢失
- **Hermes** 采用"结构化记忆"——把重要事实存为memories/*.json，可以精确检索和修改。适合需要精确回溯的场景
- **OpenClaw** 采用"事件溯源"——记录所有Action/Observation对，可以replay。适合需要审计和debug的场景

**维度二：工具调用**

| 框架 | 工具定义方式 | 工具发现 | 并行调用 |
|------|------------|---------|---------|
| Claude Code | 内置Shell/FS + MCP Client | MCP Server自动发现 | 支持 |
| Hermes | Tools + Skills + MCP | 配置文件声明 + MCP | 支持 |
| OpenClaw | Plugin系统 | 注册式 | 有限支持 |

**关键差异：**
- **Claude Code** 的MCP集成最深——启动时自动加载~/.claude/下的MCP配置，工具发现是零配置的
- **Hermes** 的Skill系统最强——Skill=Prompt+工具+流程+记忆体，是最完整的能力封装
- **OpenClaw** 的Plugin最灵活——支持热加载，但配置较复杂

**维度三：上下文管理**

| 框架 | 窗口策略 | 上下文注入 | 分支/并行 |
|------|---------|-----------|----------|
| Claude Code | 自动摘要压缩 | CLAUDE.md + 文件引用 | --resume多会话 |
| Hermes | Token计数 + 智能裁剪 | Skills注入 + Memories检索 | Profile隔离 |
| OpenClaw | 可配置窗口管理 | Workspace注入 | Agent分支 |

**上下文管理深度分析：**

Claude Code的上下文压缩策略：
```
原始对话: [msg1, msg2, ..., msg50]  # 超出窗口
压缩后:   [summary(msg1-30), msg31, ..., msg50]
          └── 摘要替代原文 ──┘  └── 保留近期原文 ──┘
```

Hermes的上下文注入策略：
```
系统Prompt = 固定指令
          + Skills定义（按需注入相关Skill）
          + Memories检索（语义搜索相关记忆）
          + 工具Schema
          + 当前对话
```

**选型建议：**
- **日常编程/快速原型** → Claude Code（零配置，开箱即用）
- **需要持久记忆/多Profile** → Hermes（结构化记忆，Profile隔离）
- **需要审计/可定制** → OpenClaw（事件溯源，Plugin灵活）

**架构启示：** 一个好的Agent框架需要在三个维度平衡——记忆不能太重（影响速度）也不能太轻（丢失上下文）；工具调用要灵活但有安全边界；上下文管理要自动但可干预。目前没有"完美"框架，选型应基于场景需求。
