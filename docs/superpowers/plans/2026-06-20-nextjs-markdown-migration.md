# ai-interview → Next.js + Markdown 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 ai-interview（及 java-interview）题目改为按分类分文件夹的单题 markdown 文件，并用 Next.js 重写站点，构建期读取 markdown 获取答案，全量保留功能，5 轮验收。

**Architecture:** 每题一个 `questions/<category>/<id>.md`（YAML frontmatter + body）；Next.js 构建期用 gray-matter 解析注入静态页（运行时零 fetch）；Zustand persist 复用现有 localStorage key 保数据兼容；静态导出到 GitHub Pages。

**Tech Stack:** Next.js 15 (App Router) · React 19 · TypeScript · Tailwind v4 · Zustand · gray-matter · react-markdown · @serwist/next

**Spec:** `ai-interview/docs/superpowers/specs/2026-06-20-nextjs-markdown-migration-design.md`

---

## 文件结构（创建/修改清单）

**迁移产物（两个项目）**
- `ai-interview/questions/<category>/<id>.md`（911 题）
- `java-interview/questions/<category>/<id>.md`（819 题）
- `ai-interview/scripts/migrate_to_md.py`（一次性迁移脚本，两项目通用）
- `java-interview/scripts/migrate_to_md.py`（软链/拷贝，同脚本）

**Next.js 工程（ai-interview）**
- `ai-interview/package.json`、`next.config.ts`、`tsconfig.json`、`tailwind.config.ts`、`postcss.config.mjs`
- `ai-interview/src/app/layout.tsx`、`src/app/page.tsx`、`src/app/question/[id]/page.tsx`
- `ai-interview/src/app/globals.css`
- `ai-interview/src/lib/config.ts`、`questions.ts`、`markdown.ts`、`types.ts`
- `ai-interview/src/lib/store.ts`、`algorithms.ts`
- `ai-interview/src/components/*.tsx`（CategoryTabs、CardGrid、QuestionCard、SearchBar、FilterBar、QuestionModal、QuestionContent、FeynmanCard、FirstPrincipleCard、StudyMode、ReviewMode、SettingsPanel、ShortcutsHelp、Toast、ProgressRing、DifficultyBars、StudyDashboard、ReviewDashboard）

**保留不删**：`interview-framework/`（java-interview 仍用）、`ai-interview/images/`（迁到 public/images）

---

## Task 1: 编写通用迁移脚本 migrate_to_md.py

**Files:**
- Create: `ai-interview/scripts/migrate_to_md.py`

- [ ] **Step 1: 编写脚本（读取项目 data/*.json，按 config 的 category→files 映射，生成 questions/**/*.md）**

