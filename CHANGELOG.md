# Changelog

Worth-noting changes only. The version in `package.json` and `versionName` in
`android/app/build.gradle` move together; tags are `v1.2.3`.

## 1.1.0 — 2026-11-15

- Pull to refresh: grab the board at the top and drag down; let go and
  it refetches
- Refresh and Settings now live in a bottom bar where one thumb can
  reach them; the top bar is just the title
- Appearance (light / dark / match the system) is in Settings, not in
  the top bar
- Builds now sign with a fixed debug key, so this update installs
  directly over 1.0.0

## 1.0.0 — 2026-11-15

First release.

- Live Elizabeth line departures between Tottenham Court Road and Hayes & Harlington,
  straight from the TfL API, no account and no tracking.
- Says which trains actually call at the other station by working out the line's stop
  graph from TfL's own route data, instead of guessing from a destination name.
- Two big direction buttons, a countdown for the next one, the rest below, readable at
  arm's length in sun or at 2 a.m.
- Android app: opens on the board for whichever of the two stations you are standing at.
  Foreground location only, one permission, and a direction you tap always wins.
- Same `web/index.html` still works on its own as a web page, on desktop or from disk.
