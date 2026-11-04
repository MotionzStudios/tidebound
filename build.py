# Builds www/ from ../web/index.html (run: python3 build.py)
import re, os
from PIL import Image, ImageDraw
src = open("../web/index.html" if os.path.exists("../web/index.html") else "web/index.html").read()
import json
_mc = json.load(open("monetization.json")) if os.path.exists("monetization.json") else None
src = src.replace("/*__MONEY__*/ null", json.dumps(_mc) if _mc else "null")
head = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no">
<meta name="theme-color" content="#0b3b63"><meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="Tidebound">
<link rel="manifest" href="manifest.webmanifest"><link rel="icon" href="icons/icon-192.png"><link rel="apple-touch-icon" href="icons/icon-192.png">
'''
sw = '''<script>
// The apps load everything from local files, so no offline cache is needed. Remove any old one.
try {
  if ("serviceWorker" in navigator) navigator.serviceWorker.getRegistrations().then(rs => rs.forEach(r => r.unregister())).catch(() => {});
  if (window.caches) caches.keys().then(ks => ks.forEach(k => caches.delete(k))).catch(() => {});
} catch (e) {}
</script>
'''
html = head + src + sw + "</html>\n"
os.makedirs("www/icons", exist_ok=True)
open("www/index.html", "w").write(html)
from icongen import make
def icon(n, pad): return make(n).convert("RGB")
def grad(n):
    im = Image.new("RGB", (n, n)); d = ImageDraw.Draw(im)
    for y in range(n):
        k = y / n; d.line([(0, y), (n, y)], fill=(int(30 + (8 - 30) * k), int(150 + (42 - 150) * k), int(190 + (86 - 190) * k)))
    return im
os.makedirs("assets", exist_ok=True); icon(1024, 0.18).save("assets/icon-only.png"); make(1024, 0.66, True).save("assets/icon-foreground.png"); grad(1024).save("assets/icon-background.png"); make(1024, 0.7).convert("RGB").save("assets/splash.png"); make(1024, 0.7).convert("RGB").save("assets/splash-dark.png")
icon(192, 0.18).save("www/icons/icon-192.png"); icon(512, 0.18).save("www/icons/icon-512.png"); make(512, 0.8).convert("RGB").save("www/icons/icon-maskable-512.png")
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
open("www/sw.js", "w").write('''// Kill switch: replaces the old cache-first worker, clears its caches, unregisters itself and reloads the page.
self.addEventListener("install", e => { self.skipWaiting(); });
self.addEventListener("activate", e => { e.waitUntil((async () => {
  try { const ks = await caches.keys(); await Promise.all(ks.map(k => caches.delete(k))); } catch (err) {}
  try { await self.registration.unregister(); } catch (err) {}
  try { const cs = await self.clients.matchAll({type: "window", includeUncontrolled: true}); cs.forEach(c => { try { c.navigate(c.url); } catch (err) {} }); } catch (err) {}
})()); });
''')
print("built", len(html))
