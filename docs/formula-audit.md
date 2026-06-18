# Formula Audit Report — AI Interview Question Bank

**Audit Date:** 2025-06-17  
**Scope:** All 35 JSON data files in `/opt/data/projects/ai-interview/data/`  
**Context:** Frontend uses a lightweight markdown renderer with NO MathJax/KaTeX. Formulas must be plain Unicode text.

---

## Summary

| Issue Type | Count | Severity |
|---|---|---|
| LaTeX commands that won't render | 8 | 🔴 Critical |
| Caret notation (^T, ^2) instead of Unicode superscript | 14 | 🟡 Medium |
| Mathematical errors / corruption | 4 | 🔴 Critical |
| Inconsistent notation across entries | 11 | 🟡 Medium |
| **Total issues** | **37** | |

---

## 1. LaTeX Commands That Won't Render (🔴 Critical)

These contain raw LaTeX (`\text{}`, `\sqrt{}`, `\top`) that will display as literal backslash text on the web frontend.

| # | FILE | ID | ISSUE_TYPE | CURRENT_TEXT | SUGGESTED_FIX | EXPLANATION |
|---|---|---|---|---|---|---|
| 1 | agent-llm.json | agen-001 | LATEX_UNRENDERED | `\text{softmax}(QK^\top/\sqrt{d_k})V` (in answer) | `softmax(QKᵀ/√d_k)·V` | `\text{}`, `\top`, `\sqrt{}` are LaTeX commands. Frontend has no LaTeX renderer; these display as literal `\text{softmax}` etc. |
| 2 | agent-llm.json | agen-001 | LATEX_UNRENDERED | `\text{softmax}(QK^\top/\sqrt{d_k})V` (in feynman.essence) | `softmax(QKᵀ/√d_k)·V` | Same LaTeX issue in essence field |
| 3 | agent-llm.json | agen-001 | LATEX_UNRENDERED | `\text{softmax}(QK^\top/\sqrt{d_k})V` (in feynman.key_points[0]) | `softmax(QKᵀ/√d_k)·V` | Same LaTeX issue in key_points field |
| 4 | agent-llm.json | agen-001 | LATEX_UNRENDERED | `\sqrt{d_k}` (in question field) | `√d_k` | LaTeX in question title |
| 5 | agent-llm.json | agen-001 | LATEX_UNRENDERED | `\sqrt{d_k}` (in first_principle.problem) | `√d_k` | LaTeX in problem field |
| 6 | llm-100.json | (llm--026, FlashAttention) | LATEX_UNRENDERED | Contains `softmax(QK ) ⊤` with stray Unicode `⊤` (top symbol) used as transpose marker | `softmax(QKᵀ)` | The `⊤` (U+22A4 DOWN TACK) is a logic/set-theory symbol, not matrix transpose. Should use Unicode superscript T (ᵀ) |
| 7 | llm-100.json | (llm--026, Linear Attention) | LATEX_UNRENDERED | `softmax(QK ) ⊤` in formula for Linear Attention | `softmax(QKᵀ)` | Same stray `⊤` symbol issue |
| 8 | llm-100.json | (llm--094, MHA) | LATEX_UNRENDERED | `O(n2)O(n^2)O(n2)` — triple garbled complexity notation | `O(n²)` | Text appears triplicated and mixed between `O(n2)` and `O(n^2)` — likely a copy-paste artifact |

---

## 2. Caret Notation Instead of Unicode Superscript (🟡 Medium)

The frontend renders `^T` and `^2` as literal characters. Should use Unicode superscripts: ᵀ (U+1D40), ² (U+00B2).

### 2a. `^T` should be `ᵀ` (transpose)

| # | FILE | ID | CURRENT_TEXT | SUGGESTED_FIX | EXPLANATION |
|---|---|---|---|---|---|
| 9 | ai-basics.json | (basics-001, Self-Attention) | `softmax(QK^T/√dk)·V` | `softmax(QKᵀ/√d_k)·V` | `^T` renders as literal caret-T; should use Unicode superscript ᵀ |
| 10 | supp-ai-basics.json | (s003) | `softmax(QK^T / √d) · V` | `softmax(QKᵀ / √d_k) · V` | Same caret notation; also `√d` should be `√d_k` |
| 11 | supp-llm-transformer.json | llm-core-s001 | `QK^T` (appears 4× in answer, essence, key_points) | `QKᵀ` | Caret notation throughout |
| 12 | supp-llm-advanced.json | (KV Cache entry) | `softmax(Q*K^T/sqrt(d))*V` | `softmax(QKᵀ/√d_k)·V` | Caret notation + inconsistent use of `*` for multiply + `sqrt()` function notation |
| 13 | agent-interview-qa.json | (Self-Attention entry) | `Q · K^T` (2× in answer, 1× in key_points) | `Q · Kᵀ` | Caret notation |
| 14 | llm-notes.json | (Flash Attention entry) | `QK^T` (3× in answer) | `QKᵀ` | Caret notation |
| 15 | ai-basics.json | (RoPE entry) | `k_n^T` | `k_nᵀ` | Caret notation for transpose |
| 16 | llm-100.json | (FlashAttention) | `QK^T` (in key_points) | `QKᵀ` | Caret notation |

