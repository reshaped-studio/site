from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import sys,xml.etree.ElementTree as ET
root=Path(sys.argv[1]);prefix=sys.argv[2] if len(sys.argv)>2 else ''
class Audit(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.refs=[];self.tags=[];self.attrs=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append(tag);self.attrs.append((tag,a))
  if 'id' in a:self.ids.append(a['id'])
  for attr in ['href','src']:
   if a.get(attr):self.refs.append(a[attr])
files=list(root.rglob('*.html'));parsed={}
for file in files:
 a=Audit();a.feed(file.read_text());parsed[file.resolve()]=a
 assert len(a.ids)==len(set(a.ids)),f'duplicate IDs: {file}'
 assert a.tags.count('h1')==1,file
 assert a.tags.count('main')==1,file
for file,a in parsed.items():
 for ref in a.refs:
  u=urlsplit(ref)
  if u.scheme or u.netloc:continue
  path=unquote(u.path)
  if path.startswith('/'):
   if prefix:assert path.startswith(prefix+'/') or path==prefix+'/',(file,path)
   path=path[len(prefix):].lstrip('/');target=root/path
  else:target=file.parent/path if path else file
  if path.endswith('/') or target.is_dir():target=target/'index.html'
  assert target.exists(),f'{file}: {ref} missing {target}'
  if u.fragment and target.suffix=='.html':assert u.fragment in parsed[target.resolve()].ids,(file,ref)
for slug in ['coffee-ordering','class-booking','support-workspace']:
 p=(root/'design-plans'/slug/'index.html').resolve();a=parsed[p];text=p.read_text()
 for id in ['context','opportunity','insights','objects','flows','summary']:assert id in a.ids
 assert sum(1 for t,attrs in a.attrs if attrs.get('class')=='object-guide')==3
 assert sum(1 for t,attrs in a.attrs if 'data-enlarge' in attrs)==5
 assert all('hidden' not in attrs for t,attrs in a.attrs if attrs.get('class')=='object-guide'),'no-JS panels must remain visible'
 assert all('hidden' in attrs for t,attrs in a.attrs if 'data-enlarge' in attrs),'enhanced controls start hidden'
 assert 'Draft for review' in text
for svg in root.glob('img/design-plans/*.svg'):ET.parse(svg)
assert len(list(root.glob('img/design-plans/*.svg')))==15
home=(root/'index.html').read_text();assert home.index('id="section-plan"')<home.index('id="method-pipeline"')<home.index('id="design-plans"')
assert 'Oat latte' in home
assert 'mailto:hello@reshaped.studio' in home
assert '<form' not in home
assert 'id="section-who"' not in home and 'id="section-what"' not in home
print(f'Passed: {len(files)} pages, local links and fragments, assets, 15 SVGs, example sections, no-JS guides, gallery placement; prefix {prefix or "/"}.')
