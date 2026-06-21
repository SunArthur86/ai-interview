---
id: ai-scen-015
difficulty: L3
category: ai-scenario
subcategory: AI Agent系统设计
tags:
- 私有化部署
- vLLM
- 开源LLM
- Agent框架
- 量化部署
- 数据安全
feynman:
  essence: 基于开源模型和本地推理引擎，在受限硬件资源下构建安全可控的私有AI系统。
  analogy: 像自建机房，不租阿里云，用自己的服务器和开源软件搭建内部系统，数据绝对安全。
  first_principle: 如何在脱离外部API依赖的前提下，利用有限算力构建高性能的AI服务？
  key_points:
  - 选择高性能开源LLM（如Qwen、Llama）和推理引擎（如vLLM）。
  - 通过量化和批处理优化资源利用率。
  - 使用本地向量库和内网隔离确保数据安全。
  - 设计多租户隔离和审计机制满足合规。
follow_up:
- 开源72B模型与GPT-4的效果差距如何弥补？
- 如何在有限GPU资源下最大化并发？
- 私有化部署的Agent如何持续迭代？
---

# 设计一个Self-hosted的Agent框架。公司要求完全私有化部署，不依赖外部LLM API。

【场景分析】
私有化部署Agent的核心约束：数据不出域、硬件资源有限、需要自主可控的模型和工具链。

【技术选型】
1. **模型层**：
   - 开源LLM：Qwen2.5-72B / Llama3-70B / DeepSeek-V3
   - 推理引擎：vLLM（高吞吐）/ TGI / llama.cpp（CPU部署）
   - Embedding：BGE-large-zh / bge-m3（中英双语）
   - Reranker：bge-reranker-v2-m3
2. **向量库**：
   - Milvus（分布式）/ Qdrant（轻量）/ Chroma（嵌入式）
   - 全部支持本地部署，无云依赖
3. **Agent框架**：
   - LangGraph（有状态、可控）/ 自研轻量框架
   - 避免 LangChain 的过度抽象，保持可控性
4. **工具层**：
   - 自定义Tool：Python函数 → Function Calling
   - 数据库连接：SQLAlchemy + 只读权限
   - API调用：内部微服务接口

【部署架构】
- GPU节点：2-4张A100/A800（LLM推理）
- CPU节点：向量库 + 应用服务 + 消息队列
- 存储：SSD本地存储 + NAS共享
- 网络：VPC内网，不暴露公网

【实战案例】
在某银行私有化部署中，因金融数据极度敏感，我们使用**vLLM + RocksDB** 实现了完全本地化的KV Cache存储，确保推理过程中间态数据也绝不出域，解决了审计合规痛点。

【关键代码】（LangGraph 自定义工具定义）
```python
from langchain_core.tools import tool
import requests

@tool
def query_internal_crm(customer_id: str) -> str:
    """安全查询内部CRM客户信息的工具（只读）"""
    # 实际工程中应通过内网网关调用，而非直接连接数据库
    resp = requests.post(
        "http://internal-gateway.crm/api/query",
        json={"id": customer_id, "token": "INTERNAL_AUTH_KEY"},
        timeout=5
    )
    return resp.text.get("data", "User not found")
```

【技术选型对比】
| 特性 | LangChain | LangGraph | 自研框架 |
| :--- | :--- | :--- | :--- |
| **控制力** | 低（封装过深，Debug难） | 高（基于状态机，流程可控） | 极高（完全定制） |
| **状态管理** | 依赖内存传递 | 内置Cycle图，支持持久化 | 需自行实现Redis存储 |
| **适合场景** | 快速POC、简单链路 | 复杂Agent工作流、多轮协作 | 性能极致优化、特殊逻辑 |
| **学习成本** | 低 | 中 | 高 |

```text
     ┌───────────────────────────────────────────────────────────┐
     │                    用户/业务系统                           │
     └────────────────────────┬──────────────────────────────────┘
                              │ HTTPS/gRPC
                              ▼
     ┌───────────────────────────────────────────────────────────┐
     │              API 网关 (鉴权/限流/审计)                      │
     └──────┬─────────────────────────────────────┬───────────────┘
            │                                     │
            ▼                                     ▼
     ┌──────────────┐                    ┌──────────────┐
     │  Agent 服务  │ (编排/规划/记忆)    │  向量检索服务  │
     │ (LangGraph)  │◄──────────────────►│ (Milvus/Qdrant)│
     └──────┬───────┘                    └──────┬───────┘
            │ Function Call                      │
            ▼                                     │
     ┌──────────────┐                    ┌──────────────┐
     │  工具执行器  │                    │   向量数据    │
     │ (SQL/API)    │                    │   (本地SSD)   │
     └──────────────┘                    └──────────────┘
            │
            ▼ Inference
     ┌───────────────────────────────────────────────────────────┐
     │              LLM 推理集群 (vLLM/TGI)                       │
     │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐         │
     │  │ GPU:0   │ │ GPU:1   │ │ GPU:2   │
```
