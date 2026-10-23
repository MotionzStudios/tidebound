# Builds www/ from ../web/index.html (run: python3 build.py)
import re, os
from PIL import Image, ImageDraw
src = open("../web/index.html" if os.path.exists("../web/index.html") else "web/index.html").read()
head = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no">
<meta name="theme-color" content="#0b3b63"><meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="Tidebound">
<link rel="manifest" href="manifest.webmanifest"><link rel="icon" href="icons/icon-192.png"><link rel="apple-touch-icon" href="icons/icon-192.png">
'''
sw = '''<script>
if ("serviceWorker" in navigator && location.protocol.startsWith("http")) {
  window.addEventListener("load", () => { try { navigator.serviceWorker.register("sw.js"); } catch (e) {} });
}
</script>
'''
html = head + src + sw + "</html>\n"
os.makedirs("www/icons", exist_ok=True)
open("www/index.html", "w").write(html)
def icon(n, pad):
    im = Image.new("RGB", (n, n)); d = ImageDraw.Draw(im)
    for y in range(n):
        k = y / n; d.line([(0, y), (n, y)], fill=(int(43 + (11 - 43) * k), int(143 + (59 - 143) * k), int(184 + (99 - 184) * k)))
    c = n / 2; s = n * (0.5 - pad)
    d.ellipse([c - s, c - s * 0.55, c + s * 0.8, c + s * 0.55], fill=(255, 183, 3))           # body
    d.polygon([(c - s * 0.6, c), (c - s * 1.15, c - s * 0.5), (c - s * 1.15, c + s * 0.5)], fill=(255, 140, 0))  # tail
    d.ellipse([c + s * 0.35, c - s * 0.25, c + s * 0.6, c], fill=(255, 255, 255)); d.ellipse([c + s * 0.45, c - s * 0.17, c + s * 0.55, c - s * 0.05], fill=(16, 34, 47))
    for i in range(3): d.arc([c - s * 0.1 + i * s * 0.25, c - s * 0.4, c + s * 0.3 + i * s * 0.25, c + s * 0.4], 300, 60, fill=(230, 120, 0), width=max(2, n // 70))
    return im
os.makedirs("assets", exist_ok=True); icon(1024, 0.18).save("assets/icon-only.png"); icon(1024, 0.30).save("assets/icon-foreground.png"); Image.new("RGB", (1024, 1024), (24, 100, 142)).save("assets/icon-background.png"); icon(1024, 0.20).save("assets/splash.png"); icon(1024, 0.20).save("assets/splash-dark.png")
icon(192, 0.18).save("www/icons/icon-192.png"); icon(512, 0.18).save("www/icons/icon-512.png"); icon(512, 0.30).save("www/icons/icon-maskable-512.png")
open("www/manifest.webmanifest", "w").write('''{
  "name": "Tidebound", "short_name": "Tidebound", "description": "A fishing game: cast, hook, reel, collect.",
  "start_url": "./index.html", "scope": "./", "display": "fullscreen", "orientation": "portrait",
  "background_color": "#0b3b63", "theme_color": "#0b3b63",
  "icons": [
    {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
    {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
    {"src": "icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
  ]
}
''')
open("www/sw.js", "w").write('''const CACHE = "tidebound-v1";
const CORE = ["./", "./index.html", "./manifest.webmanifest", "./icons/icon-192.png", "./icons/icon-512.png", "./icons/icon-maskable-512.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
// cache-first; also caches the Google font files the first time they load, so the font works offline afterwards
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(caches.match(e.request).then(hit => hit || fetch(e.request).then(res => {
    if (res && (res.ok || res.type === "opaque")) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }
    return res;
  }).catch(() => caches.match("./index.html"))));
});
''')
print("built", len(html))