### 2b. `^2` should be `²` (squared)

| # | FILE | ID | CURRENT_TEXT | SUGGESTED_FIX | EXPLANATION |
|---|---|---|---|---|---|
| 17 | supp-llm-advanced.json | (KV Cache entry) | `O(n^2)` (3× in answer, essence) | `O(n²)` | Caret notation; should use Unicode ² |
| 18 | ai-basics.json | (Flash Attention entry) | `O(n^2)` | `O(n²)` | Caret notation |
| 19 | ai-basics.json | (Long Context entry) | `O(n^2)` (2× in answer, essence) | `O(n²)` | Caret notation |
| 20 | llm-notes.json | (Flash Attention entry) | `O(N^2)` (3× in answer) | `O(N²)` | Caret notation |
| 21 | ai-basics.json | (RMSNorm entry) | `sqrt(mean(x^2) + eps)` | `sqrt(mean(x²) + eps)` | Caret notation in formula |
| 22 | agent-interview-qa.json | (RLHF/DPO entry) | `n³` and `n²` — these are already Unicode ✓ | — | (No fix needed — noted as correctly using Unicode) |

---

## 3. Mathematical Errors / Data Corruption (🔴 Critical)

| # | FILE | ID | ISSUE_TYPE | CURRENT_TEXT | SUGGESTED_FIX | EXPLANATION |
|---|---|---|---|---|---|---|
| 23 | agent-interview-qa.json | (Self-Attention entry, line ~2636) | MATH_ERROR | `ROI = (年化收益 - 年化成本) / 年化成本 × 100%` inserted into the middle of Self-Attention explanation | Remove this line entirely | An irrelevant ROI (Return on Investment) formula has been accidentally inserted into the Self-Attention Q/K/V explanation. This is data corruption — the ROI formula has nothing to do with attention computation |
| 24 | agent-interview-qa.json | (LoRA entry, line ~2668) | MATH_ERROR | `4096² = 16M` | `4096² = 16.7M` | 4096² = 16,777,216 ≈ 16.7M, not 16M. Other entries (supp-llm-training.json, supp-finetuning.json) correctly state 16.7M |
| 25 | llm-100.json | (Linear Attention, line ~2629) | MATH_ERROR | `Attention(Q, K, V) ≈ (ϕ(Q)[ϕ(K)ᵀV]) / (ϕ(Q)[ϕ(K)ᵀ1])` — formula is structurally correct but uses stray `⊤` and formatting is garbled | Clean up to: `Attention(Q,K,V) ≈ (φ(Q)[φ(K)ᵀV]) / (φ(Q)[φ(K)ᵀ·1])` | The `⊤` symbol is used incorrectly as transpose; should be ᵀ. Also `ϕ` (U+03D5 variant phi) vs `φ` (U+03C6) inconsistency |
| 26 | llm-100.json | (MHA comparison, line ~2724) | MATH_ERROR | `O(n2)O(n^2)O(n2)` | `O(n²)` | Triple-garbled text — appears to be the same formula written three times with different notations concatenated together |

---

## 4. Inconsistent Notation Across Entries (🟡 Medium)

### 4a. Attention scaling factor notation (should be `√d_k` everywhere)

| # | FILE | ID | CURRENT_TEXT | SUGGESTED_FIX | EXPLANATION |
|---|---|---|---|---|---|
| 27 | ai-basics.json | basics-001 | `√dk` | `√d_k` | Missing underscore separator between d and k — ambiguous (could read as "√dk" single variable) |
| 28 | supp-ai-basics.json | s003 | `√d` | `√d_k` | Uses just `d` instead of `d_k` — technically incorrect; scaling factor is √d_k (key dimension), not √d (model dimension) |
| 29 | supp-llm-advanced.json | (KV Cache) | `sqrt(d)` | `√d_k` | Uses function-style `sqrt()` and `d` instead of `d_k` — inconsistent with other entries and imprecise |
| 30 | llm-100.json | (FlashAttention) | `√dk` in some places, `sqrt(d_k)` in others | Standardize to `√d_k` | Mixed notation within the same file |