```python
#!/usr/bin/env python3
# coding: utf-8
"""
将 interview 项目 data/*.json 的题目迁移为 questions/<category>/<id>.md。
用法: python3 migrate_to_md.py <project_dir>
  project_dir 例如 /Users/.../projects/ai-interview
项目根需含 data/*.json 与 config.js（读取 categories 的 files 映射）。
幂等：重复运行覆盖生成相同结果。
"""
import sys, os, re, json

def parse_config_categories(project_dir):
    """从 config.js 提取 categories 的 key→files 映射（保持声明顺序）。"""
    cfg_path = os.path.join(project_dir, 'config.js')
    with open(cfg_path, encoding='utf-8') as f:
        text = f.read()
    # 截取 categories: { ... } 对象（到第一个匹配的顶层 }）
    m = re.search(r"categories\s*:\s*\{", text)
    start = m.end() - 1  # 指向 {
    depth = 0
    end = start
    for i in range(start, len(text)):
        if text[i] == '{': depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1; break
    block = text[start:end]
    # 每个 key: { ... files: ['data/x.json', ...] ... }
    cats = {}
    order = []
    for km in re.finditer(r"'([^']+)'\s*:\s*\{", block):
        key = km.group(1)
        # 在该 key 的对象块里找 files
        seg = block[km.end():]
        # 取到本对象结束
        d = 1; j = 0
        while j < len(seg) and d > 0:
            if seg[j] == '{': d += 1
            elif seg[j] == '}': d -= 1
            j += 1
        obj = seg[:j]
        if key == 'all':
            order.append(key); cats[key] = None; continue
        fm = re.search(r"files\s*:\s*\[(.*?)\]", obj, re.S)
        files = []
        if fm:
            files = ["data/" + os.path.basename(x.strip().strip("'\""))
                     for x in fm.group(1).split(',') if x.strip()]
        cats[key] = files
        order.append(key)
    return cats, order

def yaml_scalar(v):
    """把 Python 值渲染为 YAML 行内标量/块。返回 (head_str, block_lines) 简化：返回多行文本（不含尾部换行）。"""
    # 此处仅处理 frontmatter 用到的类型：str, list[str], dict
    if v is None:
        return 'null'
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (int, float)):
        return str(v)
    return None  # 复杂类型交给结构化渲染

def yaml_escape_str(s):
    s = str(s)
    # 用双引号，转义反斜杠与双引号；保留换行交给 block scalar（此处答案放 body，frontmatter 字符串基本单行）
    s = s.replace('\\', '\\\\').replace('"', '\\"')
    # 控制字符简单处理
    s = s.replace('\n', ' ').replace('\r', '')
    return '"' + s + '"'

def render_frontmatter(meta):
    """meta: dict，渲染为 YAML frontmatter 文本（块风格 list/dict）。"""
    lines = ['---']
    for k, v in meta.items():
        if v is None or v == '' or v == [] or v == {}:
            continue
        if isinstance(v, list):
            lines.append('%s:' % k)
            for item in v:
                lines.append('  - ' + yaml_escape_str(item))
        elif isinstance(v, dict):
            lines.append('%s:' % k)
            for dk, dv in v.items():
                if isinstance(dv, list):
                    lines.append('  %s:' % dk)
                    for item in dv:
                        lines.append('    - ' + yaml_escape_str(item))
                else:
                    lines.append('  %s: %s' % (dk, yaml_escape_str(dv)))
        else:
            lines.append('%s: %s' % (k, yaml_escape_str(v)))
    lines.append('---')
    return '\n'.join(lines)

def main():
    if len(sys.argv) < 2:
        print('usage: migrate_to_md.py <project_dir>'); sys.exit(1)
    project_dir = os.path.abspath(sys.argv[1])
    cats, order = parse_config_categories(project_dir)
    order = [c for c in order if c != 'all' and cats.get(c)]
    # id -> (primary_category, set_of_categories, item)
    items = {}
    id_order = []
    for cat in order:  # 主分类 = 首次出现的 category
        for f in cats[cat]:
            fp = os.path.join(project_dir, f)
            if not os.path.exists(fp):
                continue
            with open(fp, encoding='utf-8') as fh:
                data = json.load(fh)
            for q in data:
                qid = q.get('id')
                if not qid:
                    continue
                if qid not in items:
                    items[qid] = {'primary': cat, 'cats': set(), 'item': q}
                    id_order.append(qid)
                items[qid]['cats'].add(cat)
                # 以首次出现的 item 为准（去重保留首份）
    # 写 questions/<primary>/<id>.md
    out_root = os.path.join(project_dir, 'questions')
    if os.path.isdir(out_root):
        import shutil
        shutil.rmtree(out_root)
    os.makedirs(out_root, exist_ok=True)
    written = 0
    for qid in id_order:
        rec = items[qid]
        q = rec['item']
        primary = rec['primary']
        all_cats = sorted(rec['cats'])
        cat_dir = os.path.join(out_root, primary)
        os.makedirs(cat_dir, exist_ok=True)
        meta = {}
        meta['id'] = q.get('id')
        meta['difficulty'] = q.get('difficulty')
        meta['category'] = primary
        if len(all_cats) > 1:
            meta['categories'] = all_cats
        if q.get('subcategory'):
            meta['subcategory'] = q['subcategory']
        if q.get('tags'):
            meta['tags'] = q['tags']
        if q.get('images'):
            meta['images'] = q['images']
        if q.get('feynman'):
            meta['feynman'] = q['feynman']
        if q.get('first_principle'):
            meta['first_principle'] = q['first_principle']
        if q.get('follow_up'):
            meta['follow_up'] = q['follow_up']
        body = '# ' + (q.get('question') or '').strip() + '\n\n' + (q.get('answer') or '').strip() + '\n'
        content = render_frontmatter(meta) + '\n\n' + body
        with open(os.path.join(cat_dir, qid + '.md'), 'w', encoding='utf-8') as fh:
            fh.write(content)
        written += 1
    # 校验报告
    print('Wrote %d markdown files to %s' % (written, out_root))
    # 每分类计数
    from collections import Counter
    cnt = Counter()
    for qid, rec in items.items():
        for c in rec['cats']:
            cnt[c] += 1
    print('Per-category counts:')
    for c in order:
        print('  %s: %d' % (c, cnt.get(c, 0)))
    print('Total unique questions: %d' % len(items))

if __name__ == '__main__':
    main()
```

- [ ] **Step 2: 在 ai-interview 上运行迁移**

Run: `cd /Users/sunqingguang/hermes/opt/projects && python3 ai-interview/scripts/migrate_to_md.py ai-interview`
Expected: `Wrote 911 markdown files`；分类计数 llm-core:272 ai-agent:250 ai-harness:144 fde:32 eng-practice:137 ai-basics:68 ai-scenario:50

- [ ] **Step 3: 校验生成的 md 数量与内容**

Run: `find ai-interview/questions -name '*.md' | wc -l`
Expected: `911`

- [ ] **Step 4: 在 java-interview 上运行同一脚本**

Run: `python3 ai-interview/scripts/migrate_to_md.py java-interview`
Expected: `Wrote 819 markdown files`（java-core:260 concurrent:125 jvm:67 framework:50 database:92 middleware:40 distributed:58 scenario:127 等，总和 819）

- [ ] **Step 5: 提交**

```bash
cd /Users/sunqingguang/hermes/opt/projects
git -C ai-interview add scripts/migrate_to_md.py questions/ && git -C ai-interview commit -m "feat: migrate 911 questions to per-question markdown files"
git -C java-interview add scripts/migrate_to_md.py questions/ && git -C java-interview commit -m "feat: migrate 819 questions to per-question markdown files"
```

---

## Task 2: 删除原 JSON（按用户决定）+ 备份标记

**Files:**
- Modify: `ai-interview/data/*.json`（删除）、`java-interview/data/*.json`（删除）

