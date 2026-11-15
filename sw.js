// Keeps the app working offline: serve from cache, refresh the cache in the background.
const CACHE = "plz-quran-lamp-v3";
const FILES = ["./", "index.html", "manifest.json", "icon.svg", "icon-192.png", "icon-512.png", "times.json"];

self.addEventListener("install", (e) => e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FILES)).then(() => self.skipWaiting())));
self.addEventListener("activate", (e) => e.waitUntil(self.clients.claim()));
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  e.respondWith(caches.open(CACHE).then(async (c) => {
    const key = e.request.url.split("?")[0];
    const fresh = fetch(e.request).then((r) => { if (r.ok) c.put(key, r.clone()); return r; }).catch(() => null);
    return (await fresh) || (await c.match(key)) || Response.error();
  }));
});
