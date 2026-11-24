"""Check generated HTML, links, assets and preservation of existing support routes."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from xml.etree import ElementTree
import json
root=Path(__file__).resolve().parent.parent
apps=json.loads((root/'apps/catalog.json').read_text())
class Check(HTMLParser):
 def __init__(self): super().__init__(); self.links=[];self.ids=[];self.h1=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='h1':self.h1+=1
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
sitemap=ElementTree.parse(root/'sitemap.xml')
locations=[node.text for node in sitemap.findall('{*}url/{*}loc')]
expected=['https://apportico.com/']+[f'https://apportico.com/apps/{a["slug"]}/' for a in apps]
assert locations==expected and len(locations)==len(set(locations))
assert 'Sitemap: https://apportico.com/sitemap.xml' in (root/'robots.txt').read_text()
for a, canonical in zip(apps, expected[1:]):
 page=(root/'apps'/a['slug']/'index.html').read_text()
 assert f'rel="canonical" href="{canonical}"' in page
 schema=json.loads(page.split('<script type="application/ld+json">',1)[1].split('</script>',1)[0])
 assert schema['@type']=='SoftwareApplication' and schema['url']==canonical and schema['installUrl']==a['store']
 assert schema['publisher']['name']==a['publisher']
 assert a['screenshot_device'] in a['devices'] and len(a['use_cases'])==2
 support=a.get('support')
 assert not support or support.startswith('https://') or (support.startswith('/') and not support.startswith('//'))
assert (root/'CNAME').read_text().strip()=='apportico.com'
assert 'window.location.replace' in (root/'apps/index.html').read_text()
print(f'PASS: {len(apps)} app routes, local links and assets, canonical URLs, sitemap, structured data, CNAME and legacy redirect')
