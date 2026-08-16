from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='<!-- Despesas Casal - Controle Financeiro | versão 2.86 -->'
new='<!-- Despesas Casal - Controle Financeiro | versão 2.87 -->'
if old not in s:
    raise SystemExit('V2.86 não encontrada')
s=s.replace(old,new,1)
marker='v287-planning-mobile-columns-style'
if marker not in s:
    block=Path('v287_fragment.tmp').read_text(encoding='utf-8')
    s=s.replace('</body>',block+'\n</body>',1)
p.write_text(s,encoding='utf-8')
sw=Path('sw.js')
t=sw.read_text(encoding='utf-8')
t=re.sub(r'financas-cn-v\d+','financas-cn-v250',t,count=1)
sw.write_text(t,encoding='utf-8')
