# How to Capture Screenshots

## Method 0: the script (recommended)

`scripts/capture_screenshots.py` drives Chromium through Playwright and writes both the view
screenshots and the per-template crops, at `deviceScaleFactor=2`. It authenticates with a
long-lived access token, and can relay through an SSH host when the machine running it has no
route to Home Assistant. Read its docstring for the environment variables; the component part
is documented at the bottom of this page.

```bash
pip install playwright && playwright install chromium
HA_URL=http://homeassistant.local:8123 python3 scripts/capture_screenshots.py
```

The methods below are the manual fallbacks, for a one-off shot or an instance the script
can't reach.

## Method 1: Browser DevTools

### Desktop Screenshots (1920x1080)
1. Open your HA dashboard in Chrome/Edge
2. Press `F12` to open DevTools
3. Press `Ctrl+Shift+M` to toggle device toolbar
4. Set dimensions to `1920 x 1080`
5. Navigate to each view and capture:

| View | URL Path | Filename |
|------|----------|----------|
| Home | `/lovelace/0` | `home-desktop.png` |
| Meteo | `/lovelace/1` | `meteo-desktop.png` |
| Remote | `/lovelace/2` | `remote-desktop.png` |
| Programmation | `/lovelace/3` | `programmation-desktop.png` |

6. For each view: click the `...` menu in DevTools device toolbar → "Capture screenshot"

### Mobile Screenshots (390x844)
1. Same DevTools device toolbar
2. Set dimensions to `390 x 844` (iPhone 14 Pro)
3. Capture each view with `-mobile.png` suffix

## Method 2: One-Click Console Script

Paste this in browser console (F12 → Console) while on your dashboard:

```javascript
// Auto-capture all views
(async () => {
  const views = [
    { path: '/lovelace/0', name: 'home' },
    { path: '/lovelace/1', name: 'meteo' },
    { path: '/lovelace/2', name: 'remote' },
    { path: '/lovelace/3', name: 'programmation' },
    { path: '/lovelace/4', name: 'proxmox' },
    { path: '/lovelace/5', name: 'routeurs' },
    { path: '/lovelace/6', name: 'nas' },
  ];
  
  for (const view of views) {
    window.location.pathname = view.path;
    await new Promise(r => setTimeout(r, 3000)); // Wait for render
    
    // Use html2canvas if available, otherwise prompt manual capture
    console.log(`Ready to capture: ${view.name}`);
    console.log(`Save as: docs/screenshots/${view.name}-desktop.png`);
    await new Promise(r => setTimeout(r, 1000));
  }
  console.log('Done! Capture each view using DevTools screenshot tool.');
})();
```

## Method 3: iOS/Android

For the most authentic mobile screenshots:
1. Open HA companion app or browser
2. Navigate to each view
3. Take a standard screenshot (Power + Volume or swipe gesture)
4. Crop to remove status bar if desired

## Where to Save

Place all screenshots in:
```
~/ha-glass-dashboard/docs/screenshots/
```

### Required for README

The script names files `<view>-desktop.png` / `<view>-mobile.png` after `HA_VIEWS`, and the
README links `home-view.jpg`, `weather-view.jpg`, `remote-view.jpg` and `home-mobile.jpg` —
full-view shots are committed as JPEG because a 2x PNG of a photographic background weighs
around 9 MB. Downscale the 2x capture to 1920 wide and save at quality 90.

The mobile shot has to show a view that is taller than the phone, and `full_page=True` is the
wrong way to get it: the theme paints its background with `background-attachment: fixed`,
which Chromium only paints over one window's worth of height, so everything a full-page
capture adds below that comes back **white** — the shot ends up split in two. The script grows
the window to the height of the document instead (`grow_to_page`) and takes an ordinary
capture. Check the bottom row of pixels of any new mobile shot: white there means the fix was
bypassed, not that the dashboard ends.

## Component Crops (`docs/screenshots/components/`)

The per-template close-ups used in the README's *Template Reference* are captured by the same
script, one file per template, each cropped **by the browser from the card element itself**:

```bash
HA_URL=http://home.home.arpa HA_SSH_RELAY=root@node1.home.arpa \
HA_SSH_TARGET=192.168.4.50:80 HA_COMPONENTS=1 HA_VIEWS_ONLY=0 \
python3 scripts/capture_screenshots.py

# un seul composant
HA_ONLY="state_on_off_on state_on_off_off" ... python3 scripts/capture_screenshots.py
```

There are no coordinates to re-measure: the `COMPONENTS` list at the top of the script maps a
name to a locator, and `pick` says which match to keep (`smallest` = the card itself,
`largest` = the row it sits in, `union` = clip to a set of elements, `index` = position,
`badge` = one circle in the view header, matched on `entity` instead of a locator).

Things worth knowing before touching that list:

- **A `:has-text()` selector also matches every ancestor** containing the text, plus inner
  labels — hence `pick`. `inner_text()` is empty on `button-card` (content lives in shadow
  DOM), but `:has-text()` sees through it.
- **Text must be unique enough.** `button-card:has-text("Garage")` matched a label inside a
  sensor card; scoping it to the covers row (`hui-card:has(button-card:has-text("Baie vitr"))`)
  fixed it. The same applies to `Cuisine`, which appears in both the lamp row and the covers.
- **A card whose own template gives it a class is easier to find than one with text.**
  `battery_rack` is matched by `hui-card:has(.batt-grid)`: `:has()` sees through the shadow
  root, and that class comes from the template's `extra_styles`, so it moves with the card
  instead of with a label someone may rename.
- **The remote panel is not a card** but eleven stacked `hui-grid-card` rows, so it uses
  `union` — the frame is centred on the grid by construction.
- **The device row has no text at all** (icons only) and is the one entry addressed by
  `index`; a layout change will silently point it at another card.
- **Some components drive real devices.** `state_on_off_on` / `_off` toggle `HA_LAMP_ENTITY`;
  the three cover shots drive `HA_COVER_ENTITY` through one open/close cycle. Every entity is
  snapshotted the first time it is touched and restored in a `finally`, including when a
  capture raises.
- **Waiting for "not moving" is not enough** to know a cover arrived: it still reports its old
  state a second or two after the command, so the first poll returns immediately. Wait for the
  position itself — the first version of this reported a restore that had not happened yet.
- **The moving state needs the page loaded *before* the command.** The dashboard follows the
  state live, so reloading after starting the shutter would burn the whole travel inside
  `HA_SETTLE_MS`. `glass_cover_moving` is captured as a GIF (`frames` / `interval_ms`).
- **The theme background follows a weather entity, not the sun.** `weather.marseille` and
  `weather.senas` stay on `clear-night` for about an hour and a half after sunrise: capture too
  early and the glass sits on a night sky.

Badges (`pick: "badge"`) have three quirks of their own:

- **Nothing in the markup tells them apart** — every one of them is a `hui-badge` holding the
  same 36 px circle — so they are matched on the `entity` of their card configuration.
- **Their indicators are drawn outside the circle** (a countdown at `left: -6px`, a power
  reading at `right: -6px`), where an element screenshot would cut them off, and the next badge
  is only 8 px away, close enough to show up in the margin. So the shot masks the other badges
  and clips the union of the circle and everything the card draws.
- **The mask has to be a CSS rule injected into the shadow root, and it needs a second to
  land.** An inline `style` on the badge does not survive: the header re-renders whenever a
  sensor moves — every second here — and Lit rewrites the attribute right before the capture.
  Worse, even the CSS rule paints late: `getComputedStyle` returns `hidden` immediately, but the
  badges are composited layers (`backdrop-filter`) and the frame still shows them for close to a
  second. Screenshotting straight after masking gives back the neighbours, which looks exactly
  like a mask that never applied — hence `BADGE_REPAINT_MS`.

## After Capturing

```bash
cd ~/ha-glass-dashboard
git add docs/screenshots/
git commit -S -m "docs: refresh dashboard screenshots"
git push
```

The README references `docs/screenshots/` through absolute `raw.githubusercontent.com` URLs on
`main` — deliberately, so the images also render where HACS shows the README out of repo
context. The flip side is that on a branch the preview keeps showing `main`'s images, and any
file added by the branch 404s until it is merged. Review new images by their raw URL pinned to
the commit, not through the README preview.