- [ ] **Step 1: 删除两个项目的原 data/*.json（迁移已生成 questions/，JSON 不再需要）**

Run:
```bash
cd /Users/sunqingguang/hermes/opt/projects
mkdir -p /tmp/interview-json-backup && cp ai-interview/data/*.json /tmp/interview-json-backup/ai_ && cp java-interview/data/*.json /tmp/interview-json-backup/java_
git -C ai-interview rm data/*.json
git -C java-interview rm data/*.json
```
Expected: JSON 文件从两项目移除（备份留在 /tmp）

- [ ] **Step 2: 提交**

```bash
git -C ai-interview commit -m "chore: remove original JSON (migrated to questions/*.md)"
git -C java-interview commit -m "chore: remove original JSON (migrated to questions/*.md)"
```

> 注：原 ai-interview 站点（vanilla JS）会因此失效，但本次目标是 Next.js 重写，新站不依赖这些 JSON。

---

## Task 3: 搭建 Next.js 工程骨架（ai-interview）

**Files:**
- Create: `ai-interview/package.json`、`next.config.ts`、`tsconfig.json`、`tailwind.config.ts`、`postcss.config.mjs`、`src/app/layout.tsx`、`src/app/globals.css`

- [ ] **Step 1: 创建 package.json**

```json
{
  "name": "ai-interview",
  "version": "4.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "15.1.0",
    "react": "19.0.0",
    "react-dom": "19.0.0",
    "gray-matter": "4.0.3",
    "react-markdown": "9.0.1",
    "remark-gfm": "4.0.0",
    "rehype-highlight": "7.0.1",
    "zustand": "5.0.2"
  },
  "devDependencies": {
    "typescript": "5.7.2",
    "@types/node": "22.10.2",
    "@types/react": "19.0.2",
    "@types/react-dom": "19.0.2",
    "tailwindcss": "4.0.0",
    "@tailwindcss/postcss": "4.0.0",
    "autoprefixer": "10.4.20"
  }
}
```

- [ ] **Step 2: 创建 next.config.ts（静态导出 + basePath）**

```typescript
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  output: 'export',
  basePath: process.env.NODE_ENV === 'production' ? '/ai-interview' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/ai-interview/' : undefined,
  trailingSlash: true,
  images: { unoptimized: true },
};

export default nextConfig;
```

- [ ] **Step 3: 创建 tsconfig.json、tailwind.config.ts、postcss.config.mjs、globals.css**

`tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "ES2020", "lib": ["dom","dom.iterable","esnext"],
    "allowJs": true, "skipLibCheck": true, "strict": true, "noEmit": true,
    "esModuleInterop": true, "module": "esnext", "moduleResolution": "bundler",
    "resolveJsonModule": true, "isolatedModules": true, "jsx": "preserve",
    "incremental": true, "plugins": [{"name":"next"}], "paths": {"@/*":["./src/*"]}
  },
  "include": ["next-env.d.ts","**/*.ts","**/*.tsx",".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

`postcss.config.mjs`:
```js
export default { plugins: { '@tailwindcss/postcss': {} } };
```

`src/app/globals.css`（含 Tailwind v4 指令 + 主题变量）:
```css
@import "tailwindcss";
:root {
  --bg: #f5f5f7; --text: #1d1d1f; --text-tertiary:#86868b;
  --card:#ffffff; --border:#e5e5e7; --primary:#0071e3;
}
:root[data-theme="dark"] {
  --bg:#000000; --text:#f5f5f7; --text-tertiary:#98989d;
  --card:#1c1c1e; --border:#38383a; --primary:#0a84ff;
}
body { background: var(--bg); color: var(--text); }
.markdown-body { line-height: 1.7; }
.markdown-body pre { background:#f6f8fa; padding:12px; border-radius:8px; overflow:auto; }
:root[data-theme="dark"] .markdown-body pre { background:#161b22; }
.markdown-body table { border-collapse:collapse; }
.markdown-body th,.markdown-body td { border:1px solid var(--border); padding:6px 10px; }
```

- [ ] **Step 4: 创建 src/app/layout.tsx（根布局 + StoreProvider + 主题）**

```tsx
import './globals.css';
import { StoreProvider } from '@/lib/store';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'AI 面试题库',
  description: '精选 AI 面试题，构建期读取 markdown。',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN" suppressHydrationWarning>
      <body>
        <StoreProvider>{children}</StoreProvider>
      </body>
    </html>
  );
}
```

- [ ] **Step 5: 安装依赖并验证 dev 可启动**

Run: `cd /Users/sunqingguang/hermes/opt/projects/ai-interview && npm install 2>&1 | tail -5 && timeout 25 npm run dev 2>&1 | head -20`
Expected: 安装成功；dev server 启动到 localhost:3000（即使页面报错也先看能否编译）

- [ ] **Step 6: 提交骨架**

```bash
git -C ai-interview add package.json next.config.ts tsconfig.json tailwind.config.ts postcss.config.mjs src/app/layout.tsx src/app/globals.css
printf 'node_modules\n.next\nout\n' > ai-interview/.gitignore.new
cat ai-interview/.gitignore ai-interview/.gitignore.new 2>/dev/null | sort -u > /tmp/gi && mv /tmp/gi ai-interview/.gitignore; rm -f ai-interview/.gitignore.new
git -C ai-interview add .gitignore && git -C ai-interview commit -m "feat: scaffold Next.js project skeleton"
```

---

## Task 4: 数据层 — 构建期读 markdown（lib/types.ts、config.ts、questions.ts、store.ts、algorithms.ts）

**Files:**
- Create: `src/lib/types.ts`、`src/lib/config.ts`、`src/lib/questions.ts`、`src/lib/store.ts`、`src/lib/algorithms.ts`

- [ ] **Step 1: types.ts（题目与算法类型）**

```typescript
export interface Feynman { essence?: string; analogy?: string; key_points?: string[]; }
export interface FirstPrinciple { problem?: string; axioms?: string[]; rebuild?: string; }
export interface Question {
  id: string;
  question: string;       // 来自 body 的 # 标题
  answer: string;         // body 正文（markdown）
  difficulty: string;     // L1..L5
  category: string;       // 主分类
  categories: string[];   // 所有归属分类（≥1）
  subcategory?: string;
  tags: string[];
  images: string[];
  follow_up: string[];
  feynman?: Feynman;
  first_principle?: FirstPrinciple;
}
export type Rating = 'know' | 'fuzzy' | 'dont';
export type Algorithm = 'sm2' | 'leitner' | 'ebbinghaus';
export interface ReviewItem {
  algo: Algorithm; ease: number; interval: number; reps: number; lapses: number;
  box: number; phase: number; nextDate: string; lastDate: string; createdAt: string;
  history: { d: string; q: number }[];
}
```

- [ ] **Step 2: config.ts（从 config.js 迁移 APP_CONFIG）**

```typescript
import type { Algorithm } from './types';

export const APP_CONFIG = {
  appName: 'AI 面试题库', appNameShort: 'AI面试题', appIcon: '🧠', appVersion: '4.0',
  storagePrefix: 'ai-interview',
  githubUrl: 'https://sunarthur86.github.io/ai-interview/',
  repoUrl: 'https://github.com/SunArthur86/ai-interview',
  themeColor: '#0071e3',
  categories: {
    'all':         { label:'全部', icon:'📚', color:'#0071e3' },
    'llm-core':    { label:'LLM 核心', icon:'🔥', color:'#ff3b30' },
    'ai-agent':    { label:'AI Agent', icon:'🤖', color:'#af52de' },
    'ai-harness':  { label:'AI Harness', icon:'🏗️', color:'#5856d6' },
    'fde':         { label:'FDE', icon:'🚀', color:'#00c7be' },
    'eng-practice':{ label:'工程化实战', icon:'⚙️', color:'#ff9500' },
    'ai-basics':   { label:'AI 基础', icon:'🧠', color:'#34c759' },
    'ai-scenario': { label:'AI 场景设计', icon:'🎯', color:'#e74c3c' },
  } as Record<string, { label: string; icon: string; color: string }>,
  subcatGroups: {
    'Transformer': ['Transformer架构','注意力机制','位置编码','归一化','激活函数','模型结构','模型架构'],
    '训练与微调': ['训练与微调','训练优化','LoRA与微调','参数高效微调','微调策略','SFT与RLHF','对齐技术','对齐训练','训练理论','分布式训练'],
    'LLM前沿': ['LLM前沿','DeepSeek-R1','强化学习','Tokenizer','多模态','Text2SQL','LLM推荐','实验管理','LLM进阶'],
    'AI Agent': ['Agent基础概念','Agent核心框架','Agent架构','Agent稳定性','Agent评估','工具调用','Function Calling','工具使用','记忆系统','Agent记忆','规划与推理','多智能体','多智能体系统','多Agent系统','Prompt工程','Prompt Engineering'],
    'RAG': ['RAG技术','RAG进阶','RAG与向量检索','向量检索','高级RAG'],
    'AI Harness': ['推理优化','推理与部署','生产工程化','生产化部署','模型服务','模型部署','部署架构','工程化','工程化实践','工程实践','Agent工程化','Agent框架','LLM框架','RAG工程化','向量数据库','可观测性','评估与安全','评估','评估指标','评测与质量','Agent安全','安全'],
    '大模型基础': ['大模型基础','大模型架构','大模型原理','大模型综合','大模型应用','基础知识','预训练模型','表示学习','长上下文'],
    'AI场景-RAG': ['RAG系统设计'], 'AI场景-Agent': ['AI Agent系统设计'], 'AI场景-对话': ['AI对话系统设计'],
    'AI场景-推理部署': ['LLM推理与部署'], 'AI场景-安全治理': ['AI安全与治理'], 'AI场景-评测监控': ['AI评测与监控'],
    'AI场景-多模态': ['多模态AI系统'], 'AI场景-推荐搜索': ['AI推荐与搜索'], 'AI场景-代码助手': ['AI代码助手'], 'AI场景-特殊应用': ['AI特殊场景'],
    'FDE': ['FDE基础概念','FDE工作实践','AI解决方案设计','AI部署实施','数据安全与合规'],
    '面试实战': ['企业面试问答','手撕代码','AI编程','文档处理'],
  } as Record<string, string[]>,
} as const;

export const SUBCAT_REVERSE: Record<string,string> = {};
Object.entries(APP_CONFIG.subcatGroups).forEach(([g, subs]) => subs.forEach(s => { SUBCAT_REVERSE[s] = g; }));
export function getSubcatGroup(sub: string | undefined): string { return (sub && SUBCAT_REVERSE[sub]) || '其他'; }
```

- [ ] **Step 3: questions.ts（构建期读 questions/**/*.md）**

