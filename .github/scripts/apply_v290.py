from pathlib import Path

STYLE = r'''<style id="v290-planning-consolidated-columns-style">
.v290-planning-width-btn{display:inline-flex!important;align-items:center!important;justify-content:center!important;min-height:34px!important;padding:7px 11px!important;border:1px solid #DCE3EC!important;border-radius:11px!important;background:#FFFFFF!important;color:#475467!important;font-size:10px!important;font-weight:900!important;white-space:nowrap!important;box-shadow:none!important}
.v290-planning-width-btn:hover{border-color:#AFC3FF!important;color:#2854E8!important;background:#F7F9FF!important}
.v290-planning-native-toolbar{display:none!important}
.v215-table-wrap th.column-resizable{position:relative!important;padding-right:18px!important}
.v215-table-wrap .column-resize-handle{display:block!important;top:0!important;right:-9px!important;bottom:0!important;width:19px!important;z-index:96!important;cursor:col-resize!important;touch-action:none!important}
.v215-table-wrap .column-resize-handle::after{left:9px!important;width:2px!important}
@media (max-width:1120px){.v215-table-wrap .column-resize-handle::after{background:#B5BFCC!important}.v215-table-wrap .column-resize-handle.is-active::after{background:#3559E0!important;box-shadow:0 0 0 3px rgba(53,89,224,.12)!important}}
@media (max-width:760px){
html.device-mobile .view-despesas .v215-table-wrap .column-resize-handle,html.device-mobile .view-receitas .v215-table-wrap .column-resize-handle{display:block!important;width:22px!important;right:-11px!important;z-index:110!important}
html.device-mobile .view-despesas .v215-table-wrap .column-resize-handle::after,html.device-mobile .view-receitas .v215-table-wrap .column-resize-handle::after{left:10px!important;background:#A8B2C1!important}
.v215-planning-section>.v23-panel-head{display:flex!important;align-items:flex-start!important;justify-content:space-between!important;gap:9px!important;flex-wrap:wrap!important}
.v215-planning-section>.v23-panel-head>div{min-width:0!important;flex:1 1 210px!important}
.v290-planning-width-btn{flex:0 0 auto!important;min-height:36px!important;font-size:9.5px!important}}
@media (max-width:430px){.v290-planning-width-btn{width:100%!important}}
</style>'''

SCRIPT = r'''<script id="v290-planning-consolidated-columns-script">
(function(){
const defs={category:{selector:'.view-despesas .v215-category-table-wrap'},subcategory:{selector:'.view-despesas .v215-subcategory-table-wrap'},revenue:{selector:'.view-receitas .v215-table-wrap'}};
function ensureOne(root,kind){const def=defs[kind],wrap=root?.querySelector(def.selector);if(!wrap)return;const table=wrap.querySelector('table');if(!table)return;if(!table.dataset.columnKey&&typeof initColumnWidthEditors==='function')initColumnWidthEditors(root);const nativeToolbar=wrap.previousElementSibling;if(nativeToolbar?.classList?.contains('column-width-toolbar'))nativeToolbar.classList.add('v290-planning-native-toolbar');const section=wrap.closest('.v215-planning-section'),head=section?.querySelector(':scope > .v23-panel-head');if(head&&!head.querySelector(`.v290-planning-width-btn[data-kind="${kind}"]`)){const button=document.createElement('button');button.type='button';button.className='v290-planning-width-btn';button.dataset.kind=kind;button.textContent='Ajustar colunas';button.title='Editar a largura das colunas desta tabela';button.addEventListener('click',()=>window.v290OpenPlanningWidth(kind));head.appendChild(button)}}
window.v290OpenPlanningWidth=function(kind){const root=document.getElementById('app'),def=defs[kind],wrap=def?root?.querySelector(def.selector):null,table=wrap?.querySelector('table');if(!table)return alert('Esta tabela não está disponível nesta tela.');if(!table.dataset.columnKey&&typeof initColumnWidthEditors==='function')initColumnWidthEditors(root);if(typeof installColumnDragResizers==='function')installColumnDragResizers(root);const key=table.dataset.columnKey;if(!key)return alert('Não foi possível abrir a configuração das colunas.');openColumnWidthEditor(encodeURIComponent(key))};
window.v290EnsurePlanningColumns=function(root=document.getElementById('app')){if(!root)return;if(typeof initColumnWidthEditors==='function')initColumnWidthEditors(root);ensureOne(root,'category');ensureOne(root,'subcategory');ensureOne(root,'revenue');if(typeof installColumnDragResizers==='function')installColumnDragResizers(root)};
const previousPostRender=postRenderV75;postRenderV75=function(){previousPostRender();requestAnimationFrame(()=>window.v290EnsurePlanningColumns(document.getElementById('app')))};
setTimeout(()=>window.v290EnsurePlanningColumns(document.getElementById('app')),1200);
})();
</script>
<!-- V2.90 — ajuste de colunas nas tabelas consolidadas do Planejamento. -->'''

p=Path('index.html')
s=p.read_text(encoding='utf-8')
if 'versão 2.89' not in s and 'versão 2.90' not in s:
    raise SystemExit('Unexpected index version')
s=s.replace('versão 2.89','versão 2.90',1)
if 'id="v290-planning-consolidated-columns-style"' not in s:
    s=s.replace('</body>', STYLE+'\n'+SCRIPT+'\n</body>')
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
w=sw.read_text(encoding='utf-8').replace('financas-cn-v252','financas-cn-v253')
sw.write_text(w,encoding='utf-8')
