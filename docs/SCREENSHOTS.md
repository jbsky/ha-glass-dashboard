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

### Required for README (minimum 3):
- `home-desktop.png` — Main view with weather background (the hero image)
- `home-mobile.png` — Same view on mobile
- `remote-mobile.png` — Remote control on mobile (shows compact layout)

### Nice to have:
- `meteo-desktop.png` — Weather badges view
- `programmation-desktop.png` — Clean scheduler view
- `home-night.png` — Night mode (capture after sunset or change sun entity)

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
`largest` = the row it sits in, `union` = clip to a set of elements, `index` = position).

Things worth knowing before touching that list:

- **A `:has-text()` selector also matches every ancestor** containing the text, plus inner
  labels — hence `pick`. `inner_text()` is empty on `button-card` (content lives in shadow
  DOM), but `:has-text()` sees through it.
- **Text must be unique enough.** `button-card:has-text("Garage")` matched a label inside a
  sensor card; scoping it to the covers row (`hui-card:has(button-card:has-text("Baie vitr"))`)
  fixed it. The same applies to `Cuisine`, which appears in both the lamp row and the covers.
- **The remote panel is not a card** but eleven stacked `hui-grid-card` rows, so it uses
  `union` — the frame is centred on the grid by construction.
- **The device row has no text at all** (icons only) and is the one entry addressed by
  `index`; a layout change will silently point it at another card.
- **`state_on_off_on` / `_off` drive a real switch** (`HA_LAMP_ENTITY`, default
  `switch.lumiere_wc`). The script records the state it found, sets what it needs, and puts it
  back — including when a capture raises.
- **The theme background follows a weather entity, not the sun.** `weather.marseille` and
  `weather.senas` stay on `clear-night` for about an hour and a half after sunrise: capture too
  early and the glass sits on a night sky.
