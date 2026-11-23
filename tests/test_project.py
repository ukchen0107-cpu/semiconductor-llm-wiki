import unittest, pathlib, json, re
ROOT=pathlib.Path(__file__).resolve().parents[1]
class WikiTests(unittest.TestCase):
 def test_sources_at_least_five(self):
  self.assertGreaterEqual(len(list((ROOT/'data/sources').glob('S*.json'))),5)
 def test_source_structure(self):
  docs=[json.loads(f.read_text(encoding='utf8')) for f in (ROOT/'data/sources').glob('S*.json')]
  ids=[d['id'] for d in docs];urls=[d['url'] for d in docs]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(len(urls),len(set(urls)))
  for d in docs:
   for k in ('title','publisher','summary','beginner_explanation','url','category'):self.assertTrue(d[k])
   self.assertTrue(d['url'].startswith('https://'))
 def test_wiki_pages(self):
  for f in (ROOT/'data/sources').glob('S*.json'):
   k=f.stem
   self.assertTrue((ROOT/'wiki'/f'{k}.html').is_file())
   self.assertTrue((ROOT/'wiki'/f'{k}.md').is_file())
 def test_html_and_source_links(self):
  h=(ROOT/'slides/index.html').read_text(encoding='utf8')
  for id in re.findall(r'wiki/(S\d+).html',h):self.assertTrue((ROOT/'wiki'/f'{id}.html').exists())
  self.assertIn('id="next"',h);self.assertIn('id="prev"',h)
 def test_public_pages(self):
  self.assertTrue((ROOT/'index.html').is_file())
  self.assertTrue((ROOT/'slides/index.html').is_file())
 def test_workflow(self):
  self.assertTrue((ROOT/'AGENTS.md').exists())
  self.assertTrue((ROOT/'.github/workflows/pages.yml').exists())
 def test_no_secrets(self):
  for p in ROOT.rglob('*'):
   if p.is_file() and '.git' not in p.parts and 'tests' not in p.parts and p.suffix in ('.json','.py','.md','.html','.yml'):
    s=p.read_text(encoding='utf8')
    self.assertNotIn('-----BEGIN PRIVATE KEY-----',s)
if __name__=='__main__':unittest.main()
