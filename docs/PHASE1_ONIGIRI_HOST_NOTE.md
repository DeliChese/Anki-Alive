# Phase 1 Deck Browser Compatibility Finding

Status: FIX IMPLEMENTED, HOST RE-VALIDATION REQUIRED
Date: 2026-08-19

Real-host inspection with the Onigiri add-on exposed a structural compatibility problem: embedding the full Anki Alive Today surface directly into Anki's Deck Browser competes with appearance/dashboard add-ons that legitimately customize the same host DOM.

Phase 1 now follows a compatibility-first boundary:

- Anki Alive does not inject Today into Deck Browser content.
- The native Deck Browser remains owned by Anki and other installed add-ons.
- Native Decks / Add / Browse / Stats / Sync flows remain available without Anki Alive reimplementing them.
- Anki Alive Today opens in a dedicated modeless AnkiWebView window.
- Today is reachable from an `Alive` top-toolbar entry outside active review and from `Tools > Anki Alive Today` as a fallback.
- The reviewer progress strip remains a small reviewer-only augmentation.
- Expedition completion exits active recall and opens the dedicated Today window for closure.

This finding supersedes the earlier Phase 1 implementation note that described Deck Browser augmentation as the Today host surface.

Host re-validation must confirm coexistence with Onigiri and with normal Anki Deck Browser behavior before Phase 1 closes.
