const CACHE_NAME = 'spellcasting-v1';
const urlsToCache = [
  '/',
  '/login/',
  '/register/',
  '/static/bee/images/192.png',
  '/static/bee/images/512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[Service Worker] Pre-caching critical assets safely');
        return cache.addAll(urlsToCache);
      })
      .catch(err => console.error('[Service Worker] Cache addAll crashed due to a missing asset file path:', err))
  );
});


self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          if (cache !== CACHE_NAME) {
            console.log('[Service Worker] Clearing legacy application shell cache stores');
            return caches.delete(cache);
          }
        })
      );
    })
  );
});

// Fetch stage: network fallback strategies
self.addEventListener('fetch', event => {
  
  if (event.request.method !== 'GET') {
      return; 
  }

  const url = new URL(event.request.url);
  if (url.pathname.startsWith('/login/') || url.pathname.startsWith('/logout/') || url.pathname.startsWith('/register/')) {
      event.respondWith(fetch(event.request));
      return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
