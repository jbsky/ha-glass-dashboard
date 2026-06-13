# Community Posts - Glass Dynamic Dashboard

## 1. Home Assistant Community Forum
**Category**: Share your Projects!
**URL**: https://community.home-assistant.io/c/share-your-projects/34

### Title:
Glass Dynamic Dashboard - Weather-reactive glass-morphism theme + 33 button-card templates

### Body:

Hey everyone!

I've been working on my dashboard for a while and decided to open-source the result. It's a **glass-morphism theme** with **weather-reactive backgrounds** and a complete **button-card template library**.

### What it does

The background changes automatically with your local weather (15 conditions) and detects day/night. All cards get a frosted glass look via card-mod. And I'm sharing 33 button-card templates as reusable components.

### Key components

- **`glass_climate`** - Full HVAC widget (power, current temp, target up/down, status, secondary sensors)
- **`glass_cover`** - Animated shutter/blind control with position badge
- **`glass_garage`** - Garage door with state
- **`remote_button`** - Compact colored button grid for IR remotes
- **`field_graph`** - Embedded mini-graph-card with glass styling

### What makes it different from existing themes?

| Feature | Frosted Glass | This |
|---------|:---:|:---:|
| Dynamic weather backgrounds | No | 15 conditions + night |
| Button-card template pack | No | 33 templates |
| Self-contained components | No | Climate, Cover, Garage widgets |
| Remote control layout | No | Compact 4-col mobile grid |

### Links

- **GitHub**: https://github.com/jbsky/ha-glass-dashboard
- **HACS**: Add as custom repository (Theme category)

### Requirements
- card-mod
- button-card
- A weather integration

### Installation
Add via HACS custom repository or copy files manually. Full instructions in the README.

I'm based in Provence, France - the included background photos are Mediterranean-themed but you can easily swap them with photos from your own area.

Feedback and contributions welcome!

---

## 2. Reddit r/homeassistant
**URL**: https://www.reddit.com/r/homeassistant/

### Title:
[Share] Glass Dynamic Dashboard - Weather-reactive theme + 33 button-card templates (open source)

### Body:

Open-sourced my glass-morphism dashboard setup. The background changes with weather (15 conditions, day/night aware) and I'm sharing 33 button-card templates as reusable components.

**Highlights:**
- Weather-reactive backgrounds (sunny, rainy, snowy, foggy, etc.)
- Glass-morphism on all cards (backdrop-filter blur via card-mod)
- `glass_climate` — full HVAC widget in one template call
- `glass_cover` — animated shutter control
- `remote_button` — compact IR remote grid for mobile
- `field_graph` — embedded mini-graph with glass style
- 15 curated Mediterranean background photos included
- HACS compatible

**Requires:** card-mod + button-card + any weather integration

**GitHub:** https://github.com/jbsky/ha-glass-dashboard

MIT licensed. Background photos are Unsplash (free). Feedback welcome.

---

## 3. Reddit r/homeautomation
**URL**: https://www.reddit.com/r/homeautomation/

### Title:
Made a weather-reactive glass dashboard theme for Home Assistant (open source, 33 templates)

### Body:

Same as r/homeassistant post above.

---

## 4. HACS Default Repository Submission
**URL**: https://github.com/hacs/default/pulls

### Steps:
1. Go to https://github.com/hacs/default
2. Open `theme` file
3. Add `"jbsky/ha-glass-dashboard"` in alphabetical order
4. Create PR with title: "Add Glass Dynamic Dashboard theme"

### PR Description:
```
## Repository: jbsky/ha-glass-dashboard

### Description
Glass-morphism theme for Home Assistant with weather-reactive backgrounds (15 conditions, sun-aware) and 33 button-card templates as reusable components.

### Checklist
- [x] The repository has a description
- [x] The repository has topics set
- [x] The repository has a release with a tag
- [x] The repository has a hacs.json file
- [x] The repository is not a fork
- [x] The repository is not archived
- [x] The theme file exists in the expected location
```

---

## 5. Twitter/X (optional)
### Text:
Released my glass-morphism dashboard for Home Assistant. Weather-reactive backgrounds (15 conditions), 33 button-card templates, HACS compatible.

https://github.com/jbsky/ha-glass-dashboard

#HomeAssistant #SmartHome #HACS #OpenSource
