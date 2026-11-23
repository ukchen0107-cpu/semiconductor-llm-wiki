"""Wiki generator: read source JSON and refresh Wiki entries + index.
Existing teacher-reviewed HTML presentation stays intact; add any new sources
to the public homepage and references panel without replacing its visual deck.
"""
import json, pathlib, html, re
R=pathlib.Path(__file__).resolve().parents[1]
sources=sorted((R/'data/sources').glob('S*.json'))
docs=[json.loads(p.read_text(encoding='utf8')) for p in sources]
ids=[d['id'] for d in docs]
urls=[d['url'] for d in docs]
if len(ids)<5 or len(ids)!=len(set(ids)) or len(urls)!=len(set(urls)):
 raise ValueError('Need five unique sources, IDs and URLs')
for d in docs:
 for key in ('id','title','publisher','url','category','summary','beginner_explanation'):
  if not d.get(key):raise ValueError(f'Missing {key} in {d.get("id")}')
 if not d['url'].startswith('https://'):raise ValueError('Only HTTPS sources allowed')
 (R/'wiki'/f"{d['id']}.md").write_text(
 f"# {d['title']}\n\n- Wiki ID：{d['id']}\n- 類別：{d['category']}\n- 出版者：{d['publisher']}\n- 原始標題：{d.get('source_title','')}\n- 來源：{d['url']}\n- 查核日期：{d.get('checked_on','')}\n\n## 資料摘要\n{d['summary']}\n\n## 初學者理解\n{d['beginner_explanation']}\n\n> 此為依原始資料撰寫的摘要，不是逐字重製。\n",encoding='utf8')
 def e(s):return html.escape(str(s),quote=True)
 page=f"""<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(d['title'])}｜半導體 LLM Wiki</title><style>body{{margin:0;background:#08111f;color:#eaf4fb;font:17px/1.8 system-ui,"Noto Sans TC",sans-serif}}main{{max-width:800px;padding:24px;margin:5vh auto}}a{{color:#60e2cb}}article{{background:#112338;border:1px solid #294057;padding:30px;border-radius:20px}}h1{{line-height:1.3}}h2{{color:#60e2cb}}small{{color:#a7bbce}}footer{{margin-top:30px}}</style></head><body><main><p><a href="../index.html">← Wiki 首頁</a> · <a href="../slides/">教學簡報</a></p><article><small>{e(d['id'])} · {e(d['category'])}</small><h1>{e(d['title'])}</h1><h2>重點摘要</h2><p>{e(d['summary'])}</p><h2>初學者解釋</h2><p>{e(d['beginner_explanation'])}</p><h2>來源與查核</h2><p>{e(d['publisher'])} · {e(d.get('source_title',''))}</p><a href="{e(d['url'])}" target="_blank" rel="noopener noreferrer">查看官方來源</a><p><small>查核日期：{e(d.get('checked_on',''))} · 人工摘要，非原文全文轉載</small></p></article><footer><a href="../index.html">返回 Wiki 知識庫</a></footer></main></body></html>"""
 (R/'wiki'/f"{d['id']}.html").write_text(page,encoding='utf8')
(R/'wiki/index.json').write_text(json.dumps(docs,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
# Extend the existing public wiki cards when new entries have been ingested.
home=R/'index.html'
s=home.read_text(encoding='utf8')
for d in docs:
 if f'href="wiki/{d["id"]}.html"' in s:continue
 e=lambda v:html.escape(str(v),quote=True)
 card=f'<article class="card" data-search="{e(d["title"]+" "+d["summary"]+" "+d["category"])}"><span class="tag">{e(d["id"])} · {e(d["category"])}</span><h3>{e(d["title"])}</h3><p>{e(d["beginner_explanation"])}</p><div class="small">來源：{e(d["publisher"])} · {e(d.get("checked_on",""))}</div><p><a href="wiki/{e(d["id"])}.html">開啟 Wiki 條目</a>　<a href="{e(d["url"])}" target="_blank" rel="noopener noreferrer">原始來源</a></p></article>'
 mark='</div><p id="empty"'
 if mark not in s:raise ValueError('Wiki card insert point missing')
 s=s.replace(mark,card+mark,1)
home.write_text(s,encoding='utf8')
# Add newly ingested source references to the final slideshow bibliography.
deck=R/'slides/index.html'
s=deck.read_text(encoding='utf8')
for d in docs:
 if f'href="../wiki/{d["id"]}.html"' in s:continue
 link=f'<a href="../wiki/{d["id"]}.html" class="srcitem">{html.escape(d["id"])} · {html.escape(d["title"])}</a>'
 # Insert next to the last bibliography source, without altering teaching slides.
 match=re.search(r'(</div><div class="refs">WIKI 來源)',s)
 if not match:raise ValueError('Slideshow bibliography insert point missing')
 s=s[:match.start()]+link+s[match.start():]
deck.write_text(s,encoding='utf8')
print(f'Ingested {len(docs)} sources; wiki, index and bibliography checked')