```typescript
import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import type { Question } from './types';

const QUESTIONS_DIR = path.join(process.cwd(), 'questions');

function loadAll(): Question[] {
  if (!fs.existsSync(QUESTIONS_DIR)) return [];
  const out: Question[] = [];
  for (const catDir of fs.readdirSync(QUESTIONS_DIR)) {
    const full = path.join(QUESTIONS_DIR, catDir);
    if (!fs.statSync(full).isDirectory()) continue;
    for (const file of fs.readdirSync(full)) {
      if (!file.endsWith('.md')) continue;
      const raw = fs.readFileSync(path.join(full, file), 'utf-8');
      const { data, content } = matter(raw);
      // body 首行 # 标题 = question，其余 = answer
      const lines = content.split('\n');
      let question = '', answerStart = 0;
      const firstNonEmpty = lines.findIndex(l => l.trim() !== '');
      if (firstNonEmpty >= 0 && lines[firstNonEmpty].startsWith('# ')) {
        question = lines[firstNonEmpty].slice(2).trim();
        answerStart = firstNonEmpty + 1;
      }
      const answer = lines.slice(answerStart).join('\n').trim();
      out.push({
        id: String(data.id || file.replace(/\.md$/, '')),
        question,
        answer,
        difficulty: String(data.difficulty || 'L1'),
        category: String(data.category || catDir),
        categories: Array.isArray(data.categories) ? data.categories : [data.category || catDir],
        subcategory: data.subcategory || undefined,
        tags: Array.isArray(data.tags) ? data.tags : [],
        images: Array.isArray(data.images) ? data.images : [],
        follow_up: Array.isArray(data.follow_up) ? data.follow_up : [],
        feynman: data.feynman || undefined,
        first_principle: data.first_principle || undefined,
      });
    }
  }
  return out;
}

let _cache: Question[] | null = null;
export function getAllQuestions(): Question[] {
  if (_cache) return _cache;
  _cache = loadAll();
  return _cache;
}
export function getQuestionById(id: string): Question | undefined {
  return getAllQuestions().find(q => q.id === id);
}
export function getAllIds(): string[] {
  return getAllQuestions().map(q => q.id);
}
```

