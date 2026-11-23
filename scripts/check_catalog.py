"""Check generated HTML, links, assets and preservation of existing support routes."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
root=Path(__file__).resolve().parent.parent
apps=json.loads((root/'apps/catalog.json').read_text())
assert len({a['slug'] for a in apps})==len(apps), 'Duplicate catalog slug'
for a in apps:
 def assert_image(src):
  url=urlsplit(src)
  assert not url.scheme and not url.netloc and src.startswith('/apps/assets/'), (a['slug'],src)
  asset=(root/src.lstrip('/')).resolve()
  assert asset.is_relative_to(root/'apps/assets') and asset.is_file(), (a['slug'],src)
 assert_image(a['icon'])
 assert_image(a['screenshot'])
 for key in ('screenshot_alt','screenshot_caption'):
  if key in a: assert isinstance(a[key],str) and a[key].strip(), (a['slug'],key)
 for key in ('features','platforms'):
  arr=a.get(key,[])
  assert isinstance(arr,list) and all(isinstance(item,str) and item.strip() for item in arr), (a['slug'],key)
 gallery=a.get('gallery',[])
 assert isinstance(gallery,list), (a['slug'],'gallery')
 seen={a['screenshot']}
 for item in gallery:
  assert isinstance(item,dict) and isinstance(item.get('alt'),str) and item['alt'].strip(), (a['slug'],item)
  assert_image(item['src'])
  assert item['src'] not in seen, (a['slug'],item['src'])
  seen.add(item['src'])
class Check(HTMLParser):
 def __init__(self): super().__init__(); self.links=[];self.ids=[];self.h1=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='img':assert 'alt' in a, a
  for name in ('href','src'):
   if name in a:self.links.append(a[name])
for file in [root/'index.html']+[root/'apps'/a['slug']/'index.html' for a in apps]:
 p=Check();p.feed(file.read_text());assert p.h1==1,(file,p.h1);assert len(p.ids)==len(set(p.ids)),file
 assert '{{' not in file.read_text() and '{arrow}' not in file.read_text()
 for link in p.links:
  u=urlsplit(link)
  if u.scheme or u.netloc: continue
  dest=(root/unquote(u.path).lstrip('/')) if u.path.startswith('/') else (file.parent/unquote(u.path))
  if not u.path:dest=file
  if dest.is_dir():dest/='index.html'
  assert dest.exists(),(file,link)
  if u.fragment and dest.suffix=='.html':
   q=Check();q.feed(dest.read_text());assert u.fragment in q.ids,(dest,u.fragment)
for a in apps:
 assert a['store'].startswith('https://apps.apple.com/')
 assert (root/'apps'/a['slug']/'index.html').exists()
assert (root/'CNAME').read_text().strip()=='apportico.com'
assert 'window.location.replace' in (root/'apps/index.html').read_text()
print(f'PASS: {len(apps)} app routes; all local links/assets/anchors; one H1 per page; CNAME; legacy redirect')
