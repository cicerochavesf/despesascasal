from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
old = '<!-- Despesas Casal - Controle Financeiro | versão 2.85 -->'
new = '<!-- Despesas Casal - Controle Financeiro | versão 2.86 -->'
if old not in s:
    raise SystemExit('Versão 2.85 não encontrada')
s = s.replace(old, new, 1)

marker = 'v286-unify-history-jan-jun-script'
if marker not in s:
    block = r'''<script id="v286-unify-history-jan-jun-script">
(function(){
  const V286_MIGRATION='v286UnifyJanJunWithJulDec';
  const V286_HISTORY_MONTHS=['2026-01','2026-02','2026-03','2026-04','2026-05','2026-06'];
  const V286_REFERENCE_MONTHS=['2026-07','2026-08','2026-09','2026-10','2026-11','2026-12'];
  let v286SaveQueued=false;

  function v286IsHistorical(item){
    return !!(item&&(item.historical===true||String(item.id||'').startsWith('b_hist_')||String(item.id||'').startsWith('tx_hist_')||item.historicalSource==='Caderno Jan-Jun/2026'));
  }
  function v286SubKey(item){return norm(cleanName(item?.sub||item?.description||item?.desc||''));}
  function v286Local(item){
    const explicit=typeof v231ValidLocal==='function'?v231ValidLocal(item?.city):'';
    if(explicit)return explicit;
    const legacy=typeof v231LegacyCityOf==='function'?v231LegacyCityOf(item?.sub||''):cityOf(item?.sub||'');
    return (typeof v231ValidLocal==='function'?v231ValidLocal(legacy):legacy)||'Compartilhado';
  }
  function v286Person(item,local){
    const explicit=typeof v231ValidPerson==='function'?v231ValidPerson(item?.owner||item?.responsible||item?.payer):'';
    if(explicit)return explicit;
    const inferred=typeof budgetOwner==='function'?budgetOwner(item||{}):ownerOf(local);
    return (typeof v231ValidPerson==='function'?v231ValidPerson(inferred):inferred)||'Compartilhado';
  }
  function v286ReferenceMap(){
    const byName=new Map();
    V286_REFERENCE_MONTHS.forEach((month,monthIndex)=>{
      (state.budgets?.[month]||[]).forEach((item,rowIndex)=>{
        const key=v286SubKey(item);if(!key)return;
        const local=v286Local(item),person=v286Person(item,local),sub=cleanName(item.sub||''),catId=String(item.cat||'');
        if(!sub||!catId)return;
        const identityKey=[catId,local,person].join('|');
        if(!byName.has(key))byName.set(key,new Map());
        const candidates=byName.get(key),current=candidates.get(identityKey)||{cat:catId,sub,local,person,count:0,latest:-1,total:0};
        current.count+=1;
        current.latest=Math.max(current.latest,monthIndex*1000+rowIndex);
        current.total+=Math.abs(Number(item.planned||0));
        current.sub=sub;
        candidates.set(identityKey,current);
      });
    });
    const refs=new Map();
    byName.forEach((candidates,key)=>{
      const winner=[...candidates.values()].sort((a,b)=>b.count-a.count||b.latest-a.latest||b.total-a.total)[0];
      if(winner)refs.set(key,winner);
    });
    return refs;
  }
  function v286Apply(){
    if(!cloudSynced||!state)return false;
    if(!state.migrations||typeof state.migrations!=='object')state.migrations={};
    if(state.migrations[V286_MIGRATION]?.completed)return false;
    if(!state.migrations.v261HistoryJanJun2026?.completed)return false;
    const refs=v286ReferenceMap();
    if(!refs.size)return false;
    let budgetChanges=0,transactionChanges=0;
    const matchedNames=new Set(),stamp=new Date().toISOString();

    V286_HISTORY_MONTHS.forEach(month=>{
      (state.budgets?.[month]||[]).forEach(item=>{
        if(!v286IsHistorical(item))return;
        const key=v286SubKey(item),ref=refs.get(key);if(!ref)return;
        matchedNames.add(key);
        const before=[item.cat,cleanName(item.sub||''),item.city,item.owner,item.responsible].join('|');
        item.cat=ref.cat;item.sub=ref.sub;item.city=ref.local;item.owner=ref.person;item.responsible=ref.person;
        const after=[item.cat,cleanName(item.sub||''),item.city,item.owner,item.responsible].join('|');
        if(before!==after)budgetChanges++;
      });
      (state.transactions?.[month]||[]).forEach(item=>{
        if(!v286IsHistorical(item))return;
        const key=v286SubKey(item),ref=refs.get(key);if(!ref)return;
        matchedNames.add(key);
        const before=[item.cat,cleanName(item.sub||''),item.city,item.responsible,item.payer].join('|');
        item.cat=ref.cat;item.sub=ref.sub;item.city=ref.local;item.responsible=ref.person;item.payer=ref.person;item.updatedAt=stamp;
        const after=[item.cat,cleanName(item.sub||''),item.city,item.responsible,item.payer].join('|');
        if(before!==after)transactionChanges++;
      });
    });

    refs.forEach((ref,key)=>{
      if(!matchedNames.has(key))return;
      if(!state.subs[ref.cat])state.subs[ref.cat]=[];
      if(!state.subs[ref.cat].some(value=>norm(cleanName(value))===norm(ref.sub)))state.subs[ref.cat].push(ref.sub);
      if(typeof v231SetSubcategoryProfile==='function')v231SetSubcategoryProfile(ref.cat,ref.sub,ref.local,ref.person);
    });

    state.migrations[V286_MIGRATION]={
      completed:true,
      at:stamp,
      reference:'Julho a dezembro de 2026',
      rule:'Mesma subcategoria usa Categoria, Local e Pessoa da identidade predominante em jul-dez/2026; empate favorece o registro mais recente.',
      matchedSubcategories:matchedNames.size,
      budgetRowsUpdated:budgetChanges,
      transactionRowsUpdated:transactionChanges,
      valuesChanged:false
    };
    if(typeof cacheCloudState==='function')cacheCloudState();
    if(!v286SaveQueued&&typeof scheduleCloudSave==='function'){
      v286SaveQueued=true;
      scheduleCloudSave(0);
      setTimeout(()=>{v286SaveQueued=false},1800);
    }
    return true;
  }

  const v286PreviousRender=render;
  render=function(){
    const result=v286PreviousRender.apply(this,arguments);
    if(v286Apply())return v286PreviousRender.apply(this,arguments);
    return result;
  };
  if(cloudSynced&&state&&v286Apply())v286PreviousRender();
})();
</script>
<!-- V2.86 — histórico jan-jun/2026 alinhado à identidade de jul-dez/2026. -->'''
    s = s.replace('</body>', block + '\n</body>', 1)

p.write_text(s, encoding='utf-8')

m = re.search(r'<script id="v286-unify-history-jan-jun-script">(.*?)</script>', s, re.S)
if not m:
    raise SystemExit('Script V2.86 não encontrado')
Path('/tmp/v286.js').write_text(m.group(1), encoding='utf-8')

sw = Path('sw.js')
t = sw.read_text(encoding='utf-8')
t = re.sub(r'financas-cn-v\d+', 'financas-cn-v249', t, count=1)
sw.write_text(t, encoding='utf-8')
