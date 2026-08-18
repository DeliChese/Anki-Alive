# Phase 0 Manual Anki Validation

Status: PENDING REAL HOST RUN

This checklist is intentionally written for a low-friction local test. The goal is to validate Anki Alive inside a real Anki desktop runtime without requiring Git or Python expertise.

## One-time dev link setup on Windows

1. Pull the latest `phase-0/foundation` branch in VS Code.
2. Close Anki completely.
3. Open the VS Code terminal in the Anki Alive repository.
4. Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\link_dev_addon.ps1
```

The script creates this development link:

```text
%APPDATA%\Anki2\addons21\anki_alive_dev
    -> your local Anki Alive repository
```

This is a directory junction, not a copied code folder. After the one-time setup, future Git pulls update the code Anki sees automatically.

## Enable Phase 0 diagnostics

1. Open Anki.
2. Open `Tools -> Add-ons`.
3. Select `anki_alive_dev`.
4. Open Config.
5. Set diagnostics to true:

```json
"diagnostics": {
  "enabled": true
}
```

6. Save and restart Anki.

Diagnostics intentionally contain IDs, ratings, state names, and timings only. Card/note text is excluded by policy and sanitizer.

## Smoke test

Record the Anki version and Windows version, then perform:

1. Start Anki and verify there is no add-on startup error dialog.
2. Open the normal collection/profile.
3. Review at least four cards, preferably using Again, Hard, Good, and Easy at least once each where honest.
4. Confirm normal reviewing still behaves normally.
5. Undo the most recent accepted review once.
6. Continue reviewing one or two cards.
7. Close Anki normally.
8. Start Anki again and review one more card.

Do not press a higher answer button merely for the test. Honest grading remains the product rule.

## Evidence file

After the run, collect:

```text
%APPDATA%\Anki2\logs\addons\anki_alive_dev\anki_alive_dev.log
```

Expected diagnostic event names include:

```text
bootstrap_complete
review_observation
review_reversed
performance_sample
```

For review-hook samples the important timing name is:

```text
reviewer_did_answer_card
```

For undo samples:

```text
state_did_undo
```

## Pass criteria

The real-host Phase 0 gate passes when:

- Anki starts without an Anki Alive error,
- accepted reviews generate `review_observation`,
- an unrelated/no-op condition does not create a false reversal,
- undoing the tracked review generates `review_reversed`,
- restarting Anki does not corrupt storage or settings,
- normal review behavior remains unaffected,
- database integrity remains true at bootstrap,
- reviewer hook timing is recorded,
- measured reviewer cost is acceptable against the Phase 0 budget.

Provisional synchronous reviewer budget:

```text
Preferred < 5 ms
Typical < 10 ms
P95 < 20 ms
```

## After validation

Attach or paste the log into the project chat. The Phase 0 handoff should then be updated with:

- exact Anki version,
- OS,
- manual smoke result,
- reviewer timing evidence,
- any host-specific issue,
- final Phase 0 PASS/BLOCKED status.