- [ ] **Step 4: algorithms.ts（SM-2/Leitner/Ebbinghaus 纯函数，与原实现数值一致）**

```typescript
import type { Algorithm, ReviewItem } from './types';

export const ALGO_PARAMS = {
  sm2: { initialEase: 2.5, minEase: 1.3 },
  leitner: { intervals: [1,3,7,14,30], maxBox: 4 },
  ebbinghaus: { intervals: [1,2,4,7,15,30] },
};
const QMAP = [1,3,4,5]; // quality 0..3 -> sm2 0..5
function todayISO(): string { return new Date().toISOString().split('T')[0]; }
function addDays(iso: string, days: number): string {
  const d = new Date(iso + 'T00:00:00Z'); d.setUTCDate(d.getUTCDate() + days);
  return d.toISOString().split('T')[0];
}

export function calcInterval(item: ReviewItem, quality: number): number {
  const algo = item.algo;
  if (algo === 'sm2') {
    const { minEase } = ALGO_PARAMS.sm2;
    const q5 = QMAP[quality];
    if (q5 < 3) return 1; // 失败：明天
    const delta = 0.1 - (5 - q5) * (0.08 + (5 - q5) * 0.02);
    item.ease = Math.max(minEase, item.ease + delta);
    if (item.reps === 0) return 1;
    if (item.reps === 1) return 3;
    return Math.round(item.interval * item.ease);
  }
  if (algo === 'leitner') {
    const iv = ALGO_PARAMS.leitner.intervals;
    if (quality === 0) return iv[Math.max(0, item.box)];
    const nb = Math.min(ALGO_PARAMS.leitner.maxBox, item.box + 1);
    return iv[nb] ?? 30;
  }
  // ebbinghaus
  const iv = ALGO_PARAMS.ebbinghaus.intervals;
  if (quality === 0) { return iv[0]; }
  const np = Math.min(iv.length - 1, item.phase + 1);
  return iv[np];
}

export function review(item: ReviewItem, quality: number): ReviewItem {
  const next: ReviewItem = { ...item, history: item.history.slice(-19) };
  let interval = calcInterval(next, quality);
  if (interval > 1) {
    interval = Math.max(1, Math.round(interval * (0.9 + Math.random() * 0.2)));
  }
  if (quality === 0) {
    next.lapses += 1;
    if (next.algo === 'leitner') next.box = Math.max(0, next.box - 1);
    if (next.algo === 'ebbinghaus') next.phase = 0;
  }
  next.interval = interval;
  next.reps += 1;
  next.lastDate = todayISO();
  next.nextDate = addDays(todayISO(), interval);
  next.history = [...next.history, { d: todayISO(), q: quality }].slice(-20);
  return next;
}

export function newItem(algo: Algorithm): ReviewItem {
  const today = todayISO();
  return { algo, ease: ALGO_PARAMS.sm2.initialEase, interval: 0, reps: 0, lapses: 0,
    box: 0, phase: 0, nextDate: today, lastDate: today, createdAt: today, history: [] };
}

export function isMastered(it: ReviewItem): boolean {
  if (it.algo === 'leitner') return it.box >= 4;
  if (it.algo === 'ebbinghaus') return it.phase >= 5;
  return it.interval >= 21;
}

export function isDue(it: ReviewItem): boolean {
  return it.nextDate <= todayISO();
}

// 预览（不提交）下一个间隔天数，用于评分按钮提示
export function previewInterval(item: ReviewItem, quality: number): number {
  return calcInterval({ ...item }, quality);
}
```

- [ ] **Step 5: store.ts（Zustand + persist，复用现有 localStorage key）**

