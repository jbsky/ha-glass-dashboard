# Glass Dynamic Dashboard for Home Assistant

A stunning glass-morphism theme with **weather-reactive backgrounds** and a complete **button-card template library** for Home Assistant.

[![HACS Badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/jbsky/ha-glass-dashboard)](https://github.com/jbsky/ha-glass-dashboard/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## What makes this different?

| Feature | Frosted Glass Theme | Mobile First | **Glass Dynamic** |
|---------|--------------------:|-------------:|------------------:|
| Glass-morphism | Theme only | No | Theme + per-card |
| Dynamic backgrounds | No | No | 15 weather conditions |
| Button-card templates | No | Config dump | 33 reusable templates |
| Sun-aware (day/night) | No | No | Yes |
| Multi-view themes | No | No | Yes (tech, remote) |
| Remote control layout | No | No | Compact 4-col grid |
| Climate component | No | No | Full HVAC widget |

---

## Features

### Weather-Reactive Background
The dashboard background changes automatically based on your local weather — sunny, rainy, stormy, snowy, foggy... with night-time variants when the sun goes below the horizon.

### Glass-Morphism Everywhere
Every card gets a frosted glass effect via `card-mod`:
- `backdrop-filter: blur(12px)` for the glass effect
- Semi-transparent dark background
- Subtle light borders
- Consistent across all card types

### 33 Button-Card Templates
A complete template library organized by function:

| Category | Templates | Purpose |
|----------|-----------|---------|
| **Core Glass** | `glass_button`, `glass_container`, `glass_button_base` | Base glass cards |
| **Components** | `glass_climate`, `glass_cover`, `glass_garage` | Full device widgets |
| **Fields** | `field_command`, `field_graph`, `field_title`, `field_secondary` | Card sub-components |
| **States** | `state_on_off`, `animation_effects` | Visual state feedback |
| **Sensors** | `battery_level`, `humidity_template`, `temperature_template` | Sensor display |
| **Remote** | `remote_button`, `remote_separator` | IR/RF remote grid |
| **Badges** | `badge_base`, `badge_status` | Status indicators |

### Climate Widget (`glass_climate`)
A self-contained HVAC component with:
- Power button with state coloring
- Current temperature display
- Target temperature up/down controls
- Status text (heating/cooling/idle)
- Optional secondary sensors (air quality, fan control)

```yaml
type: custom:button-card
template: glass_climate
variables:
  climate_entity: climate.living_room
  secondary_sensors:
    - sensor.air_quality_pm25
    - input_boolean.fan_control
```

### Cover Widget (`glass_cover`)
Animated shutter/blind control:
- Position badge — `fermé`, `ouvert`, or the current percentage
- Icon, color and left border follow the position; pulsing icon while moving
- Tap to toggle, hold for more-info

### Remote Control Layout
Compact colored button grid for IR/RF remotes:
- 4-column layout, physically compact (380px max-width)
- Colored buttons with customizable backgrounds
- Works great on mobile as a dedicated panel view

---

## Screenshots

| Home | Weather | Remote |
|:---:|:---:|:---:|
| ![home](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/home-view.jpg) | ![weather](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/weather-view.jpg) | ![remote](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/remote-view.jpg) |

<details>
<summary>Mobile view</summary>

![mobile](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/home-mobile.jpg)

</details>

---

## Installation

### HACS (Recommended)

1. Open HACS in your HA instance
2. Click the 3-dot menu → **Custom repositories**
3. Add `https://github.com/jbsky/ha-glass-dashboard` with category **Theme**
4. Install "Glass Dynamic Dashboard"
5. Restart Home Assistant

### Manual Installation

1. Copy `themes/glass-dynamic/` to your `/config/themes/` directory
2. Copy background images from `backgrounds/weather/` to `/config/www/backgrounds/weather/`
3. Add templates from `templates/` to your lovelace `button_card_templates`
4. Restart Home Assistant

---

## Configuration

### 1. Theme Setup

In your `configuration.yaml`:
```yaml
frontend:
  themes: !include_dir_merge_named themes
```

### 2. Weather Entity

Edit `themes/glass-dynamic/glass-dynamic.yaml` and replace `weather.home` with your weather entity:
```yaml
# Find and replace all occurrences of:
weather.home
# With your entity, e.g.:
weather.my_city
```

### 3. Background Images

Place the 15 weather images in `/config/www/backgrounds/weather/`:
```
clearnight.jpg    cloudy.jpg        exceptional.jpg
fog.jpg           hail.jpg          lightning.jpg
lightningrainy.jpg  partlycloudy.jpg  pouring.jpg
rainy.jpg         snowy.jpg         snowyrainy.jpg
sunny.jpg         windy.jpg         windyvariant.jpg
```

See [backgrounds/README.md](backgrounds/README.md) for sourcing guidelines.

### 4. Button-Card Templates

Add templates to your dashboard. In the raw config editor:

```yaml
button_card_templates:
  # Paste contents of templates/glass-core.yaml here
  glass_button_base:
    ...
```

Or use [decluttering-card](https://github.com/custom-cards/decluttering-card) for template management.

---

## Requirements

- [card-mod](https://github.com/thomasloven/lovelace-card-mod) (required for glass effect + dynamic backgrounds)
- [button-card](https://github.com/custom-cards/button-card) (required for templates)
- [mini-graph-card](https://github.com/kalkih/mini-graph-card) (optional, for `field_graph`)
- [scheduler-card](https://github.com/nielsfaber/scheduler-card) (optional, for scheduling view)
- A weather integration configured (e.g., Met.no, OpenWeatherMap)

---

## Template Reference

### Glass Components

#### `glass_climate`
Full HVAC control widget with power button, temperature display, up/down controls, and status.

![glass_climate](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/glass_climate.png)

| Variable | Required | Description |
|----------|----------|-------------|
| `climate_entity` | Yes | Climate entity ID |
| `secondary_sensors` | No | Array of up to 3 sensor entity IDs |

#### `glass_container`
Horizontal-stack wrapper with glass effect. Use as a row container for multiple sub-cards (sensors, device buttons, etc.).

![glass_container](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/glass_container_sensors.png)

| Variable | Required | Description |
|----------|----------|-------------|
| *(none)* | — | Wrap child cards inside a horizontal-stack |

#### `state_on_off`
Visual state feedback with colored icon when entity is on. Combine with `glass_container` for device control rows.

| `on` | `off` |
|:----:|:-----:|
| ![state_on_off on](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/state_on_off_on.png) | ![state_on_off off](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/state_on_off_off.png) |

Same button, both states — the icon turns amber and the tile brightens when the entity is on.

| Variable | Required | Description |
|----------|----------|-------------|
| `entity` | Yes | Entity to toggle |

Several of them inside a `glass_container` row:

![state_on_off row](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/state_on_off.png)

#### `glass_cover`
Shutter/blind control with animation and position badge. The badge sits in the top-right corner
— out of the way of the name, which long entity names used to run into — and it follows the
current position along with the icon color and the left border: `fermé` at 0 %, `ouvert` at
100 %, the percentage in between, and `ouverture` / `fermeture` (with a pulsing icon) while the
shutter is moving.

| part-way open | opening | closed |
|:---:|:---:|:---:|
| ![cover part-way open](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/glass_cover.png) | ![cover opening](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/glass_cover_moving.gif) | ![cover closed](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/glass_cover_closed.png) |

The middle one is the real thing, not a mock-up: the shutter was driven while the capture ran,
so it shows the `mdi:window-shutter-alert` icon in `accent_moving`, the `ouverture` badge, and
the icon pulsing at 1.5 s per cycle.

| Variable | Required | Description |
|----------|----------|-------------|
| `entity` | Yes | Cover entity — the card reads its `current_position` and its `opening` / `closing` state |
| `accent_open` | No | Icon and border color when open (default `#42A5F5`) |
| `accent_closed` | No | Border color when closed (default `#546E7A`) |
| `accent_moving` | No | Icon and border color while moving (default `#7E57C2`) |

Tap toggles the cover, hold opens more-info.

#### `glass_garage`
Garage door control. The card is driven by **two entities**: a contact sensor gives the state
(icon, color, left border), and a script does the action — a garage motor is a dry-contact pulse,
not a switch, so the card can't just toggle the sensor.

![glass_garage](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/glass_garage.png)

| Variable | Required | Description |
|----------|----------|-------------|
| `entity` | Yes | Door contact/closure sensor (`binary_sensor`) — `on` = open (amber `mdi:garage-open-variant`), `off` = closed (grey `mdi:garage-variant`) |
| `script_entity` | No | Script fired on tap, via `script.turn_on` (default `script.pulse_porte_garage`) |
| `accent_open` | No | Icon and border color when open (default `#FF9800`) |
| `accent_closed` | No | Border color when closed (default `#546E7A`) |

Tap fires the script, hold opens more-info on the sensor.

### Field Templates

Composable sub-components for building sensor/monitoring cards. Combine `field_graph`, `field_secondary`, `field_command`, and `field_title` in a single card.

A single card — title, sparkline, secondary value and command buttons:

![field_templates](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/field_templates.png)

Two of them side by side in a row:

![field_templates pair](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/field_templates_pair.png)

#### `field_graph`
Inline mini-graph-card sparkline.

#### `field_title`
Card title label with icon.

#### `field_secondary`
Secondary sensor value display.

#### `field_command`
Up to 3 toggle/command buttons inside a card.

### Badges

The circles in the view header. `badge_base` gives them their shape, each badge puts its own
state logic on top, and anything extra — a countdown, a power reading — is a `custom_field`
placed outside the circle.

![badge row](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/badge_row.png)

#### `badge_base`
Shape only, no state: a 36 px circle with a drop shadow and a transition on every property.
Build on it either by driving the colors yourself, or by combining it with a `state_*` template
— `badge_pompe` in `glass-devices-example.yaml` is exactly `state_pompe` + `badge_base`.

| doorbell | remote | washing machine | borehole pump |
|:---:|:---:|:---:|:---:|
| ![doorbell badge](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/badge_doorbell.png) | ![remote badge](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/badge_remote.png) | ![washing machine badge](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/badge_washer.png) | ![pump badge](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/badge_pump.png) |

Four badges out of the header above, each shot on its own. The first two are `badge_base` with a
gradient driven by the entity state. The last two add a `custom_field`, the pill under the
circle: both show the power being drawn, and the washing machine swaps in the time left once a
cycle is running — neither was, here. A `custom_field` sits outside the circle, so a badge that
carries one needs `overflow: visible` on its card.

#### `badge_status`
Ready-made on/off variant of `badge_base` — swaps background, left border and icon on state,
and can pulse while on.

| Variable | Default | Description |
|----------|---------|-------------|
| `gradient_on` | `linear-gradient(135deg, #FFC107, #FFD54F)` | Background when on |
| `gradient_off` | `linear-gradient(135deg, #546E7A, #90A4AE)` | Background when off |
| `border_on` | `3px solid #FFC107` | Left border when on |
| `border_off` | `3px solid #37474F` | Left border when off |
| `icon_on` | `mdi:power` | Icon when on |
| `icon_off` | `mdi:power-off` | Icon when off |
| `pulse_animation` | `none` | CSS animation applied while on |

### Remote Buttons

#### `remote_button`
Colored button for remote control grids. Compact 4-column layout designed for IR/RF remotes.

<p align="center">
  <img src="https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/remote_view.png" alt="remote_view" width="384">
</p>

| Variable | Default | Description |
|----------|---------|-------------|
| `btn_bg` | `#374151` | Button background color |
| `btn_color` | `#FFFFFF` | Text/icon color |
| `btn_height` | `48px` | Button height |

---

## Multi-View Setup

The theme supports multiple views with different personalities:

```yaml
views:
  - title: Home
    theme: glass-dynamic    # Weather background
  - title: Weather
    theme: glass-dynamic    # Same dynamic background
  - title: Remote
    type: panel
    theme: glass-dynamic    # Works on panel views too
  - title: Proxmox
    theme: proxmox-tech     # Custom tech background (optional)
```

---

## Customization

### Changing the glass intensity
In the theme file, adjust:
```yaml
ha-card-background: "rgba(20, 20, 30, 0.55)"  # opacity (0.3 = lighter, 0.7 = darker)
```

And in `card-mod-card-yaml`:
```yaml
backdrop-filter: blur(12px) !important;  # blur radius (8px = subtle, 20px = heavy)
```

### Adding your own backgrounds
The theme uses a Jinja2 map in `card-mod-view`. Add new conditions:
```yaml
{% set weather_images = {
    'your-condition': '/local/backgrounds/weather/your-image.jpg?v=1',
    ...
} %}
```

---

## Credits

- Glass-morphism inspired by [glassmorphism.com](https://glassmorphism.com)
- Background photos from [Unsplash](https://unsplash.com) (free license)
- Built with [card-mod](https://github.com/thomasloven/lovelace-card-mod) and [button-card](https://github.com/custom-cards/button-card)

---

## Contributing

Contributions welcome! Feel free to:
- Submit new background photos
- Add button-card templates for new device types
- Improve documentation
- Report issues

---

## License

MIT - See [LICENSE](LICENSE)
