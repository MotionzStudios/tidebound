# Publishing Tidebound to the stores

Checked against Google's and Apple's pages in October 2026. Policies change, so re-check the linked pages before you submit.

## Google Play (do this first, it is cheaper and faster)
1. **Developer account**: one-time registration fee (about 25 USD) plus identity verification, at play.google.com/console.
2. **New personal accounts need a closed test first**: accounts created after 13 Nov 2023 must run a closed test with at least
   12 testers who stay opted in for 14 days in a row before you can apply for production access. Start recruiting testers
   (friends, family, a Discord) as soon as the first build is uploaded. Organisation accounts have different rules.
3. **Build target**: since 31 Aug 2026 new apps and updates must target Android 16 (API 36). Use the newest Capacitor release
   (`package.json` already says "latest"), then open `android/variables.gradle` after `npx cap add android` and confirm
   `targetSdkVersion = 36` and `compileSdkVersion = 36`.
4. **Upload an Android App Bundle (.aab), not an .apk**: `cd android && ./gradlew bundleRelease`, signed with your own
   upload key (Android Studio: Build > Generate Signed Bundle). Keep the keystore and its password safe forever.
5. **Store listing**: app name, short description (80 chars), full description, 512x512 icon, 1024x500 feature graphic,
   at least 2 phone screenshots (use the photo mode or screenshots from the game), category "Casual" or "Simulation".
6. **Policy forms**: privacy policy URL (see PRIVACY.md, host it as a web page), Data safety form (the game collects nothing
   and has no ads: answer "no data collected"), content rating questionnaire (expect an all-ages rating), target audience
   (choose 13+ or all ages carefully: choosing under-13 triggers the Families policy), ads declaration (none).
7. Release to closed testing, wait the 14 days, apply for production, then roll out.

## Apple App Store (later, needs more effort)
- **Apple Developer Program**: 99 USD per year. Verification takes hours for individuals.
- **You need a Mac with Xcode** (or a cloud build service) to produce the iOS build: `npx cap add ios`, `npx cap sync ios`,
  archive in Xcode, upload to App Store Connect, test with TestFlight, then submit.
- **Guideline 4.2 (minimum functionality)**: Apple rejects apps that are "just a website in a shell". A game with its own
  gameplay is a good case, but add a few native touches to be safe: Capacitor Haptics, the native Share sheet for the photo
  mode, and local notifications ("your aquarium is full", "daily reward ready").
- Also needed: privacy policy URL, App Privacy answers, screenshots for the required iPhone sizes, age rating.

## Before you submit (both stores)
- Test on a real phone: touch targets, rotation lock (portrait), back-button behaviour, airplane mode.
- Add the app name, version and a support email to the listing.
- Money later: digital items sold inside the app must use Google Play Billing / Apple In-App Purchase. Both stores take a cut.
  Keep purchases cosmetic or convenience-only (looks, extra aquarium slots, ad-free) so the game stays fair.
- Saves are stored on the device only. If the player uninstalls, progress is lost. Cloud saves would need an online account.
