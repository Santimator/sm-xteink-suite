from pathlib import Path
import json, sys, subprocess, requests
from bs4 import BeautifulSoup
import trafilatura

root='https://vesselofhermes.beehiiv.com'
urls=[
 root+'/p/source-and-spirit',
 root+'/p/excerpt-from-chapter-5-reflections-on-an-encounter',
 root+'/p/toward-a-quantum-semiotics',
]
out=Path('workspace/vessel-of-hermes-2026')
(out/'chapters').mkdir(parents=True,exist_ok=True)
(out/'build').mkdir(parents=True,exist_ok=True)
chapters=[]
report=[]
for url in urls:
 try:
  response=requests.get(url,timeout=30)
  response.raise_for_status()
  text=trafilatura.extract(response.text,output_format='markdown',include_comments=False)
  if not text or len(text.split())<150: raise ValueError('Full article unavailable')
  title=BeautifulSoup(response.text,'html.parser').title.get_text(' ',strip=True)
  md='# '+title+'\n\n'+text+'\n'
  fname='chapters/ch%02d.md'%(len(chapters)+1)
  (out/fname).write_text(md,encoding='utf8')
  chapters.append({'source':fname})
  report.append({'url':url,'words':len(text.split()),'included':True})
 except Exception as e:
  report.append({'url':url,'error':str(e),'included':False})
(out/'build/report.json').write_text(json.dumps(report,indent=2))
if not chapters: sys.exit('Nothing accessible')
(out/'book.json').write_text(json.dumps({'title':'The Vessel of Hermes - Public Articles','author':'Jamie F','language':'en','line_spacing':'tight','chapters':chapters}))
epub=out/'build/Vessel_of_Hermes_Public_Posts_X3_X4.epub'
subprocess.run([sys.executable,'epub-builder/scripts/build_epub.py',str(out),'--out',str(epub)],check=True)
subprocess.run([sys.executable,'epub-builder/scripts/verify_epub.py',str(epub)],check=True)