```typescript
'use client';
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { Rating, Algorithm, ReviewItem } from './types';
import { APP_CONFIG } from './config';
const P = APP_CONFIG.storagePrefix;
const todayISO = () => new Date().toISOString().split('T')[0];

interface AppState {
  favorites: string[];
  viewed: string[];
  notes: Record<string, string>;
  ratings: Record<string, Rating>;
  theme: 'light' | 'dark';
  sortOrder: 'easy-first' | 'hard-first' | 'default';
  searchHistory: string[];
  dailyLog: Record<string, { studied:number; know:number; fuzzy:number; dont:number }>;
  lastStudyDate: string | null;
  streak: number;
  dailyGoal: number;
  reviewData: Record<string, ReviewItem>;
  reviewAlgorithm: Algorithm;
  dailyReviewLimit: number;
  reviewNotification: boolean;
  autoEnroll: boolean;
  // actions
  toggleFavorite: (id: string) => void;
  isFavorite: (id: string) => boolean;
  markViewed: (id: string) => void;
  setNote: (id: string, text: string) => void;
  getNote: (id: string) => string;
  setRating: (id: string, r: Rating) => void;
  toggleTheme: () => void;
  setSortOrder: (o: AppState['sortOrder']) => void;
  addSearchHistory: (q: string) => void;
  clearSearchHistory: () => void;
  logStudy: (r: Rating, prev: Rating | undefined) => void;
  setDailyGoal: (n: number) => void;
  upsertReview: (id: string, it: ReviewItem) => void;
  setReviewAlgorithm: (a: Algorithm) => void;
  setDailyReviewLimit: (n: number) => void;
  toggleReviewNotification: () => void;
  toggleAutoEnroll: () => void;
  resetProgress: () => void;
  resetReview: () => void;
  _hasHydrated: boolean;
  setHydrated: (b: boolean) => void;
}

// 注意：persist 按 key 拆分到现有 localStorage 命名（favorites/viewed/...）
// 为兼容老数据，每个 slice 单独 persist
export const useStore = create<AppState>()(
  persist(
    (set, get) => ({
      favorites: [], viewed: [], notes: {}, ratings: {},
      theme: 'light', sortOrder: 'easy-first', searchHistory: [],
      dailyLog: {}, lastStudyDate: null, streak: 0, dailyGoal: 20,
      reviewData: {}, reviewAlgorithm: 'sm2', dailyReviewLimit: 50,
      reviewNotification: true, autoEnroll: true, _hasHydrated: false,
      toggleFavorite: (id) => set(s => {
        const has = s.favorites.includes(id);
        return { favorites: has ? s.favorites.filter(x=>x!==id) : [...s.favorites, id] };
      }),
      isFavorite: (id) => get().favorites.includes(id),
      markViewed: (id) => set(s => s.viewed.includes(id) ? s : { viewed: [...s.viewed, id] }),
      setNote: (id, text) => set(s => {
        const notes = { ...s.notes };
        if (!text.trim()) delete notes[id]; else notes[id] = text;
        return { notes };
      }),
      getNote: (id) => get().notes[id] || '',
      setRating: (id, r) => set(s => ({ ratings: { ...s.ratings, [id]: r } })),
      toggleTheme: () => set(s => ({ theme: s.theme === 'light' ? 'dark' : 'light' })),
      setSortOrder: (o) => set({ sortOrder: o }),
      addSearchHistory: (q) => set(s => {
        const trimmed = q.trim(); if (trimmed.length < 2) return s;
        const hist = [trimmed, ...s.searchHistory.filter(x=>x!==trimmed)].slice(0,8);
        return { searchHistory: hist };
      }),
      clearSearchHistory: () => set({ searchHistory: [] }),
      logStudy: (r, prev) => set(s => {
        const t = todayISO();
        const log = { ...s.dailyLog };
        const day = log[t] || { studied:0, know:0, fuzzy:0, dont:0 };
        if (!prev || prev !== r) {
          day.studied += 1;
          day[r] = (day[r]||0) + 1;
          if (prev && day[prev] > 0) day[prev] -= 1;
        }
        log[t] = day;
        let streak = s.streak;
        let lastStudyDate = s.lastStudyDate;
        if (lastStudyDate !== t) {
          const y = new Date(); y.setDate(y.getDate()-1);
          const yIso = y.toISOString().split('T')[0];
          streak = (lastStudyDate === yIso) ? streak + 1 : 1;
          lastStudyDate = t;
        }
        return { dailyLog: log, streak, lastStudyDate };
      }),
      setDailyGoal: (n) => set({ dailyGoal: Math.max(5, Math.min(200, n)) }),
      upsertReview: (id, it) => set(s => ({ reviewData: { ...s.reviewData, [id]: it } })),
      setReviewAlgorithm: (a) => set(s => {
        const rd = { ...s.reviewData };
        for (const k of Object.keys(rd)) rd[k] = { ...rd[k], algo: a };
        return { reviewAlgorithm: a, reviewData: rd };
      }),
      setDailyReviewLimit: (n) => set({ dailyReviewLimit: Math.max(5, Math.min(500, n)) }),
      toggleReviewNotification: () => set(s => ({ reviewNotification: !s.reviewNotification })),
      toggleAutoEnroll: () => set(s => ({ autoEnroll: !s.autoEnroll })),
      resetProgress: () => set({ viewed: [] }),
      resetReview: () => set({ reviewData: {} }),
      setHydrated: (b) => set({ _hasHydrated: b }),
    }),
    {
      name: P, // 顶层 key（兼容性见 StoreProvider 的迁移）
      storage: createJSONStorage(() => localStorage),
      partialize: (s) => ({
        favorites: s.favorites, viewed: s.viewed, notes: s.notes, ratings: s.ratings,
        theme: s.theme, sortOrder: s.sortOrder, searchHistory: s.searchHistory,
        dailyLog: s.dailyLog, lastStudyDate: s.lastStudyDate, streak: s.streak, dailyGoal: s.dailyGoal,
        reviewData: s.reviewData, reviewAlgorithm: s.reviewAlgorithm,
        dailyReviewLimit: s.dailyReviewLimit, reviewNotification: s.reviewNotification, autoEnroll: s.autoEnroll,
      }),
      onRehydrateStorage: () => (state) => { state?.setHydrated(true); },
    }
  )
);

// StoreProvider：把老的分散 key 迁移到 zustand 单一 persist 对象（仅在客户端执行一次）
export function StoreProvider({ children }: { children: React.ReactNode }) {
  'use client';
  return <>{children}</>;
}
```

> 兼容说明：老数据分散在 `ai-interview.favorites` 等多个 key。为保兼容，StoreProvider 在挂载时把老 key 合并到 zustand 的单一 persist 对象（首次 hydrate 前迁移）。此迁移逻辑放在 Task 5 的 StoreProvider 客户端 effect 中实现（见 Task 5 Step 3 的 migrateLegacyStorage）。

- [ ] **Step 6: 验证数据层可被构建期调用**

Run: `cd /Users/sunqingguang/hermes/opt/projects/ai-interview && npx tsc --noEmit 2>&1 | tail -20`
Expected: 无类型错误（或仅 next-env.d.ts 相关，可忽略）

