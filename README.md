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
| Button-card templates | No | Config dump | 36 reusable templates |
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

### 36 Button-Card Templates
A complete template library organized by function:

| Category | Templates | Purpose |
|----------|-----------|---------|
| **Core Glass** | `glass_button`, `glass_container`, `glass_button_base` | Base glass cards |
| **Components** | `glass_climate`, `glass_cover`, `glass_garage` | Full device widgets |
| **Fields** | `field_command`, `field_graph`, `field_title`, `field_secondary` | Card sub-components |
| **States** | `state_on_off`, `animation_effects` | Visual state feedback |
| **Sensors** | `battery_level`, `humidity_template`, `temperature_template` | Sensor display |
| **Remote** | `remote_button`, `remote_separator` | IR/RF remote grid |
| **Badges** | `badge_base`, `badge_status`, `badge_power`, `badge_appliance`, `badge_health` | Status indicators |

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

The circles in the view header. They are four pieces that stack, so a badge is a card with a
handful of `variables` rather than a page of inline JavaScript:

| | |
|---|---|
| `badge_base` | the shape — and the `badge-pulse` keyframes the others animate with |
| `badge_status` | on/off colors |
| `badge_power` | the power pill |
| `badge_appliance` / `badge_health` | a whole behaviour, built on the pieces above |

`badge_power` carries nothing but the pill, so it combines: `template: [badge_status,
badge_power]` is an on/off badge that reads a wattage, and `badge_appliance` picks up the same
pill without redefining it. Anything drawn outside the circle is a `custom_field`, which is
why `badge_power` sets `overflow: visible` on the card.

![badge row](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/badge_row.png)

| doorbell | remote | washing machine | borehole pump |
|:---:|:---:|:---:|:---:|
| ![doorbell badge](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/badge_doorbell.png) | ![remote badge](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/badge_remote.png) | ![washing machine badge](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/badge_washer.png) | ![pump badge](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/badge_pump.png) |
| `badge_health` | `badge_status` | `badge_appliance` | `badge_status` + `badge_power` |

Four badges out of the header above, each shot on its own, in the state they happened to be
in. The doorbell is on with its relay unreachable — hence the orange circle instead of the
yellow one, and the red dot in the corner; by the time the row above was shot it had been
switched off, which is the grey circle. The washing machine is plugged in but idle, so the
circle is green while the drum stays crossed out — the icon follows the machine, the color
follows the plug. Both it and the pump read the power being drawn, and the washing machine
swaps in the time left once a cycle starts.

#### `badge_base`
Shape only, no state: a 36 px circle with a drop shadow and a transition on every property. It
also holds the `badge-pulse` keyframes, so anything built on it can pulse by naming that
animation. Build on it either by driving the colors yourself, or by combining it with a
`state_*` template — `badge_pompe` in `glass-devices-example.yaml` is exactly `state_pompe` +
`badge_base`. Note that `extra_styles` replaces rather than merges: a card that declares its
own has to re-declare the keyframes.

#### `badge_status`
On/off badge — swaps background, left border and icon on state, and can pulse while on.

| Variable | Default | Description |
|----------|---------|-------------|
| `gradient_on` | `linear-gradient(135deg, #FFC107, #FFD54F)` | Background when on |
| `gradient_off` | `linear-gradient(135deg, #546E7A, #90A4AE)` | Background when off |
| `border_on` | `3px solid #FFC107` | Left border when on |
| `border_off` | `3px solid #37474F` | Left border when off |
| `icon_on` | `mdi:power` | Icon when on |
| `icon_off` | `mdi:power-off` | Icon when off |
| `icon_color_on` | `#FFFFFF` | Icon color when on |
| `icon_color_off` | `#CFD8DC` | Icon color when off |
| `glow_on` | `drop-shadow(0 0 4px rgba(255,255,255,0.5))` | Icon `filter` when on |
| `glow_off` | `none` | Icon `filter` when off |
| `pulse_animation` | `none` | CSS animation applied while on |
| `pulse_from` / `pulse_to` | `rgba(255,255,255,0.35)` / `rgba(255,255,255,0.6)` | The two glow colors of `badge-pulse`, the keyframes shipped with the template |

The remote badge above, in full:

```yaml
type: custom:button-card
entity: remote.rm4pro
template: badge_status
size: 75%
tap_action:
  action: navigate
  navigation_path: /lovelace/telecommande
variables:
  icon_on: mdi:remote-tv
  icon_off: mdi:remote-tv
  gradient_on: linear-gradient(135deg, #1565C0, #42A5F5)
  gradient_off: linear-gradient(135deg, #616161, #9E9E9E)
  border_on: 3px solid #0D47A1
  border_off: 3px solid #424242
  glow_on: drop-shadow(0 0 4px rgba(21, 101, 192, 0.8))
  glow_off: grayscale(100%)
  icon_color_off: "#FFFFFF"
```

#### `badge_power`
A pill in the corner with the power being drawn, and nothing else — no colors, no shape. It is
meant to be stacked on a badge that has those: `[badge_status, badge_power]` for an on/off
device, and `badge_appliance` pulls it in the same way. The pill disappears while the badge is
off, or when the sensor holds anything that is not a number.

