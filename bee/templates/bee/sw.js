const CACHE_NAME = 'spellcasting-v1';
const urlsToCache = [
  '/',
  '/login/',
  '/register/',
  '/static/bee/intro.mp4',
  '/static/bee/bg-spellcasting.jpg' // FIXED: Point to the actual .jpg file
];

// Install stage: precache system assets
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

// Activation stage: clear legacy systems
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
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
