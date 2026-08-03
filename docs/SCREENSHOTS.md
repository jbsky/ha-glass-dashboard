# How to Capture Screenshots

## Method 1: Browser DevTools (Recommended)

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

The per-template close-ups used in the README's *Template Reference* are **crops of the
committed full-view captures**, not separate captures:

| Crop | Source | Region |
|------|--------|--------|
| `state_on_off_off.jpg` | `components/state_on_off.jpg` (2× session) | 3rd tile of the device row |
| `state_on_off_on.jpg` | `home-view.jpg` (1×, upscaled ×2) | same tile, entity on |
| `remote_view.jpg` | `remote-view.jpg` | `x 896–1280, y 60–612` (button grid centred) |
| `field_templates.jpg` | left card of `field_templates_pair.jpg` | — |
| `glass_cover_partial.jpg` | `components/glass_covers_row.jpg` | 2nd card (`x 254–508`) |
| `glass_cover_closed.jpg` | `components/glass_covers_row.jpg` | 3rd card (`x 508–762`) |

Gotchas for whoever redoes them:

- The original **2× (`deviceScaleFactor=2`) capture session was never committed** — only its
  crops were. So a crop that is truncated (as `remote_view.jpg` was) can only be redone from
  the 1× full views, at half the pixel density.
- The full views carry **baked-in annotation overlays** (labels, leader lines, a cyan highlight
  rectangle around the remote card). Crop *inside* the highlight stroke, and check for leader
  arrows landing on the UI — one had to be inpainted out of the `Noel` button.
- HA (`home.home.arpa`, 192.168.4.50) is **not reachable from `ansible.home.arpa`** (ports
  22/80/443/8123 all filtered), so live re-capture with the Playwright script below has to run
  from a host on a VLAN that can reach it.
- An on/off pair must be the **same entity**: `home-view.jpg` and `components/state_on_off.jpg`
  come from different sessions and happen to have the 3rd tile in opposite states.
- **No lit lightbulb exists in any committed capture** — the seven-lamp row is off in every one
  of them, so the `state_on_off` pair uses the LED/socket tile instead. If you ever recapture,
  switch one of those lamps on first: a bulb reads as on/off more immediately than an LED.

## After Capturing

```bash
cd ~/ha-glass-dashboard
git add docs/screenshots/
git commit -S -m "docs: add dashboard screenshots"
git push origin main
```

Then update the README image references (they already point to `docs/screenshots/`).