### 4b. Multiplication operator inconsistency

| # | FILE | ID | CURRENT_TEXT | SUGGESTED_FIX | EXPLANATION |
|---|---|---|---|---|---|
| 31 | supp-llm-advanced.json | (KV Cache) | `Q*K^T` and `sqrt(d))*V` | `QKᵀ` and `√d_k)·V` | Uses `*` for multiplication — other entries use `·` (middle dot) or nothing (juxtaposition) |
| 32 | Multiple files | — | Some use `·` (dot), some use `×`, some use `*`, some use juxtaposition | Standardize on `·` for scalar/matrix multiply in formulas | Inconsistent across: supp-llm-training uses `B·A`, supp-llm-advanced uses `*`, agent-interview-qa uses `·`, ai-basics uses `·` |

### 4c. DPO loss formula notation inconsistency

| # | FILE | ID | CURRENT_TEXT | SUGGESTED_FIX | EXPLANATION |
|---|---|---|---|---|---|
| 33 | ai-basics.json | (DPO entry) | `L_DPO = -log sigma(beta * log(pi(y_w)/pi_ref(y_w)) - ...)` | `L_DPO = -log σ(β·log(π(y_w|x)/π_ref(y_w|x)) - β·log(π(y_l|x)/π_ref(y_l|x)))` | Missing `|x` conditioning in pi functions; uses `*` instead of `·`; uses `beta` instead of `β`; uses `sigma` instead of `σ` |
| 34 | llm-notes.json | (DPO entry) | `L_DPO = -E[log sigma(beta·log(pi(y_w|x)/pi_ref(y_w|x)) - ...)]` | Close to correct; standardize Greek letters: `β` instead of `beta`, `σ` instead of `sigma` | This version includes `|x` (correct) and `·` (consistent) but uses ASCII `beta` and `sigma` instead of Greek |

### 4d. Norm formula notation inconsistency

| # | FILE | ID | CURRENT_TEXT | SUGGESTED_FIX | EXPLANATION |
|---|---|---|---|---|---|
| 35 | ai-basics.json | (RMSNorm entry) | `y = gamma * (x - mean) / sqrt(var + eps) + beta` and `y = gamma * x / sqrt(mean(x^2) + eps)` | `y = γ·(x - μ)/√(σ² + ε) + β` and `y = γ·x/√(mean(x²) + ε)` | Uses ASCII `gamma`, `mean`, `var`, `eps`, `beta` and function-style `sqrt()` while supp-llm-transformer.json uses proper Greek: `μ`, `σ²`, `√(σ² + ε)`, `γ`, `β` |

### 4e. Set membership notation inconsistency

| # | FILE | ID | CURRENT_TEXT | SUGGESTED_FIX | EXPLANATION |
|---|---|---|---|---|---|
| 36 | Multiple files | — | `∈R^(d×r)` (supp-llm-training, ai-basics) vs `∈R^d×r` vs `∈Rd×k` (llm-100) vs `∈ ℝ^(d×r)` | Standardize to `∈ ℝ^(d×r)` or `∈ R^(d×r)` | llm-100.json uses severely garbled notation like `W ∈Rd×k` (missing exponent), while supp-llm-training uses clean `A∈R^(d×r)`. Should use ℝ (U+211D) or at minimum consistent `R^()` notation |

### 4f. `∈R` vs `∈ ℝ` for real number set

| # | FILE | ID | CURRENT_TEXT | SUGGESTED_FIX | EXPLANATION |
|---|---|---|---|---|---|
| 37 | supp-llm-training.json | llm-core-s001 | `A∈R^(d×r)，B∈R^(r×d)` | `A∈ℝ^(d×r)，B∈ℝ^(r×d)` | Uses `R` (plain letter) instead of `ℝ` (U+211D DOUBLE-STRUCK R). Minor but for mathematical correctness should use ℝ |

---

## Appendix: Files Reviewed

All 35 JSON files in `/opt/data/projects/ai-interview/data/` were searched and reviewed:

