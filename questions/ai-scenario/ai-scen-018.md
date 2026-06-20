---
id: ai-scen-018
difficulty: L3
category: ai-scenario
subcategory: AI对话系统设计
tags:
- 语音Agent
- ASR
- TTS
- VAD
- 实时对话
- 打断处理
- 端云协同
feynman:
  essence: 构建全链路流式语音处理管道，通过ASR/LLM/TTS并行和状态机管理实现毫秒级响应。
  analogy: 像同声传译，耳朵听进去的同时脑子在转，嘴巴马上说出来，还能随时被打断。
  first_principle: 如何在处理听、想、说三个串行步骤时，将端到端延迟压缩到人类可接受的范围？
  key_points:
  - 采用流式ASR和流式TTS，配合LLM流式生成。
  - 使用VAD检测语音活动，设计状态机管理交互。
  - 打断时立即停止TTS和LLM，保留上下文。
  - 端云协同优化延迟，简单指令端侧执行。
follow_up:
- 如何处理嘈杂环境下的语音识别？
- 端侧部署ASR/TTS有哪些技术选型？
- 语音Agent如何管理多轮对话的上下文？
---

# 如何设计一个实时语音AI助手？支持语音输入、实时对话、语音输出，延迟控制在1秒以内。

【场景分析】
实时语音Agent是最具挑战的AI系统之一：多模态链路（ASR->LLM->TTS）、低延迟要求、打断处理、状态管理。

【系统架构】
1. **音频输入处理**：
   - 音频采集：WebSocket传输音频流（16kHz PCM/Opus）
   - VAD（语音活动检测）：Silero VAD检测说话开始/结束
   - 流式ASR：Whisper-streaming / Paraformer流式版
   - 延迟优化：分块识别，边说边转
2. **对话推理**：
   - LLM流式生成：首Token延迟 < 300ms
   - 上下文管理：多轮对话历史 + 系统人设
   - 工具调用：查天气、设闹钟等
3. **语音合成（TTS）**：
   - 流式TTS：逐句合成，不等完整回复
   - 模型：CosyVoice / GPT-SoVITS / Edge-TTS
   - 声纹克隆：可选个性化音色
4. **音频输出**：
   - 流式播放：边合成边播放
   - 打断处理：检测到用户说话 → 立即停止播放

```text
用户音频流 (PCM)
    │
    ▼
┌───────────────┐
│   VAD 检测    │ ◄─── [静音切除/语音段切分]
└───────┬───────┘
        │ (语音块 Chunk)
        ▼
┌───────────────┐
│  流式 ASR     │ ──► Partial Text (中间结果)
│ (Whisper/Para)│ ──► Final Text (最终结果)
└───────┬───────┘
        │ Text
        ▼
┌───────────────┐
│   LLM 推理     │ ──► Streaming Text Tokens
│ (vLLM流式)     │
└───────┬───────┘
        │ Text Tokens (流式)
        ▼
┌───────────────┐
│  流式 TTS      │ ──► Audio Chunks
│ (VITS/SoVITS)  │
└───────┬───────┘
        │ Audio Chunks
        ▼
┌───────────────┐
│  客户端播放    │
└───────────────┘
```

【延迟拆解】
VAD判断 50ms + ASR转写 200ms + LLM首字 300ms + TTS首包 200ms + 网络传输 100ms = 总计约850ms

【状态机设计】
States: IDLE -> LISTENING -> THINKING -> SPEAKING -> IDLE
用户打断: SPEAKING -> INTERRUPTED -> LISTENING
- LISTENING：VAD检测到语音 → 流式ASR
- THINKING：ASR完成 → LLM流式生成
- SPEAKING：TTS流式合成 + 播放
- INTERRUPTED：用户打断 → 停止播放 → 回到LISTENING

```text
       ┌─────────┐
       │  IDLE   │ (等待输入)
       └────┬────┘
            │ VAD Start
            ▼
       ┌─────────┐
       │LISTENING│ (ASR中...)
       └────┬────┘
            │ VAD End (说话结束)
            ▼
       ┌─────────┐
       │THINKING │ (LLM推理中...)
       └────┬────┘
            │ TTS Start
            ▼
       ┌─────────┐    VAD Start (Barge-in)
       │SPEAKING │ ──────────────────┐
       └────┬────┘                   │
            │ Finish / Interrupt     │
            ▼                         ▼
       ┌─────────┐              ┌──────────┐
       │  IDLE   │              │INTERRUPTED│ (停止播放/取消推理)
       └─────────┘              └─────┬────┘
                                      │
                                      ▼
                                 ┌─────────┐
                                 │LISTENING│
                                 └─────────┘
```

【打断处理】
1. 停止TTS播放
2. 取消LLM推理（节省Token）
3. 保留已播放内容到上下文
4. 开始处理新的用户输入

【端云协同方案】
- 端侧：VAD + 轻量ASR（快速响应）
- 云端：大模型推理 + TTS
- 混合：简单指令端侧处理，复杂对话云端处理

## 常见考点
1. **如何进一步降低端到端延迟？**
   - **并行处理**：在LLM生成完整句子之前，只要生成了一个完整的短语或从句，就立即推送给TTS合成，不需要等LLM生成EOS标记。
   - **音频压缩**：使用Opus编码代替PCM，大幅降低网络传输带宽和延迟。
   - **预加载**：在VAD检测到语音开始的同时，预先启动LLM的Prefill阶段（如果使用Partial Text作为输入，虽然会有错误但能抢时间）。
2. **回声消除（AEC）与打断的冲突如何解决？**
   - 如果不消除回声，机器听到自己的声音会误判为用户在说话。必须在前端或服务端部署AEC（声学回声消除）模块，消除播放声音对麦克风的干扰，确保VAD只检测到用户的声音。
3. **半双工 vs 全双工 的区别？**
   - **半双工（当前方案）**：必须等用户说完（VAD检测静音）才开始处理。缺点是自然度稍差，但实现稳定。
   - **全双工（GPT-4o模式）**：用户说话的同时机器也在听和处理，可以随时插话。这要求ASR和LLM具备极高的流式处理能力和更强的“抗干扰”能力。
