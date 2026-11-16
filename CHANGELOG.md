# Changelog

Worth-noting changes only. The version in `package.json` and `versionName` in
`android/app/build.gradle` move together; tags are the version with a `v` in front.

## 1.5.9 — 2026-11-16

Settings floats again, and only steps aside while you scroll

- The Settings button is a floating one again at the bottom right: it stays put at rest,
  including at the very top of the board, and while you scroll it slips out of the way
  so the last visible row's detail is never hidden behind it — then returns the moment
  scrolling stops
- It does not slip away while a sheet is open, or during a pull-to-refresh
- The page no longer keeps a whole empty 96 px band for the button underneath; the
  footer's own controls clear it instead, so nothing is permanently unreachable
- Its outline has more contrast on both appearances now that it floats over the page


Docked Settings button, a thumb-sized switch box, and short screens that show departures

- The Settings button is docked in the footer, next to the status line: always in reach,
  never on top of a departure row or the location line at rest, and no longer costing the
  page a reserved band of empty space at the bottom
- Every settings toggle row is now a label: tapping anywhere on it flips the switch
  once, in either direction, and the pill has a 44 px touch box while staying its size
- The "All good" pill, which opens the status sheet, is a 44 px button
- On short screens the glance still leads but the "via" disclosure and chip band tuck
  in two steps, so the first departures stay above the fold (all four fit at 412×892)
- The list header tightens and wraps cleanly, and the journey card keeps its spacing
- The Settings button's outline now reads as a control in both appearances, with the
  light-mode edge lifted to 3:1 and the dark one kept at 3:1


- Dropped the "Direct · no changes" fact pill from the journey card: it was a
  hardcoded constant (every offered train on a single-line board is direct by
  construction) dressed up as a computed fact; the real facts — trains in the
  next hour, usual platform, sample-data warning — stay

## 1.5.6 — 2026-11-16

- Line status rebuilt around one gesture: a new problem shows as a card whose whole body
  is tappable and opens a proper sheet with the complete, unbroken description; swiping the
  card away (or tapping its cross) collapses it to a compact severity pill that stays up
  top and reopens the sheet on tap; the card returns automatically when the status changes
- The "Read the rest" split dropped characters (off-by-one on the ellipsis — "As we deal"
  arrived as "e we deal"); the preview is now a CSS line-clamp over the whole text and the
  sheet carries it in one piece
- Good service and the dismissed pill are real buttons (Enter/Space work); the sheet joins
  the back/Escape close chain and the drag-down-to-close family

## 1.5.5 — 2026-11-16

- The station picker is a single combobox: the box itself shows the current
  station; tapping it drops the full list (current pick highlighted and
  scrolled into view, list scrolls); typing narrows it live; one tap picks,
  saves and leaves the name in the box; walking away mid-type restores the
  current name
- The redundant second control — the native dropdown and its system popup —
  is gone from Settings and first-run setup. Its select element stays in the
  page, invisible, as the stored value and the change-event carrier
- README: the picker is described as it now behaves

## 1.5.4 — 2026-11-16

- Late trains are named: the app keeps a ledger of TfL's first prediction per train
  and, when it slips by 90 seconds or more, marks the train amber with "+N late"
  on the hero, the list, the route sheet — and says it once for screen readers.
  The baseline survives restarts; a recovered prediction clears the badge
- Each train now also carries the time TfL expects it at the far station, paired
  from the far station's own arrivals feed (same terminus, plausible gap, in
  order); where no pairing is honest, nothing is claimed
- A train older than 75 seconds past its expected time is retired — the "Due"
  hero no longer sits there a minute behind the phone's clock (field report,
  16:01 with a "Due 16:00" card)
- Refresh now fetches both stations' arrival boards in one pass

## 1.5.3 — 2026-11-15

- The board has new edges. Corners are tighter (cards 14px, the big card
  16px, sheets 20px), the big card no longer throws a purple haze across
  the card beneath it, and the cards sit with honest air between them
- The journey card ends where its content ends: less floating space
- Cards rest on their outlines alone — shadows only where something
  actually floats (the buttons and the gear)

## 1.5.2 — 2026-11-15

- Picking a station is one move now: type in the find box and tap a name from
  the list that appears under it. Before, typing quietly filtered a list you
  could not see unless you opened the dropdown
- After an update the app opens with a short "New in X" list instead of
  saying nothing about what changed

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
