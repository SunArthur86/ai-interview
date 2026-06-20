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
    """从 config.js 提取 categories 的 key->files 映射（保持声明顺序）。"""
    cfg_path = os.path.join(project_dir, 'config.js')
    with open(cfg_path, encoding='utf-8') as f:
        text = f.read()
    m = re.search(r"categories\s*:\s*\{", text)
    start = m.end() - 1  # 指向 {
    depth = 0
    end = start
    for i in range(start, len(text)):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    block = text[start:end]
    cats = {}
    order = []
    for km in re.finditer(r"'([^']+)'\s*:\s*\{", block):
        key = km.group(1)
        seg = block[km.end():]
        d = 1
        j = 0
        while j < len(seg) and d > 0:
            if seg[j] == '{':
                d += 1
            elif seg[j] == '}':
                d -= 1
            j += 1
        obj = seg[:j]
        if key == 'all':
            order.append(key)
            cats[key] = None
            continue
        fm = re.search(r"files\s*:\s*\[(.*?)\]", obj, re.S)
        files = []
        if fm:
            files = ["data/" + os.path.basename(x.strip().strip("'\""))
                     for x in fm.group(1).split(',') if x.strip()]
        cats[key] = files
        order.append(key)
    return cats, order


def yaml_escape_str(s):
    s = str(s)
    s = s.replace('\\', '\\\\').replace('"', '\\"')
    s = s.replace('\n', ' ').replace('\r', '')
    return '"' + s + '"'


def render_frontmatter(meta):
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
        print('usage: migrate_to_md.py <project_dir>')
        sys.exit(1)
    project_dir = os.path.abspath(sys.argv[1])
    cats, order = parse_config_categories(project_dir)
    order = [c for c in order if c != 'all' and cats.get(c)]

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

    print('Wrote %d markdown files to %s' % (written, out_root))
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