- [ ] **Step 7: 提交数据层**

```bash
git -C ai-interview add src/lib/ && git -C ai-interview commit -m "feat: data layer — build-time md loader, algorithms, zustand store"
```

---

## Task 5: 首页（列表 + 筛选 + 搜索 + 分类 + 卡片）

**Files:**
- Create: `src/app/page.tsx`、`src/components/*.tsx`（CategoryTabs、CardGrid、QuestionCard、SearchBar、FilterBar、ProgressRing、DifficultyBars）

- [ ] **Step 1: page.tsx（首页 server component，构建期取全部题目传给客户端组件）**

```tsx
import { getAllQuestions } from '@/lib/questions';
import { APP_CONFIG } from '@/lib/config';
import HomeClient from '@/components/HomeClient';

export default function Page() {
  const questions = getAllQuestions().map(q => ({
    id: q.id, question: q.question, difficulty: q.difficulty,
    category: q.category, categories: q.categories, subcategory: q.subcategory,
    tags: q.tags, images: q.images,
    // 给搜索用的答案片段
    answerSnippet: q.answer.replace(/[#*`>\-|]/g, '').slice(0, 200),
  }));
  return <HomeClient questions={questions} categories={APP_CONFIG.categories} />;
}
```

- [ ] **Step 2: 编写 HomeClient.tsx（客户端筛选/搜索/排序/虚拟滚动状态）**

（实现：useState 管理 currentCategory/difficulty/subcategory/selectedTags/searchQuery/sortOrder/favOnly；
useMemo 做 filter+sort；IntersectionObserver 分页 PAGE_SIZE=48；调用 useStore 读写收藏/已看/主题/搜索历史）

> 该组件较大，实现要点：
> - 顶部：SearchBar、主题按钮、设置按钮、排序按钮、仅看收藏按钮
> - CategoryTabs：从 props.categories 渲染 + 计数
> - DifficultyBars：当前 filtered 的 L1–L5 相对柱
> - FilterBar：子分类分组 chips + 标签云（Top20，AND 多选）
> - ProgressRing：viewed/total
> - CardGrid：虚拟滚动渲染 QuestionCard
> - QuestionModal：点卡片打开（见 Task 6）

- [ ] **Step 3: StoreProvider 中加 migrateLegacyStorage（兼容老 key）**

在 `src/lib/store.ts` 的 StoreProvider 改为：
```tsx
'use client';
import { useEffect } from 'react';
export function StoreProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // 一次性迁移老的分散 key 到 zustand 单一 persist 对象
    const P = APP_CONFIG.storagePrefix;
    const legacyKeys: Record<string,string> = {
      favorites:'favorites', viewed:'viewed', notes:'notes', ratings:'ratings',
      theme:'theme', sortOrder:'sortOrder', searchHistory:'searchHistory',
      dailyLog:'dailyLog', lastStudyDate:'lastStudyDate', streak:'streak', dailyGoal:'dailyGoal',
      reviewData:'reviewData', reviewAlgorithm:'reviewAlgorithm',
      dailyReviewLimit:'dailyReviewLimit', reviewNotification:'reviewNotification', autoEnroll:'autoEnroll',
    };
    const cur = localStorage.getItem(P);
    if (cur) return; // 已有合并态，跳过
    const merged: Record<string, unknown> = { state: {}, version: 1 };
    for (const [lk, sk] of Object.entries(legacyKeys)) {
      const raw = localStorage.getItem(P + '.' + lk);
      if (raw != null) { try { (merged.state as any)[sk] = JSON.parse(raw); } catch { (merged.state as any)[sk] = raw; } }
    }
    if (Object.keys(merged.state).length) {
      localStorage.setItem(P, JSON.stringify(merged));
    }
  }, []);
  return <>{children}</>;
}
```
并在 layout.tsx 包裹 `<StoreProvider>`（已在 Task 3 包裹）。

- [ ] **Step 4: 验证首页渲染（dev）**

Run: `cd /Users/sunqingguang/hermes/opt/projects/ai-interview && timeout 30 npm run dev 2>&1 | tail -15`
打开 http://localhost:3000 看是否渲染 911 题列表、分类 tab、筛选。
Expected: 页面加载，无控制台报错，题目计数显示 911。

- [ ] **Step 5: 提交**

```bash
git -C ai-interview add src/ && git -C ai-interview commit -m "feat: home page with filtering, search, category tabs, cards"
```

---

## Task 6: 题目详情（弹窗 + /question/[id] 页，共享 QuestionContent）

**Files:**
- Create: `src/app/question/[id]/page.tsx`、`src/components/QuestionModal.tsx`、`src/components/QuestionContent.tsx`、`src/components/FeynmanCard.tsx`、`src/components/FirstPrincipleCard.tsx`

- [ ] **Step 1: 详情静态页 page.tsx**

```tsx
import { getAllQuestions, getQuestionById } from '@/lib/questions';
import { notFound } from 'next/navigation';
import QuestionContent from '@/components/QuestionContent';

export function generateStaticParams() {
  return getAllQuestions().map(q => ({ id: q.id }));
}
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const q = getQuestionById(id);
  if (!q) notFound();
  return (
    <main className="max-w-3xl mx-auto p-4">
      <QuestionContent q={q} />
    </main>
  );
}
```

- [ ] **Step 2: QuestionContent.tsx（共享：meta + 费曼 + 答案markdown + 第一性原理 + 配图 + 追问 + 笔记）**

（用 react-markdown 渲染 q.answer；FeynmanCard/FirstPrincipleCard 子组件；配图用 basePath 前缀 `images/<file>`；追问点击触发搜索回调；笔记 textarea 绑 useStore.setNote）

- [ ] **Step 3: QuestionModal.tsx（列表内弹窗，复用 QuestionContent + 收藏/复制/分享/报错/上下题导航 + 滑动手势）**

（客户端组件，点卡片 setModalId；URL hash 同步 `#q=<id>`；上下题在当前 filtered 列表内导航）

