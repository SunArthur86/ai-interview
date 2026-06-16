#!/usr/bin/env python3
"""
Generate SVG diagrams for AI interview questions.
Creates clear, educational diagrams for key AI/ML concepts.
"""

import os

IMG_DIR = "/opt/data/projects/ai-interview/images"
os.makedirs(IMG_DIR, exist_ok=True)

# ============================================================
# SVG Diagrams
# ============================================================

def save_svg(filename, svg_content):
    path = os.path.join(IMG_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    return filename

# --- 1. Transformer Architecture ---
svg_transformer = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 450" style="background:#f8f9fa;border-radius:12px;font-family:system-ui,sans-serif">
<defs><style>.box{fill:#e3f2fd;stroke:#1565c0;stroke-width:2;rx:8}.lbl{font-size:13px;fill:#333;text-anchor:middle}.arr{stroke:#666;stroke-width:1.5;fill:none;marker-end:url(#a)}</style>
<marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0L8,4L0,8Z" fill="#666"/></marker></defs>
<!-- Input -->
<rect x="50" y="30" width="120" height="35" class="box"/><text x="110" y="52" class="lbl">Input Embedding</text>
<rect x="50" y="75" width="120" height="30" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="6"/><text x="110" y="94" class="lbl">+ Positional Encoding</text>
<line x1="110" y1="105" x2="110" y2="130" class="arr"/>
<!-- Multi-Head Attention -->
<rect x="30" y="130" width="160" height="50" fill="#e8eaf6" stroke="#283593" stroke-width="2" rx="8"/>
<text x="110" y="152" class="lbl" style="font-weight:600">Multi-Head Self-Attention</text>
<text x="110" y="168" class="lbl" style="font-size:11px;fill:#666">Q, K, V → softmax(QK^T/√d)V</text>
<line x1="110" y1="180" x2="110" y2="195" class="arr"/>
<!-- Add & Norm -->
<rect x="40" y="195" width="140" height="30" fill="#e0f2f1" stroke="#00695c" stroke-width="2" rx="6"/>
<text x="110" y="214" class="lbl">Add &amp; LayerNorm</text>
<line x1="110" y1="225" x2="110" y2="240" class="arr"/>
<!-- FFN -->
<rect x="40" y="240" width="140" height="40" fill="#fce4ec" stroke="#880e4f" stroke-width="2" rx="8"/>
<text x="110" y="258" class="lbl" style="font-weight:600">Feed Forward (FFN)</text>
<text x="110" y="272" class="lbl" style="font-size:11px;fill:#666">Linear → SwiGLU → Linear</text>
<line x1="110" y1="280" x2="110" y2="295" class="arr"/>
<!-- Add & Norm 2 -->
<rect x="40" y="295" width="140" height="30" fill="#e0f2f1" stroke="#00695c" stroke-width="2" rx="6"/>
<text x="110" y="314" class="lbl">Add &amp; LayerNorm</text>
<!-- Residual connections -->
<path d="M 25,130 Q 15,130 15,195 L 40,195" stroke="#4caf50" stroke-width="2" fill="none" stroke-dasharray="4,2"/>
<path d="M 25,195 Q 15,195 15,295 L 40,295" stroke="#4caf50" stroke-width="2" fill="none" stroke-dasharray="4,2"/>
<!-- Right side: MHA detail -->
<rect x="280" y="120" width="290" height="120" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2" rx="8"/>
<text x="425" y="140" class="lbl" style="font-weight:600;color:#6a1b9a">Multi-Head Attention Detail</text>
<rect x="300" y="150" width="60" height="25" fill="#bbdefb" stroke="#1565c0" rx="4"/><text x="330" y="167" class="lbl" style="font-size:11px">Head 1</text>
<rect x="370" y="150" width="60" height="25" fill="#bbdefb" stroke="#1565c0" rx="4"/><text x="400" y="167" class="lbl" style="font-size:11px">Head 2</text>
<rect x="440" y="150" width="60" height="25" fill="#bbdefb" stroke="#1565c0" rx="4"/><text x="470" y="167" class="lbl" style="font-size:11px">Head N</text>
<line x1="330" y1="175" x2="330" y2="190" class="arr"/>
<line x1="400" y1="175" x2="400" y2="190" class="arr"/>
<line x1="470" y1="175" x2="470" y2="190" class="arr"/>
<rect x="320" y="190" width="200" height="25" fill="#e1bee7" stroke="#6a1b9a" rx="4"/><text x="420" y="207" class="lbl" style="font-size:11px">Concat → Linear</text>
<!-- Output -->
<rect x="50" y="340" width="120" height="35" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="8"/>
<text x="110" y="362" class="lbl">Output</text>
<!-- N× label -->
<text x="200" y="225" style="font-size:20px;font-weight:700;fill:#999">N×</text>
</svg>'''

# --- 2. Attention Mechanism (Scaled Dot-Product) ---
svg_attention = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 550 280" style="background:#f8f9fa;border-radius:12px;font-family:system-ui,sans-serif">
<defs><marker id="b" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0L8,4L0,8Z" fill="#666"/></marker></defs>
<!-- Q, K, V inputs -->
<rect x="30" y="30" width="60" height="30" fill="#e3f2fd" stroke="#1565c0" rx="6"/><text x="60" y="49" text-anchor="middle" font-size="14" font-weight="600">Q</text>
<rect x="30" y="70" width="60" height="30" fill="#e3f2fd" stroke="#1565c0" rx="6"/><text x="60" y="89" text-anchor="middle" font-size="14" font-weight="600">K</text>
<rect x="30" y="110" width="60" height="30" fill="#e3f2fd" stroke="#1565c0" rx="6"/><text x="60" y="129" text-anchor="middle" font-size="14" font-weight="600">V</text>
<!-- MatMul QK^T -->
<line x1="90" y1="55" x2="160" y2="80" stroke="#666" stroke-width="1.5" marker-end="url(#b)"/>
<line x1="90" y1="85" x2="160" y2="80" stroke="#666" stroke-width="1.5" marker-end="url(#b)"/>
<rect x="160" y="65" width="80" height="35" fill="#fff3e0" stroke="#e65100" rx="6"/>
<text x="200" y="82" text-anchor="middle" font-size="11">MatMul</text><text x="200" y="95" text-anchor="middle" font-size="10" fill="#666">Q × K^T</text>
<!-- Scale -->
<line x1="240" y1="82" x2="280" y2="82" stroke="#666" stroke-width="1.5" marker-end="url(#b)"/>
<rect x="280" y="65" width="60" height="35" fill="#fce4ec" stroke="#880e4f" rx="6"/>
<text x="310" y="82" text-anchor="middle" font-size="11">Scale</text><text x="310" y="95" text-anchor="middle" font-size="10" fill="#666">÷√d_k</text>
<!-- Softmax -->
<line x1="340" y1="82" x2="380" y2="82" stroke="#666" stroke-width="1.5" marker-end="url(#b)"/>
<rect x="380" y="65" width="70" height="35" fill="#e8eaf6" stroke="#283593" rx="6"/>
<text x="415" y="82" text-anchor="middle" font-size="11">Softmax</text>
<!-- MatMul with V -->
<line x1="450" y1="82" x2="490" y2="82" stroke="#666" stroke-width="1.5" marker-end="url(#b)"/>
<line x1="90" y1="125" x2="490" y2="110" stroke="#666" stroke-width="1.5" marker-end="url(#b)" stroke-dasharray="3,2"/>
<rect x="490" y="65" width="50" height="35" fill="#fff3e0" stroke="#e65100" rx="6"/>
<text x="515" y="82" text-anchor="middle" font-size="10">MatMul</text>
<!-- Output -->
<line x1="515" y1="100" x2="515" y2="130" stroke="#666" stroke-width="1.5" marker-end="url(#b)"/>
<rect x="475" y="130" width="80" height="30" fill="#e8f5e9" stroke="#2e7d32" rx="6"/>
<text x="515" y="150" text-anchor="middle" font-size="13" font-weight="600">Output</text>
<!-- Attention weights visualization -->
<text x="275" y="180" text-anchor="middle" font-size="12" fill="#333" font-weight="600">Attention Weights (softmax)</text>
<g transform="translate(150,190)">
<rect x="0" y="0" width="40" height="60" fill="#1565c0" opacity="0.9"/><text x="20" y="35" text-anchor="middle" font-size="10" fill="white" font-weight="600">0.7</text>
<rect x="45" y="10" width="40" height="50" fill="#1565c0" opacity="0.6"/><text x="65" y="35" text-anchor="middle" font-size="10" fill="white">0.2</text>
<rect x="90" y="20" width="40" height="40" fill="#1565c0" opacity="0.3"/><text x="110" y="40" text-anchor="middle" font-size="10" fill="#333">0.08</text>
<rect x="135" y="25" width="40" height="35" fill="#1565c0" opacity="0.15"/><text x="155" y="42" text-anchor="middle" font-size="10" fill="#333">0.02</text>
<rect x="180" y="27" width="40" height="33" fill="#1565c0" opacity="0.1"/><text x="200" y="42" text-anchor="middle" font-size="10" fill="#333">0</text>
</g>
<text x="200" y="270" text-anchor="middle" font-size="10" fill="#666">Token 1 attends more to Token 1 (self), less to others</text>
</svg>'''

# --- 3. LoRA (Low-Rank Adaptation) ---
svg_lora = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 250" style="background:#f8f9fa;border-radius:12px;font-family:system-ui,sans-serif">
<defs><marker id="c" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0L8,4L0,8Z" fill="#666"/></marker></defs>
<!-- Original W (frozen) -->
<rect x="50" y="50" width="120" height="120" fill="#e0e0e0" stroke="#9e9e9e" stroke-width="3" rx="4"/>
<text x="110" y="105" text-anchor="middle" font-size="28" font-weight="700" fill="#999">W</text>
<text x="110" y="130" text-anchor="middle" font-size="12" fill="#999">Frozen ❄️</text>
<text x="110" y="40" text-anchor="middle" font-size="13" fill="#333">Pre-trained Weights</text>
<text x="110" y="185" text-anchor="middle" font-size="11" fill="#666">d × d (e.g. 4096×4096)</text>
<!-- + -->
<text x="200" y="115" text-anchor="middle" font-size="24" fill="#4caf50" font-weight="700">+</text>
<!-- LoRA: B × A -->
<rect x="230" y="50" width="50" height="120" fill="#e8f5e9" stroke="#4caf50" stroke-width="2" rx="4"/>
<text x="255" y="105" text-anchor="middle" font-size="20" font-weight="700" fill="#2e7d32">B</text>
<text x="255" y="40" text-anchor="middle" font-size="11" fill="#2e7d32">d × r</text>
<text x="290" y="115" text-anchor="middle" font-size="16" fill="#666">×</text>
<rect x="300" y="50" width="120" height="50" fill="#e8f5e9" stroke="#4caf50" stroke-width="2" rx="4"/>
<text x="360" y="80" text-anchor="middle" font-size="20" font-weight="700" fill="#2e7d32">A</text>
<text x="360" y="40" text-anchor="middle" font-size="11" fill="#2e7d32">r × d</text>
<!-- Trainable -->
<rect x="230" y="180" width="190" height="25" fill="#c8e6c9" stroke="#4caf50" stroke-width="1" rx="6"/>
<text x="325" y="197" text-anchor="middle" font-size="12" fill="#2e7d32" font-weight="600">Trainable 🔥 (r=8)</text>
<!-- Output -->
<line x1="420" y1="110" x2="450" y2="110" stroke="#666" stroke-width="1.5" marker-end="url(#c)"/>
<text x="455" y="115" font-size="13" fill="#333">W' = W + BA</text>
<!-- Param comparison -->
<rect x="30" y="215" width="440" height="28" fill="#fff8e1" stroke="#ffc107" rx="6"/>
<text x="250" y="233" text-anchor="middle" font-size="11" fill="#666">Full: 16.7M params → LoRA: 65K params (256× fewer, same output shape)</text>
</svg>'''

# --- 4. RAG Architecture ---
svg_rag = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 380" style="background:#f8f9fa;border-radius:12px;font-family:system-ui,sans-serif">
<defs><marker id="d" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0L8,4L0,8Z" fill="#666"/></marker>
<style>.b{rx:8}.t{font-size:12px;text-anchor:middle;fill:#333}.s{font-size:10px;text-anchor:middle;fill:#666}</style></defs>
<!-- Offline section -->
<rect x="10" y="10" width="270" height="220" fill="#f3e5f5" opacity="0.15" stroke="#9c27b0" stroke-dasharray="5,3" rx="10"/>
<text x="145" y="28" text-anchor="middle" font-size="13" font-weight="600" fill="#9c27b0">📦 Offline: Indexing</text>
<!-- Documents -->
<rect x="30" y="40" width="100" height="30" fill="#e3f2fd" stroke="#1565c0" class="b"/><text x="80" y="59" class="t">📄 Documents</text>
<line x1="80" y1="70" x2="80" y2="85" stroke="#666" stroke-width="1.5" marker-end="url(#d)"/>
<!-- Chunking -->
<rect x="30" y="85" width="100" height="30" fill="#fff3e0" stroke="#e65100" class="b"/><text x="80" y="104" class="t">✂️ Chunking</text>
<text x="80" y="120" class="s">split into pieces</text>
<line x1="80" y1="120" x2="80" y2="135" stroke="#666" stroke-width="1.5" marker-end="url(#d)"/>
<!-- Embedding -->
<rect x="30" y="135" width="100" height="30" fill="#e8eaf6" stroke="#283593" class="b"/><text x="80" y="154" class="t">🔢 Embedding</text>
<text x="80" y="170" class="s">text → vectors</text>
<line x1="130" y1="150" x2="180" y2="150" stroke="#666" stroke-width="1.5" marker-end="url(#d)"/>
<!-- Vector DB -->
<rect x="180" y="120" width="90" height="60" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="8"/>
<text x="225" y="145" text-anchor="middle" font-size="12" font-weight="600" fill="#2e7d32">🗄️ Vector DB</text>
<text x="225" y="162" class="s">Milvus/Pinecone</text>

<!-- Online section -->
<rect x="300" y="10" width="290" height="370" fill="#e3f2fd" opacity="0.15" stroke="#1565c0" stroke-dasharray="5,3" rx="10"/>
<text x="445" y="28" text-anchor="middle" font-size="13" font-weight="600" fill="#1565c0">⚡ Online: Query</text>
<!-- User Query -->
<rect x="340" y="40" width="200" height="30" fill="#fce4ec" stroke="#880e4f" class="b"/><text x="440" y="59" class="t">❓ User Query</text>
<line x1="440" y1="70" x2="440" y2="85" stroke="#666" stroke-width="1.5" marker-end="url(#d)"/>
<!-- Embed query -->
<rect x="350" y="85" width="180" height="25" fill="#e8eaf6" stroke="#283593" class="b"/><text x="440" y="102" class="t">🔢 Embed Query</text>
<!-- Vector search arrow -->
<line x1="350" y1="110" x2="270" y2="140" stroke="#ff5722" stroke-width="2" stroke-dasharray="4,2" marker-end="url(#d)"/>
<text x="310" y="120" font-size="10" fill="#ff5722">similarity search</text>
<!-- Retrieve -->
<rect x="350" y="125" width="180" height="25" fill="#fff3e0" stroke="#e65100" class="b"/><text x="440" y="142" class="t">🔍 Top-K Retrieved Chunks</text>
<line x1="440" y1="150" x2="440" y2="165" stroke="#666" stroke-width="1.5" marker-end="url(#d)"/>
<!-- Rerank (optional) -->
<rect x="350" y="165" width="180" height="25" fill="#f3e5f5" stroke="#6a1b9a" class="b"/><text x="440" y="182" class="t">📊 Rerank (optional)</text>
<line x1="440" y1="190" x2="440" y2="205" stroke="#666" stroke-width="1.5" marker-end="url(#d)"/>
<!-- Prompt construction -->
<rect x="340" y="205" width="200" height="35" fill="#e0f7fa" stroke="#006064" class="b"/>
<text x="440" y="222" class="t">📝 Construct Prompt</text>
<text x="440" y="234" class="s">context + question</text>
<line x1="440" y1="240" x2="440" y2="255" stroke="#666" stroke-width="1.5" marker-end="url(#d)"/>
<!-- LLM -->
<rect x="350" y="255" width="180" height="35" fill="#e8eaf6" stroke="#283593" stroke-width="2" class="b"/>
<text x="440" y="272" class="t" font-weight="600">🧠 LLM (GPT/Claude)</text>
<text x="440" y="284" class="s">generate answer</text>
<line x1="440" y1="290" x2="440" y2="305" stroke="#666" stroke-width="1.5" marker-end="url(#d)"/>
<!-- Answer -->
<rect x="350" y="305" width="180" height="30" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" class="b"/>
<text x="440" y="324" class="t" font-weight="600">✅ Answer + Sources</text>
</svg>'''

# --- 5. KV Cache ---
svg_kvcache = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 550 320" style="background:#f8f9fa;border-radius:12px;font-family:system-ui,sans-serif">
<defs><style>.t{font-size:12px;text-anchor:middle;fill:#333}.s{font-size:10px;fill:#666}</style></defs>
<text x="275" y="25" text-anchor="middle" font-size="14" font-weight="700" fill="#333">KV Cache: Avoid Recomputing Previous Tokens</text>
<!-- Step 1: Generate token 1 -->
<text x="275" y="50" text-anchor="middle" font-size="12" fill="#1565c0" font-weight="600">Step 1: Process "Hello"</text>
<rect x="180" y="60" width="50" height="25" fill="#bbdefb" stroke="#1565c0" rx="4"/><text x="205" y="77" class="t">K₁</text>
<rect x="240" y="60" width="50" height="25" fill="#c8e6c9" stroke="#2e7d32" rx="4"/><text x="265" y="77" class="t">V₁</text>
<rect x="310" y="55" width="40" height="30" fill="#fff3e0" stroke="#e65100" rx="4"/><text x="330" y="75" class="t">Hello</text>
<!-- Step 2: Generate token 2 -->
<text x="275" y="110" text-anchor="middle" font-size="12" fill="#1565c0" font-weight="600">Step 2: Process "World" (K₁,V₁ cached!)</text>
<rect x="130" y="120" width="50" height="25" fill="#bbdefb" stroke="#1565c0" rx="4"/><text x="155" y="137" class="t">K₁ 🔒</text>
<rect x="190" y="120" width="50" height="25" fill="#c8e6c9" stroke="#2e7d32" rx="4"/><text x="215" y="137" class="t">V₁ 🔒</text>
<rect x="260" y="120" width="50" height="25" fill="#90caf9" stroke="#1565c0" rx="4"/><text x="285" y="137" class="t">K₂</text>
<rect x="320" y="120" width="50" height="25" fill="#a5d6a7" stroke="#2e7d32" rx="4"/><text x="345" y="137" class="t">V₂</text>
<rect x="390" y="115" width="40" height="30" fill="#fff3e0" stroke="#e65100" rx="4"/><text x="410" y="135" class="t">World</text>
<!-- Step 3 -->
<text x="275" y="170" text-anchor="middle" font-size="12" fill="#1565c0" font-weight="600">Step 3: Generate "!" (K₁V₁ K₂V₂ cached!)</text>
<rect x="80" y="180" width="50" height="25" fill="#bbdefb" stroke="#1565c0" rx="4"/><text x="105" y="197" class="t">K₁ 🔒</text>
<rect x="140" y="180" width="50" height="25" fill="#c8e6c9" stroke="#2e7d32" rx="4"/><text x="165" y="197" class="t">V₁ 🔒</text>
<rect x="210" y="180" width="50" height="25" fill="#bbdefb" stroke="#1565c0" rx="4"/><text x="235" y="197" class="t">K₂ 🔒</text>
<rect x="270" y="180" width="50" height="25" fill="#c8e6c9" stroke="#2e7d32" rx="4"/><text x="295" y="197" class="t">V₂ 🔒</text>
<rect x="340" y="180" width="50" height="25" fill="#64b5f6" stroke="#1565c0" rx="4"/><text x="365" y="197" class="t">K₃</text>
<rect x="400" y="180" width="50" height="25" fill="#66bb6a" stroke="#2e7d32" rx="4"/><text x="425" y="197" class="t">V₃</text>
<rect x="470" y="175" width="30" height="30" fill="#fff3e0" stroke="#e65100" rx="4"/><text x="485" y="195" class="t">!</text>
<!-- Without cache comparison -->
<rect x="30" y="230" width="500" height="75" fill="#ffebee" stroke="#c62828" rx="8"/>
<text x="280" y="250" text-anchor="middle" font-size="12" fill="#c62828" font-weight="600">❌ Without KV Cache</text>
<text x="280" y="268" text-anchor="middle" font-size="11" fill="#666">Each step recomputes ALL previous tokens → O(n²) per step → O(n³) total</text>
<text x="280" y="285" text-anchor="middle" font-size="11" fill="#2e7d32" font-weight="600">✅ With KV Cache: Only compute new token → O(n) per step → O(n²) total</text>
<text x="280" y="300" text-anchor="middle" font-size="10" fill="#666">Trade-off: KV Cache memory grows linearly with sequence length</text>
</svg>'''

# --- 6. MoE (Mixture of Experts) ---
svg_moe = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 550 300" style="background:#f8f9fa;border-radius:12px;font-family:system-ui,sans-serif">
<defs><style>.t{font-size:12px;text-anchor:middle;fill:#333}</style></defs>
<text x="275" y="25" text-anchor="middle" font-size="14" font-weight="700" fill="#333">MoE: Only Top-K Experts are Activated per Token</text>
<!-- Input token -->
<rect x="230" y="40" width="90" height="30" fill="#e3f2fd" stroke="#1565c0" rx="8"/><text x="275" y="59" class="t">Input Token</text>
<line x1="275" y1="70" x2="275" y2="85" stroke="#666" stroke-width="1.5"/>
<!-- Router/Gate -->
<rect x="200" y="85" width="150" height="30" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="8"/>
<text x="275" y="104" class="t" font-weight="600">🔀 Router / Gate</text>
<text x="275" y="120" text-anchor="middle" font-size="10" fill="#666">scores all experts, picks Top-2</text>
<!-- Expert boxes -->
<g transform="translate(50,130)">
<rect width="80" height="50" fill="#e8f5e9" stroke="#2e7d32" stroke-width="3" rx="6"/><text x="40" y="22" class="t">Expert 1</text><text x="40" y="38" text-anchor="middle" font-size="10" fill="#2e7d32" font-weight="600">✅ Selected</text>
<rect x="100" y="0" width="80" height="50" fill="#fafafa" stroke="#bbb" stroke-width="1" rx="6"/><text x="140" y="22" class="t" fill="#999">Expert 2</text><text x="140" y="38" text-anchor="middle" font-size="10" fill="#999">❌</text>
<rect x="200" y="0" width="80" height="50" fill="#e8f5e9" stroke="#2e7d32" stroke-width="3" rx="6"/><text x="240" y="22" class="t">Expert 3</text><text x="240" y="38" text-anchor="middle" font-size="10" fill="#2e7d32" font-weight="600">✅ Selected</text>
<rect x="300" y="0" width="80" height="50" fill="#fafafa" stroke="#bbb" stroke-width="1" rx="6"/><text x="340" y="22" class="t" fill="#999">Expert 4</text><text x="340" y="38" text-anchor="middle" font-size="10" fill="#999">❌</text>
<rect x="0" y="60" width="80" height="50" fill="#fafafa" stroke="#bbb" stroke-width="1" rx="6"/><text x="40" y="82" class="t" fill="#999">Expert 5</text><text x="40" y="98" text-anchor="middle" font-size="10" fill="#999">❌</text>
<rect x="100" y="60" width="80" height="50" fill="#fafafa" stroke="#bbb" stroke-width="1" rx="6"/><text x="140" y="82" class="t" fill="#999">Expert 6</text><text x="140" y="98" text-anchor="middle" font-size="10" fill="#999">❌</text>
<rect x="200" y="60" width="80" height="50" fill="#fafafa" stroke="#bbb" stroke-width="1" rx="6"/><text x="240" y="82" class="t" fill="#999">Expert 7</text><text x="240" y="98" text-anchor="middle" font-size="10" fill="#999">❌</text>
<rect x="300" y="60" width="80" height="50" fill="#fafafa" stroke="#bbb" stroke-width="1" rx="6"/><text x="340" y="82" class="t" fill="#999">Expert 8</text><text x="340" y="98" text-anchor="middle" font-size="10" fill="#999">❌</text>
</g>
<!-- Arrows from router to selected experts -->
<line x1="250" y1="115" x2="130" y2="130" stroke="#2e7d32" stroke-width="2"/>
<line x1="300" y1="115" x2="330" y2="130" stroke="#2e7d32" stroke-width="2"/>
<!-- Weighted sum -->
<rect x="200" y="260" width="150" height="30" fill="#e3f2fd" stroke="#1565c0" rx="8"/>
<text x="275" y="279" class="t">Weighted Sum → Output</text>
<line x1="130" y1="180" x2="250" y2="260" stroke="#2e7d32" stroke-width="1.5"/>
<line x1="330" y1="180" x2="300" y2="260" stroke="#2e7d32" stroke-width="1.5"/>
</svg>'''

# --- 7. RLHF vs DPO Pipeline ---
svg_rlhf_dpo = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 580 250" style="background:#f8f9fa;border-radius:12px;font-family:system-ui,sans-serif">
<defs><style>.t{font-size:11px;text-anchor:middle;fill:#333}</style></defs>
<text x="290" y="22" text-anchor="middle" font-size="14" font-weight="700">RLHF (Left) vs DPO (Right) Training Pipeline</text>
<!-- RLHF side -->
<rect x="10" y="35" width="270" height="200" fill="#fce4ec" opacity="0.1" stroke="#880e4f" stroke-dasharray="4,3" rx="8"/>
<text x="145" y="52" text-anchor="middle" font-size="12" fill="#880e4f" font-weight="600">RLHF (4 models, complex)</text>
<rect x="30" y="60" width="100" height="25" fill="#e3f2fd" stroke="#1565c0" rx="4"/><text x="80" y="77" class="t">SFT Model</text>
<line x1="80" y1="85" x2="80" y2="95" stroke="#666" stroke-width="1.5"/>
<rect x="30" y="95" width="100" height="25" fill="#fff3e0" stroke="#e65100" rx="4"/><text x="80" y="112" class="t">Reward Model</text>
<text x="160" y="112" class="t" fill="#e65100">+ human labels</text>
<line x1="80" y1="120" x2="80" y2="130" stroke="#666" stroke-width="1.5"/>
<rect x="30" y="130" width="100" height="25" fill="#e8eaf6" stroke="#283593" rx="4"/><text x="80" y="147" class="t">PPO Training</text>
<text x="145" y="147" font-size="10" fill="#666">needs 4 models:</text>
<text x="145" y="160" font-size="9" fill="#999">Actor, Ref, Reward, Critic</text>
<line x1="80" y1="155" x2="80" y2="170" stroke="#666" stroke-width="1.5"/>
<rect x="30" y="170" width="100" height="25" fill="#e8f5e9" stroke="#2e7d32" rx="4"/><text x="80" y="187" class="t">Aligned Model</text>
<text x="145" y="200" font-size="10" fill="#c62828">❌ Unstable</text>
<text x="145" y="212" font-size="10" fill="#c62828">❌ Expensive</text>
<text x="145" y="224" font-size="10" fill="#c62828">❌ 4× GPU memory</text>
<!-- DPO side -->
<rect x="300" y="35" width="270" height="200" fill="#e8f5e9" opacity="0.1" stroke="#2e7d32" stroke-dasharray="4,3" rx="8"/>
<text x="435" y="52" text-anchor="middle" font-size="12" fill="#2e7d32" font-weight="600">DPO (2 models, simple)</text>
<rect x="320" y="60" width="100" height="25" fill="#e3f2fd" stroke="#1565c0" rx="4"/><text x="370" y="77" class="t">SFT Model</text>
<line x1="370" y1="85" x2="370" y2="95" stroke="#666" stroke-width="1.5"/>
<rect x="320" y="95" width="100" height="50" fill="#fff3e0" stroke="#e65100" rx="4"/>
<text x="370" y="115" class="t">DPO Training</text>
<text x="370" y="130" font-size="9" fill="#666">direct preference</text>
<text x="370" y="140" font-size="9" fill="#666">optimization</text>
<text x="445" y="115" font-size="10" fill="#666">needs only:</text>
<text x="445" y="128" font-size="9" fill="#999">Policy + Reference</text>
<text x="445" y="140" font-size="9" fill="#999">+ preference pairs</text>
<line x1="370" y1="145" x2="370" y2="170" stroke="#666" stroke-width="1.5"/>
<rect x="320" y="170" width="100" height="25" fill="#e8f5e9" stroke="#2e7d32" rx="4"/><text x="370" y="187" class="t">Aligned Model</text>
<text x="445" y="200" font-size="10" fill="#2e7d32">✅ Stable</text>
<text x="445" y="212" font-size="10" fill="#2e7d32">✅ 2× GPU memory</text>
<text x="445" y="224" font-size="10" fill="#2e7d32">✅ No Reward Model</text>
</svg>'''

# --- 8. Agent ReAct Loop ---
svg_react = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 350" style="background:#f8f9fa;border-radius:12px;font-family:system-ui,sans-serif">
<defs><marker id="e" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0L10,5L0,10Z" fill="#1565c0"/></marker>
<style>.t{font-size:13px;text-anchor:middle;fill:#333;font-weight:600}.s{font-size:10px;fill:#666;text-anchor:middle}</style></defs>
<text x="250" y="25" text-anchor="middle" font-size="14" font-weight="700">ReAct: Reasoning + Acting Loop</text>
<!-- Thought -->
<rect x="170" y="50" width="160" height="45" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="10"/>
<text x="250" y="70" class="t">💭 Thought</text>
<text x="250" y="85" class="s">"I need to search for..."</text>
<!-- Arrow down -->
<path d="M 250,95 L 250,115" stroke="#1565c0" stroke-width="2" fill="none" marker-end="url(#e)"/>
<!-- Action -->
<rect x="170" y="120" width="160" height="45" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="10"/>
<text x="250" y="140" class="t">🔧 Action</text>
<text x="250" y="155" class="s">search("Beijing weather")</text>
<!-- Arrow down -->
<path d="M 250,165 L 250,185" stroke="#e65100" stroke-width="2" fill="none" marker-end="url(#e)"/>
<!-- Observation -->
<rect x="170" y="190" width="160" height="45" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="10"/>
<text x="250" y="210" class="t">👁️ Observation</text>
<text x="250" y="225" class="s">"Beijing: 晴, 25°C"</text>
<!-- Loop arrow back to thought -->
<path d="M 170,212 Q 80,212 80,72 Q 80,50 170,72" stroke="#9c27b0" stroke-width="2" fill="none" stroke-dasharray="5,3" marker-end="url(#e)"/>
<text x="50" y="145" font-size="10" fill="#9c27b0" transform="rotate(-90 50,145)">Repeat until done</text>
<!-- Final Answer -->
<path d="M 330,72 Q 420,72 420,290 Q 420,310 330,310" stroke="#4caf50" stroke-width="2" fill="none" marker-end="url(#e)"/>
<rect x="170" y="290" width="160" height="40" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="10"/>
<text x="250" y="315" class="t">✅ Final Answer</text>
</svg>'''

# --- 9. Training Pipeline (SFT → RLHF/DPO) ---
svg_training = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 550 200" style="background:#f8f9fa;border-radius:12px;font-family:system-ui,sans-serif">
<defs><marker id="f" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0L8,4L0,8Z" fill="#666"/></marker>
<style>.t{font-size:12px;text-anchor:middle;fill:#333;font-weight:600}.s{font-size:10px;fill:#666;text-anchor:middle}</style></defs>
<text x="275" y="22" text-anchor="middle" font-size="14" font-weight="700">LLM Training Pipeline</text>
<!-- Stage 1: Pre-training -->
<rect x="20" y="40" width="120" height="80" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="10"/>
<text x="80" y="60" class="t">1. Pre-training</text>
<text x="80" y="77" class="s">Trillions of tokens</text>
<text x="80" y="90" class="s">Next token prediction</text>
<text x="80" y="103" class="s">Web + Code + Books</text>
<text x="80" y="116" class="s">→ Base Model</text>
<!-- Arrow -->
<line x1="140" y1="80" x2="165" y2="80" stroke="#666" stroke-width="2" marker-end="url(#f)"/>
<!-- Stage 2: SFT -->
<rect x="170" y="40" width="120" height="80" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="10"/>
<text x="230" y="60" class="t">2. SFT</text>
<text x="230" y="77" class="s">Instruction tuning</text>
<text x="230" y="90" class="s">High-quality Q&amp;A</text>
<text x="230" y="103" class="s">LoRA / Full FT</text>
<text x="230" y="116" class="s">→ Chat Model</text>
<line x1="290" y1="80" x2="315" y2="80" stroke="#666" stroke-width="2" marker-end="url(#f)"/>
<!-- Stage 3: Alignment -->
<rect x="320" y="40" width="120" height="80" fill="#e8eaf6" stroke="#283593" stroke-width="2" rx="10"/>
<text x="380" y="60" class="t">3. Alignment</text>
<text x="380" y="77" class="s">RLHF / DPO</text>
<text x="380" y="90" class="s">Human preferences</text>
<text x="380" y="103" class="s">Safe + Helpful</text>
<text x="380" y="116" class="s">→ Aligned Model</text>
<line x1="440" y1="80" x2="465" y2="80" stroke="#666" stroke-width="2" marker-end="url(#f)"/>
<!-- Result -->
<rect x="470" y="55" width="70" height="50" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="10"/>
<text x="505" y="80" class="t">🚀</text>
<text x="505" y="96" class="s">Production</text>
<!-- Param counts -->
<text x="80" y="140" class="s">~15T tokens</text>
<text x="230" y="140" class="s">~100K examples</text>
<text x="380" y="140" class="s">~50K preferences</text>
<!-- Cost indicators -->
<text x="80" y="160" class="s" fill="#c62828">$$$ (GPU months)</text>
<text x="230" y="160" class="s" fill="#e65100">$$ (days)</text>
<text x="380" y="160" class="s" fill="#2e7d32">$ (hours)</text>
</svg>'''

# --- 10. Quantization Comparison ---
svg_quant = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 200" style="background:#f8f9fa;border-radius:12px;font-family:system-ui,sans-serif">
<defs><style>.t{font-size:11px;text-anchor:middle;fill:#333}</style></defs>
<text x="250" y="22" text-anchor="middle" font-size="14" font-weight="700">Quantization: Reduce Precision, Save Memory</text>
<!-- FP16 -->
<rect x="20" y="40" width="100" height="120" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="8"/>
<text x="70" y="60" class="t" font-weight="600">FP16</text>
<text x="70" y="80" class="t">16 bits/param</text>
<text x="70" y="100" class="t" font-size="20" font-weight="700">26 GB</text>
<text x="70" y="120" class="t" fill="#c62828">13B model</text>
<text x="70" y="140" class="t" fill="#2e7d32">Best quality</text>
<!-- INT8 -->
<rect x="150" y="40" width="100" height="120" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="8"/>
<text x="200" y="60" class="t" font-weight="600">INT8</text>
<text x="200" y="80" class="t">8 bits/param</text>
<text x="200" y="100" class="t" font-size="20" font-weight="700">13 GB</text>
<text x="200" y="120" class="t" fill="#e65100">50% smaller</text>
<text x="200" y="140" class="t" fill="#2e7d32">~0.5% loss</text>
<!-- INT4 -->
<rect x="280" y="40" width="100" height="120" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="8"/>
<text x="330" y="60" class="t" font-weight="600">INT4</text>
<text x="330" y="80" class="t">4 bits/param</text>
<text x="330" y="100" class="t" font-size="20" font-weight="700">7 GB</text>
<text x="330" y="120" class="t" fill="#2e7d32">75% smaller</text>
<text x="330" y="140" class="t" fill="#2e7d32">~1% loss</text>
<!-- Arrows -->
<text x="135" y="105" font-size="18" fill="#666">→</text>
<text x="265" y="105" font-size="18" fill="#666">→</text>
<!-- Annotation -->
<text x="430" y="80" class="t" fill="#1565c0" font-weight="600">Methods:</text>
<text x="430" y="95" class="t" font-size="10" fill="#666">• GPTQ</text>
<text x="430" y="108" class="t" font-size="10" fill="#666">• AWQ</text>
<text x="430" y="121" class="t" font-size="10" fill="#666">• GGUF</text>
<text x="430" y="134" class="t" font-size="10" fill="#666">• NF4/QLoRA</text>
</svg>'''

# --- Save all SVGs ---
images = {
    "svg_transformer.svg": svg_transformer,
    "svg_attention.svg": svg_attention,
    "svg_lora.svg": svg_lora,
    "svg_rag.svg": svg_rag,
    "svg_kvcache.svg": svg_kvcache,
    "svg_moe.svg": svg_moe,
    "svg_rlhf_dpo.svg": svg_rlhf_dpo,
    "svg_react.svg": svg_react,
    "svg_training.svg": svg_training,
    "svg_quantization.svg": svg_quant,
}

for fname, content in images.items():
    save_svg(fname, content)
    print(f"  ✅ {fname}")

print(f"\nTotal: {len(images)} SVG diagrams created")
