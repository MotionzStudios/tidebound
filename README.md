# Tidebound: Android packaging

The game is one HTML file (`../web/index.html`). `python3 build.py` wraps it into `www/` with a manifest,
icons and an offline service worker. From there there are two routes to an Android app.

## Route A (fastest): install as an app, no APK
1. Put the contents of `www/` on any HTTPS host (GitHub Pages, Netlify, Cloudflare Pages: all free).
2. Open the URL in Chrome on the phone, menu, "Install app" (or "Add to Home screen").
It runs fullscreen with its own icon and works offline after the first load.

## Route B: a real APK (Capacitor)
Needs a computer with Node 18+, JDK 17 and Android Studio (or just the Android SDK command-line tools).
```
npm install
npx cap add android          # first time only
python3 build.py
npx cap sync android
cd android && ./gradlew assembleDebug
```
The APK appears at `android/app/build/outputs/apk/debug/app-debug.apk`. Copy it to the phone and open it
(allow "install unknown apps"). For the Play Store build a signed release bundle instead:
`./gradlew bundleRelease` after creating a keystore (Android Studio: Build, Generate Signed Bundle).

Alternative without any tooling: upload the hosted URL from Route A to https://www.pwabuilder.com and
choose Android; it produces a signed package for you.

## Reminders (push-style notifications)
The game schedules local notifications (aquarium full, daily reward ready, new quests, a comeback nudge) when the app goes to
the background. They only work in the installed Android/iOS app, through the `@capacitor/local-notifications` plugin that is
already listed in `package.json`: run `npm install` and `npx cap sync android`. On Android 13+ the game asks for permission
when the player switches Reminders on in the Awards screen. The setting can be turned off there.

## Notes
- Saves live in the app's localStorage, so they stay on that device (and survive updates).
- The Baloo 2 font is fetched from Google Fonts on first launch and then cached for offline use. To make it
  fully offline, download the font files into `www/fonts/` and point an `@font-face` at them.
- Adding real-money purchases later means using Google Play Billing (a Capacitor billing plugin), plus a
  Play Console account. Keep purchases cosmetic or convenience-only to avoid pay-to-win.