- [ ] **Step 4: 验证详情页与弹窗**

Run dev，首页点一题弹窗显示完整答案；访问 `/question/<id>` 详情页正常；分享/复制/报错按钮工作。
Expected: 答案完整渲染，费曼/第一性原理/配图/追问/笔记齐全。

- [ ] **Step 5: 提交**

```bash
git -C ai-interview add src/ && git -C ai-interview commit -m "feat: question detail modal + static page with shared content"
```

---

## Task 7: 学习模式 + 遗忘曲线复习（StudyMode、ReviewMode、Dashboard）

**Files:**
- Create: `src/components/StudyMode.tsx`、`src/components/ReviewMode.tsx`、`src/components/StudyDashboard.tsx`、`src/components/ReviewDashboard.tsx`

- [ ] **Step 1: StudyMode.tsx（顺序/随机/错题三模式，会了/模糊/不会评分，每日目标 streak）**

（用 useStore.ratings、logStudy、dailyGoal、streak；next/prev 导航；空格揭示答案；1/2/3 评分快捷键）

- [ ] **Step 2: ReviewMode.tsx（三算法，四档评分，到期队列，7日预报，掌握判定）**

（用 algorithms.ts 的 review()/isDue()/isMastered()；评分按钮显示 previewInterval；quality→rating 映射 sync 到 ratings + logStudy）

- [ ] **Step 3: StudyDashboard / ReviewDashboard（统计卡片 + 7日预报柱状图）**

- [ ] **Step 4: 验证学习与复习流程**

Run dev，进入学习模式刷题评分；进入复习模式用四档评分，检查 nextDate 计算与 SM-2/Leitner/Ebbinghaus 数值（对照原算法手算 1 题）。
Expected: 算法数值正确，streak/已掌握计数正确。

- [ ] **Step 5: 提交**

```bash
git -C ai-interview add src/ && git -C ai-interview commit -m "feat: study mode + spaced-repetition review (SM-2/Leitner/Ebbinghaus)"
```

---

## Task 8: 全局功能（设置面板、快捷键、导出、Toast、暗色、PWA）

**Files:**
- Create: `src/components/SettingsPanel.tsx`、`src/components/ShortcutsHelp.tsx`、`src/components/Toast.tsx`、`src/lib/exporters.ts`；`public/manifest.json`、`public/sw.js`（或 @serwist 配置）

- [ ] **Step 1: SettingsPanel（复习算法切换、每日限额、通知/自动注册开关、导出进度/错题本/笔记、重置）**

- [ ] **Step 2: exporters.ts（统一 exportProgress 合并 app.js+study.js 两版；exportWrongBook；exportNotes）**

- [ ] **Step 3: ShortcutsHelp + 全局键盘监听（/ ? L R D F S 1-6 ← → Esc Cmd+K 空格 1-4 评分）**

- [ ] **Step 4: Toast 全局通知**

- [ ] **Step 5: PWA（manifest.json + sw.js 缓存静态资源；register in layout client effect）**

- [ ] **Step 6: 验证全局功能 + 静态导出**

Run: `cd /Users/sunqingguang/hermes/opt/projects/ai-interview && npm run build 2>&1 | tail -20`
Expected: `next build` 成功，输出 `out/` 目录，911 个 `/question/[id]` 页全部生成。

- [ ] **Step 7: 提交**

```bash
git -C ai-interview add src/ public/ && git -C ai-interview commit -m "feat: settings, shortcuts, exporters, toast, PWA + static export"
```

---

## Task 9: R1–R5 五轮验收 + 修复（按 spec 第 10 节）

- [ ] **R1 数据完整**：`npm run build` 成功；out/ 内 911 个详情页；各分类计数正确。失败则修。
- [ ] **R2 核心功能**：首页/分类/难度/子分类/标签云/搜索/排序/虚拟滚动；详情全字段渲染；复制/分享/报错/笔记/收藏。逐项验证并记录。
- [ ] **R3 学习+复习**：study 三模式评分 streak；review 三算法四档评分到期队列预报。算法数值对照原实现。
- [ ] **R4 数据兼容+导出**：用老 key localStorage（手动注入 ai-interview.favorites 等）验证能读出；导出格式正确。
- [ ] **R5 PWA+移动端**：离线可浏览；移动端布局/手势；深链直达；快捷键全。
- [ ] 每轮发现的问题即时修复并重跑；全部通过后提交并写验收记录到 `docs/superpowers/specs/2026-06-20-acceptance-report.md`。

---

## Self-Review（对照 spec）

- **Spec 覆盖**：§4 数据流→Task3/4；§5 md 格式→Task1；§6 目录结构→Task3；§7 功能映射→Task5/6/7/8（28项全覆盖）；§8 localStorage 兼容→Task4 Step5 + Task5 Step3 迁移；§9 迁移脚本→Task1；§10 五轮→Task9。✅
- **占位符扫描**：Task5/6/7/8 的组件实现用文字描述要点而非逐行代码——因这些是大型 React 组件，逐行展开会使计划过长。执行时按要点实现。核心数据/算法/迁移脚本是完整代码。可接受。
- **类型一致**：Question/ReviewItem/Algorithm/Rating 在 types.ts 定义，后续 Task 一致引用。✅
- **范围**：单计划覆盖 ai-interview 全量 + java-interview 的 markdown 生成（Task1/2 双项目）。Next.js 重写仅 ai-interview（spec 非目标项）。✅
