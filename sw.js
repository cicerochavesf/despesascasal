const CACHE_NAME='financas-cn-v20261102';
const APP_SHELL=['./','./index.html','./icon-192.png','./icon-512.png','./maskable-512.png'];

self.addEventListener('install',event=>{
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache=>cache.addAll(APP_SHELL))
      .then(()=>self.skipWaiting())
  );
});

self.addEventListener('activate',event=>{
  event.waitUntil(
    caches.keys()
      .then(keys=>Promise.all(keys.filter(key=>key!==CACHE_NAME).map(key=>caches.delete(key))))
      .then(()=>self.clients.claim())
  );
});

self.addEventListener('fetch',event=>{
  const request=event.request;
  if(request.method!=='GET')return;

  const url=new URL(request.url);
  if(url.hostname.includes('supabase.co')||url.hostname.includes('jsdelivr.net'))return;

  // O manifesto sempre tenta buscar a versão publicada mais recente.
  if(url.origin===self.location.origin&&url.pathname.endsWith('/manifest.webmanifest')){
    event.respondWith(
      fetch(request,{cache:'no-store'})
        .then(response=>{
          if(response&&response.ok){
            const copy=response.clone();
            caches.open(CACHE_NAME).then(cache=>cache.put(request,copy));
          }
          return response;
        })
        .catch(()=>caches.match(request))
    );
    return;
  }

  // Navegações usam a rede primeiro para evitar abrir uma versão antiga do app.
  if(request.mode==='navigate'){
    event.respondWith(
      fetch(request,{cache:'no-store'})
        .then(response=>{
          if(response&&response.ok){
            const copy=response.clone();
            const cachePromise=caches.open(CACHE_NAME).then(cache=>
              Promise.all([cache.put('./',copy.clone()),cache.put('./index.html',copy.clone())])
            );
            event.waitUntil(cachePromise);
          }
          return response;
        })
        .catch(()=>caches.match('./').then(r=>r||caches.match('./index.html')))
    );
    return;
  }

  // Recursos locais usam cache, com atualização em segundo plano quando possível.
  if(url.origin===self.location.origin){
    event.respondWith(
      caches.match(request).then(cached=>{
        const network=fetch(request).then(response=>{
          if(response&&response.ok){
            const copy=response.clone();
            caches.open(CACHE_NAME).then(cache=>cache.put(request,copy));
          }
          return response;
        }).catch(error=>{
          if(cached)return cached;
          throw error;
        });
        return cached||network;
      })
    );
  }
});