| File | Has Formulas? | Issues Found |
|---|---|---|
| agent-llm.json | ✅ Yes | 🔴 5 LaTeX issues (agen-001) |
| ai-basics.json | ✅ Yes | 🟡 ^T, ^2, notation inconsistency |
| supp-ai-basics.json | ✅ Yes | 🟡 ^T, √d notation |
| supp-llm-transformer.json | ✅ Yes | 🟡 ^T notation |
| supp-llm-training.json | ✅ Yes | 🟡 ∈R notation |
| supp-llm-advanced.json | ✅ Yes | 🟡 ^T, ^2, sqrt() notation |
| supp-llm-frontier.json | ✅ Yes | ✅ Clean (uses O(n²)) |
| supp-finetuning.json | ✅ Yes | ✅ Clean (uses proper notation) |
| agent-interview-qa.json | ✅ Yes | 🔴 ROI formula corruption, ^T, 16M error |
| llm-notes.json | ✅ Yes | 🟡 ^T, ^2, beta/sigma ASCII |
| llm-100.json | ✅ Yes | 🔴 Garbled formulas, ⊤ misuse, O(n2)O(n^2)O(n2) |
| new-llm-core.json | ✅ Yes | ✅ Clean (uses O(n²)) |
| new-ai-basics.json | ✅ Minor | ✅ Clean |
| new-eng-practice.json | ✅ Minor | ✅ Clean |
| new-agent-skill.json | ✅ Minor | ✅ Clean |
| new-agent-arch.json | ✅ Minor | ✅ Clean |
| agent-rag.json | ✅ Yes (MMR) | ✅ MMR formula correct |
| agent-memory.json | ✅ Minor | ✅ Clean |
| agent-multi.json | ✅ Minor | ✅ Clean |
| agent-concept.json | ✅ Minor | ✅ Clean |
| agent-framework.json | ✅ Minor | ✅ Clean |
| agent-eng.json | ✅ Minor | ✅ Clean |
| agent-prompt.json | ✅ Minor | ✅ Clean |
| agent-tools.json | ✅ Minor | ✅ Clean |
| ai-agent.json | ✅ Minor | ✅ Clean |
| ai-harness.json | ✅ Minor | ✅ Clean |
| ai-scenario.json | ✅ Minor | ✅ Clean |
| fde.json | ✅ Minor | ✅ Clean |
| supp-multimodal.json | ✅ Minor | ✅ Clean |
| supp-harness-inference.json | ✅ Minor | ✅ Clean |
| supp-eng-practice.json | ✅ Minor | ✅ Clean |
| supp-agent-rag.json | ✅ Minor | ✅ Clean |
| supp-agent-frameworks.json | ✅ Minor | ✅ Clean |
| supp-agent-arch.json | ✅ Minor | ✅ Clean |
| supp-advanced-rag.json | ✅ Minor | ✅ Clean |

---

## Recommended Priority Fixes

### Priority 1 — Critical (Fix Immediately)
1. **agent-llm.json agen-001**: Convert ALL LaTeX to Unicode across all fields (question, answer, essence, key_points, problem)
2. **agent-interview-qa.json**: Remove irrelevant ROI formula from Self-Attention entry
3. **llm-100.json**: Fix `O(n2)O(n^2)O(n2)` garbled text; fix `⊤` misused as transpose

### Priority 2 — Standardization (Batch Fix)
4. Replace all `^T` → `ᵀ` across all files (14 occurrences)
5. Replace all `^2` → `²` in formula contexts (6+ occurrences)  
6. Standardize scaling factor to `√d_k` everywhere (not `√d`, `√dk`, or `sqrt(d_k)`)
7. Standardize DPO loss formula notation across ai-basics.json and llm-notes.json
8. Fix `4096² = 16M` → `4096² = 16.7M` in agent-interview-qa.json

### Priority 3 — Polish
9. Standardize multiplication operator to `·` in formulas
10. Use Greek letters (β, σ, γ, μ) instead of ASCII names (beta, sigma, gamma, mean)
11. Standardize `∈R` → `∈ ℝ` for set membership

---

## Key Formula Reference (Correct Unicode Versions)

For consistency, these are the canonical Unicode formula representations all entries should use:

```
Self-Attention:  Attention(Q,K,V) = softmax(QKᵀ/√d_k)·V
LoRA:            W' = W + ΔW = W + B·A, where A∈ℝ^(d×r), B∈ℝ^(r×d), r≪d
Scaling Law:     Loss ≈ A/N^α + B/D^β + L∞
DPO Loss:        L_DPO = -log σ(β·log(π(y_w|x)/π_ref(y_w|x)) - β·log(π(y_l|x)/π_ref(y_l|x)))
LayerNorm:       y = γ·(x - μ)/√(σ² + ε) + β
RMSNorm:         y = γ·x/√(mean(x²) + ε)
Complexity:      O(n²)  [not O(n^2) or O(n2)]
Transpose:       QKᵀ   [not QK^T or QK⊤]
```