| Variable | Default | Description |
|----------|---------|-------------|
| `power_entity` | — | Sensor read for the pill |
| `power_bg` | `rgba(0,0,0,0.55)` | Pill background |

The pump badge above — `badge_status` for the colors, `badge_power` for the pill, so both sets
of variables apply:

```yaml
type: custom:button-card
entity: switch.pompe_forage
template:
  - badge_status
  - badge_power
size: 75%
variables:
  power_entity: sensor.pompe_forage_power
  power_bg: rgba(1, 87, 155, 0.85)
  icon_on: mdi:pump
  icon_off: mdi:pump-off
  gradient_on: linear-gradient(135deg, #0288D1, #4FC3F7)
  gradient_off: linear-gradient(135deg, #546E7A, #90A4AE)
  border_on: 3px solid #01579B
  border_off: 3px solid #37474F
  glow_on: drop-shadow(0 0 6px rgba(2, 136, 209, 0.8))
  glow_off: grayscale(80%)
  pulse_animation: badge-pulse 2s ease-in-out infinite
  pulse_from: rgba(2, 136, 209, 0.4)
  pulse_to: rgba(79, 195, 247, 0.7)
```

#### `badge_appliance`
An appliance behind a plug: the badge follows the switch *and* a machine-state sensor, so it
has four looks — unplugged, idle, running, paused — and carries both the time left and the
power drawn. Nothing but the dark circle shows while the plug is off. It is built on
`badge_base` + `badge_power`, so `power_entity` and `power_bg` come from that table above and
are not repeated here.

The two follow different things on purpose. The circle is the plug — dark when it is cut,
colored as soon as it feeds the machine. The icon is the machine: it stays crossed out until a
cycle actually runs, so a green circle with a crossed-out drum reads "powered, doing nothing".

| Variable | Default | Description |
|----------|---------|-------------|
| `state_entity` | — | Machine-state sensor |
| `run_states` | `["run"]` | Values of that sensor that count as running |
| `pause_states` | `["pause"]` | Values that count as paused |
| `finish_entity` | — | Timestamp sensor for the end of the cycle |
| `gradient_off` / `_idle` / `_run` / `_pause` | dark / green / teal / orange | Background per look |
| `border_off` / `_idle` / `_run` / `_pause` | `3px solid …` | Left border per look |
| `glow_off` / `_idle` / `_run` / `_pause` | `grayscale…` / `drop-shadow…` | Icon `filter` per look |
| `icon_on` / `icon_off` | `mdi:washing-machine` / `mdi:washing-machine-off` | Icon while a cycle runs / any other time |
| `pulse_off` / `_idle` / `_run` / `_pause` | `none` / `none` / `badge-pulse 1.5s ease-in-out infinite` / `none` | Animation per look |
| `pulse_from` / `pulse_to` | teal | The two glow colors of `badge-pulse` |
| `countdown_bg` | `rgba(0, 105, 92, 0.9)` | Countdown pill background (`power_bg` defaults to green here) |

The defaults are the washing machine above, so it comes down to the three sensors — plus
one line here, because that badge pulses as soon as its plug is live, the way the pump does:

```yaml
type: custom:button-card
entity: switch.lave_linge_2
template: badge_appliance
size: 75%
tap_action:
  action: more-info
  entity: sensor.lave_linge_washer_machine_state
variables:
  # pulse whenever the plug feeds the machine, not only during a cycle
  pulse_idle: badge-pulse 2s ease-in-out infinite
  state_entity: sensor.lave_linge_washer_machine_state
  finish_entity: sensor.lave_linge_washer_completion_time
  power_entity: sensor.lave_linge_power
```

The countdown reads the completion time as an absolute timestamp and prints what is left:
`45m`, then `1h30`. It only refreshes when one of the entities in `triggers_update` moves, so
a machine that reports nothing for ten minutes shows a countdown ten minutes stale.

#### `badge_health`
On/off badge that also watches the relay, bridge or gateway the device hangs off. While that
companion entity is `unavailable` the circle turns to `gradient_alert` and the corner dot flips
to `link_icon_down` — the device still answers, but you can see the link behind it is down.

| Variable | Default | Description |
|----------|---------|-------------|
| `watch_entity` | — | Companion entity whose availability is watched |
| `gradient_on` / `_off` / `_alert` | yellow / grey / orange | Background per look |
| `border_on` / `_off` / `_alert` | `3px solid …` | Left border per look |
| `icon_on` / `icon_off` | `mdi:bell-ring` / `mdi:bell-off` | Icon |
| `glow_on` / `glow_off` | `drop-shadow…` / `grayscale…` | Icon `filter` |
| `link_icon_up` / `link_icon_down` | `mdi:wifi` / `mdi:wifi-off` | Corner dot |
| `link_color_up` / `link_color_down` | `#4caf50` / `#f44336` | Corner dot color |

The doorbell above — the defaults are its colors, so only the companion is left to name:

```yaml
type: custom:button-card
entity: switch.sonnette
template: badge_health
size: 75%
tap_action:
  action: toggle
double_tap_action:
  action: call-service
  service: button.press
  service_data:
    entity_id: button.doorbell_relay_doorbell_ring
variables:
  watch_entity: button.doorbell_relay_doorbell_ring
```

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
