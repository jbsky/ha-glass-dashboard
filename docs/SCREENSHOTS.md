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

## After Capturing

```bash
cd ~/ha-glass-dashboard
git add docs/screenshots/
git commit -S -m "docs: add dashboard screenshots"
git push origin main
```

Then update the README image references (they already point to `docs/screenshots/`).
