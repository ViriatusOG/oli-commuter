# Changelog

Worth-noting changes only. The version in `package.json` and `versionName` in
`android/app/build.gradle` move together; tags are the version with a `v` in front.

## 1.5.1 — 2026-11-15

- Fixed: the slim top countdown could sit on screen showing an old time while
  the big card counted down to a different one — its hidden state was ignored,
  so it never hid and never refreshed. It now only appears when the big card
  is off screen, and always shows the same time

## 1.5.0 — 2026-11-15

The UI/UX-review build: the app behaves like an Android app now.

- The back button (and back gesture) closes whatever is open — the route sheet,
  setup, Settings — and only exits the app when there is nothing left to close
- Pull-to-refresh only listens when the board itself is pulled, never through a
  sheet that is open on top of it
- The Settings button steps out of the way while you scroll down, and the footer
  stays on one line
- When the big card scrolls off screen the countdown stays as a slim bar at the
  top; tapping it opens that train's route
- Under ten minutes the countdown reads "6:03 min", not "6 03s"
- The update banner can be dismissed (it comes back for a newer version) and now
  keeps showing the download's progress while it downloads
- Station pickers have a type-to-find box; Settings no longer has two sections
  called "Updates", the API key folds away to one line, "Clear saved data" asks
  for a second tap, and tapping anywhere on a settings row toggles its switch
- Tap targets are thumb-sized everywhere, including banner buttons
- Dark mode: brighter purple text and borders, a settings button you can see,
  and no white flash at launch on a dark phone
- The phone's font size setting is finally honoured
- The route sheet keeps its summary (when, does it stop, which platform) pinned
  and ends with a Done button
- The decorative line above the direction row is gone; it pretended to be a
  slider and did nothing
- The alert actually buzzes now (the app was missing the vibrate permission) and
  honestly says it only fires while the app is on screen
- Setup no longer asks for location on top of itself; it asks just after
- The screen reader is told "due now" once instead of every minute
- With no data the board stops showing a confident journey card under the error

## 1.4.2 — 2026-11-15

- The app is now locked to portrait. Rotating the phone sideways broke the
  layout; the two-column arrangement only appears in wide browser windows
  on a computer

## 1.4.1 — 2026-11-15

- Fixed: "Check for updates" did nothing. The App plugin that tells the app
  which version it is was missing from the build, so the check failed
  silently; the plugin is now in the app and the check says so instead of
  doing nothing
- The version line in Settings now shows the real installed version in the
  app, not "web"

## 1.4.0 — 2026-11-15

- The board now leads with the big next-train card at the top of the screen; the small
  "Next train" bar that said the same thing underneath is gone
- The direction card is now one row — where you are, where the trains go, and a single
  button that flips the direction
- The station setup sheet now appears only on first install; after that your pair is
  changed in Settings, where the fields are labelled Home and Work
- Line status: a small green "All good" pill when the line is fine, amber when there is
  a problem on the line, red with an "on your route" badge when the problem hits your
  two stations

## 1.3.2 — 2026-11-15

- The Settings, setup and train-route sheets can now be dismissed by swiping
  them down (release past a quarter of the way and they go; a small swipe
  springs back). The thin strip of dimmed page above a sheet still closes it
  on a tap
- Settings now shows which version you have under the title, e.g.
  "Oli Commuter 1.3.2 (build 8)"

## 1.3.1 — 2026-11-15

- Fix: the direction hint (which way each journey runs) was only worked out
  while the route data was being fetched, so on a later open of the app that
  used the cached route it fell back to a guess. The stop order is now kept
  with the cached route, so auto-picking your direction works every time,
  even when the route feed is being served from cache or is briefly down.

## 1.3.0 — 2026-11-15

- **In-app updates**: the app now checks the release feed while it is open
  (at most every 12 hours), offers the new version as a banner, downloads it
  with a progress bar and — after verifying the SHA-256 the release
  published — hands it to Android's installer. No browser, no cable, and the
  new version installs straight over the old one
- Settings has an **Updates** section with a manual "check for updates"

## 1.2.0 — 2026-11-15

- **Your two stations**: first run asks where you live and where you work; any pair on the
  line is valid, and either station can be changed in Settings afterwards. The board, the
  journey card and the location logic all follow the pair you pick
- **Tap a train to see its route**: the big one and every row open the stops it serves —
  where it is now, where it came from, the full path with your stations marked. TfL does not
  publish each train's exact stop pattern, so the sheet says so when a semi-direct stops at
  a subset of the route
- The bottom refresh button is gone: refreshing is the pull, and Settings is the single
  floating button at the bottom right

## 1.1.2 — 2026-11-15

- Settings now take a single **API key** (the primary key from your
  subscription at api-portal.tfl.gov.uk). TfL's new portal does not
  use app_id any more, so the two-field layout and its error copy are
  gone; old saved keys are carried over

## 1.1.1 — 2026-11-15

- Registration link in Settings now points at TfL's current portal
  (api-portal.tfl.gov.uk); the old api.tfl.gov.uk address is gone

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
