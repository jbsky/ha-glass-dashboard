# Glass Dynamic Dashboard for Home Assistant

A stunning glass-morphism theme with **weather-reactive backgrounds** and a complete **button-card template library** for Home Assistant.

[![HACS Badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/jbsky/ha-glass-dashboard)](https://github.com/jbsky/ha-glass-dashboard/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/jbsky/ha-glass-dashboard/blob/main/LICENSE)

---

## What makes this different?

| Feature | Frosted Glass Theme | Mobile First | **Glass Dynamic** |
|---------|--------------------:|-------------:|------------------:|
| Glass-morphism | Theme only | No | Theme + per-card |
| Dynamic backgrounds | No | No | 15 weather conditions |
| Button-card templates | No | Config dump | 38 reusable templates |
| Sun-aware (day/night) | No | No | Yes |
| Multi-view themes | No | No | Yes (tech, remote) |
| Remote control layout | No | No | Compact 4-col grid |
| Climate component | No | No | Full HVAC widget |

---

## Features

### Weather-Reactive Background
The dashboard background changes automatically based on your local weather — sunny, rainy, stormy, snowy, foggy... with night-time variants when the sun goes below the horizon.

### Glass-Morphism Everywhere
Every card gets a frosted glass effect from native Home Assistant theme variables — no plugin required:
- `ha-card-backdrop-filter: blur(12px)` for the glass effect
- Semi-transparent dark background
- Subtle light borders
- Consistent across all card types

### 38 Button-Card Templates
A complete template library organized by function:

| Category | Templates | Purpose |
|----------|-----------|---------|
| **Core Glass** | `glass_button`, `glass_container`, `glass_button_base` | Base glass cards |
| **Components** | `glass_climate`, `glass_cover`, `glass_garage` | Full device widgets |
| **Fields** | `field_command`, `field_graph`, `field_title`, `field_secondary` | Card sub-components |
| **States** | `state_on_off`, `animation_effects` | Visual state feedback |
| **Sensors** | `battery_rack`, `battery_level`, `humidity_template`, `temperature_template` | Sensor display |
| **Remote** | `remote_button`, `remote_separator` | IR/RF remote grid |
| **Badges** | `badge_base`, `badge_status`, `badge_power`, `badge_countdown`, `badge_appliance`, `badge_health` | Status indicators |

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

- [UIX](https://github.com/Lint-Free-Technology/uix) (required to make the background follow the weather — without it you get a fixed photo, not a flat background)
- [button-card](https://github.com/custom-cards/button-card) (required for templates)
- [mini-graph-card](https://github.com/kalkih/mini-graph-card) (optional, for `field_graph`)
- [scheduler-card](https://github.com/nielsfaber/scheduler-card) (optional, for scheduling view)
- A weather integration configured (e.g., Met.no, OpenWeatherMap)

> **Migrating from card-mod?** Versions up to `v1.x` of this theme relied on card-mod, which
> is broken since Home Assistant 2026.8 and will not be fixed
> ([lovelace-card-mod#606](https://github.com/thomasloven/lovelace-card-mod/issues/606)).
> Uninstall card-mod, drop its `extra_module_url` entry from `configuration.yaml`, restart,
> then install UIX from HACS and add the integration in **Settings > Devices & Services**.
> The glass effect itself no longer needs any plugin — it now uses native theme variables.
> UIX is only required for the background to *follow the weather*. The theme also ships a
> plain `lovelace-background` key, so without UIX — or during the second or two it takes UIX
> to attach its style node and get its template rendered by the server — the view still sits
> on a photo rather than on a flat colour.

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

The circles in the view header. They are five pieces that stack, so a badge is a card with a
handful of `variables` rather than a page of inline JavaScript:

| | |
|---|---|
| `badge_base` | the shape — and the `badge-pulse` keyframes the others animate with |
| `badge_status` | on/off colors |
| `badge_power` | the power pill |
| `badge_countdown` | the time-left pill |
| `badge_appliance` / `badge_health` | a whole behaviour, built on the pieces above |

The two pills carry nothing but themselves — no colors, no shape — so they combine: `template:
[badge_status, badge_power]` is an on/off badge that reads a wattage, and `badge_appliance` is
`[badge_status, badge_power, badge_countdown]` with the machine phase wired on top. Anything
drawn outside the circle is a `custom_field`, which is why both pills set `overflow: visible`
on the card.

One thing does not stack: `triggers_update` is a single expression, so the last template in
the list wins. A card that combines two pills has to declare its own, naming every entity it
reads — `badge_appliance` does exactly that.

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
A pill in the bottom-right corner with the power being drawn, and nothing else — no colors, no
shape. It is meant to be stacked on a badge that has those: `[badge_status, badge_power]` for
an on/off device, and `badge_appliance` pulls it in the same way. The pill disappears while
the badge is off, or when the sensor holds anything that is not a number.

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

#### `badge_countdown`
The same idea as `badge_power`, for time instead of watts: a pill in the bottom-left corner
holding what is left of a countdown, and nothing else. It reads an absolute timestamp and
prints the distance to it — `45m`, then `1h30`. The pill disappears while the badge is off,
when the sensor holds anything that is not a date, or when `countdown_active` is false.

| Variable | Default | Description |
|----------|---------|-------------|
| `finish_entity` | — | Timestamp sensor for the end of the countdown |
| `countdown_bg` | `rgba(0,0,0,0.55)` | Pill background |
| `countdown_active` | `true` | Extra gate — accepts a JS template, and `badge_appliance` uses it to show the pill only during a cycle |

`countdown_active` is what keeps the brick honest on a sensor that goes stale: many appliances
leave their completion time in the past once they stop, and the pill would otherwise sit at
`0m` forever. Gate it on whatever means "still running" for that device.

#### `badge_appliance`
An appliance behind a plug: the badge follows the switch *and* a machine-state sensor, so it
has four looks — unplugged, idle, running, paused — and carries both the time left and the
power drawn. Nothing but the dark circle shows while the plug is off.

It owns no colors of its own. It is `[badge_status, badge_power, badge_countdown]`, and all it
adds is the phase: one `cycle_phase` variable that resolves to `run`, `pause` or `idle`, and a
handful of variables that hand the matching look back to `badge_status`. So `power_entity`,
`power_bg`, `countdown_bg` and `countdown_active` come from the two tables above and are not
repeated here.

The circle and the icon follow different things on purpose. The circle is the plug — dark when
it is cut, colored as soon as it feeds the machine. The icon is the machine: it stays crossed
out until a cycle actually runs, so a green circle with a crossed-out drum reads "powered,
doing nothing".

| Variable | Default | Description |
|----------|---------|-------------|
| `state_entity` | — | Machine-state sensor |
| `run_states` | `["run"]` | Values of that sensor that count as running |
| `pause_states` | `["pause"]` | Values that count as paused |
| `finish_entity` | — | Timestamp sensor for the end of the cycle |
| `gradient_off` / `_idle` / `_run` / `_pause` | dark / green / teal / orange | Background per look |
| `border_off` / `_idle` / `_run` / `_pause` | `3px solid …` | Left border per look |
| `glow_off` / `_idle` / `_run` / `_pause` | `grayscale…` / `drop-shadow…` | Icon `filter` per look |
| `icon_run` / `icon_idle` | `mdi:washing-machine` / `mdi:washing-machine-off` | Icon while a cycle runs / while the plug is live but nothing runs |
| `icon_off` | `mdi:washing-machine-off` | Icon while the plug is cut |
| `pulse_off` / `_idle` / `_run` / `_pause` | `none` / `none` / `badge-pulse 1.5s ease-in-out infinite` / `none` | Animation per look |
| `pulse_from` / `pulse_to` | teal | The two glow colors of `badge-pulse` |

> **Do not set the `*_on` variables here.** `gradient_on`, `border_on`, `glow_on`, `icon_on`
> and `pulse_animation` are what this template *computes* from the phase and hands to
> `badge_status`. A card that sets one of them wins the merge — silently, with no error — and
> flattens the three live looks into one. Set `*_idle` / `*_run` / `*_pause` instead.
>
> Coming from an earlier version: `icon_on` used to be the running icon and `icon_off`
> everything else. They are now `icon_run` and `icon_idle`. A card still passing `icon_on`
> shows the running icon in every phase, drum never crossed out.

An `unavailable` or `unknown` plug falls back to the off look, through a `default` state entry
this template adds for itself. Two details of that look are worth knowing before you tune it:
`badge_status` dims the whole circle to 90 % while it is off — same as the pump and the remote,
it is the house style — and it also applies `opacity: 0.8` to the icon, on top of whatever
`glow_off` does. That is why `glow_off` defaults to `opacity(0.75)` rather than the `0.6` you
might expect: 0.75 × 0.8 is the 0.6 that actually lands.

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

Both pills only refresh when one of the four entities named in `triggers_update` moves, so a
machine that reports nothing for ten minutes shows a countdown ten minutes stale.

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

### Sensors

#### `battery_rack`
Every battery in the house as a rack of upright cells, lowest first. One card draws the whole
table: it walks the state machine itself, reads whatever each device publishes about its
battery, and lays the result out `columns` per row. Nothing to list and nothing to keep in
sync — a device that gains a battery sensor shows up on its own, one that goes `unavailable`
drops out. It needs no card beyond `button-card`.

![battery_rack](https://raw.githubusercontent.com/jbsky/ha-glass-dashboard/main/docs/screenshots/components/battery_rack.png)

The fill height is the charge and its color the severity band, and a cell at or below `low`
pulses. Sorted lowest first, the rack opens on whatever is closest to dying — a plant sensor at
2 % sits at the front, pulsing red, long before you would have gone looking for it. The number
sits inside the cell, the name under it — the friendly name minus its trailing
"Battery"/"Batterie" (`name_strip`), clamped to two lines. Tapping a cell opens *that* sensor's
more-info dialog, so nothing is lost against a list of bars.

**Not every device measures its battery**, and the ones that don't are exactly the ones a
percentage-only rack hides. Three readings are accepted, in that order of preference:

| The device publishes | Read as | Drawn as |
|---|---|---|
| a number (`device_class: battery`, or a `%` on a `battery` entity) | the value | solid outline, the number inside |
| a word — `low`, `medium`, `high`… (`text_levels`) | the mapped percentage | dashed outline, the word inside |
| a binary `battery low` (`binary_sensor`, `device_class: battery`) | `low` when on, `ok` when off | dashed outline, `low` / `ok` inside |

A dashed outline therefore means *deduced, not measured* — a freezer thermometer that only ever
says `high` or `medium` gets one. Devices commonly publish two of these at once, so the rack
keeps **one cell per device**, best reading first: a plant sensor reporting both `2 %` and `low`
is drawn once, from the number. A `*_battery_state` holding a
charging status (`discharging`, `Not Charging`) is not a level and is ignored, and the `_2`
Home Assistant appends to a duplicate name is kept — `x_battery` and `x_battery_2` are two
devices, while `x_battery_level_2` and `x_battery_state_2` are one.

| Variable | Default | Description |
|----------|---------|-------------|
| `entities` | `[]` | Explicit list; empty means every battery found. A listed entity with no readable level is drawn grey with a `?` rather than dropped |
| `exclude` | — | Regex matched against the entity id, dropped from the rack |
| `columns` | `6` | Cells per row |
| `layout` | `grid` | `grid` wraps, `scroll` keeps one swipeable row, `expand` folds to one row behind a `+N` cell |
| `cell_width` | `48px` | Column width under `scroll`; ignored by the other two |
| `storage_key` | — | Names the fold's memory under `expand`; two racks want two keys |
| `sort` | `level` | `level` (lowest first), `name`, or `none` for the order given |
| `low` / `warn` / `mid` | `15` / `30` / `60` | Severity thresholds, in percent |
| `color_low` / `color_warn` | `#db4437` / `#ff9800` | Fill and border below each threshold |
| `color_mid` / `color_full` | `#fdd835` / `#43a047` | Fill and border above them |
| `color_unknown` | `#78909C` | Used when no reading can be made of the state |
| `width` / `height` | `26px` / `46px` | Size of one cell |
| `gap` | `10px 6px` | Grid gap, row then column |
| `pulse_low` | `battery-low 1.6s ease-in-out infinite` | Animation at or below `low`; `none` to drop it |
| `name_strip` | trailing *battery* / *batterie* | Regex cut off the end of the friendly name |
| `text_levels` | `low: 15`, `medium: 50`, `high: 90`… | Percentage each spelled-out level stands for |
| `text_labels` | `medium: med`, `critical: !`… | Shorter word to print in the cell |

```yaml
type: custom:button-card
template: battery_rack
variables:
  columns: 6
```

Auto-discovery is the default, not the only mode. Name the cells yourself and they render in
that order, which is how you build one rack per room — or drop the phones from the house-wide
one with `exclude: iphone|ipad`:

```yaml
type: custom:button-card
template: battery_rack
variables:
  columns: 3
  sort: none
  entities:
    - sensor.thermometre_parent_battery
    - sensor.thermometre_mathilde_battery
    - sensor.thermometre_alexandre_battery
```

#### One line instead of a table

A rack that wraps every `columns` cells is what you want on a wall panel, and the last thing you
want above the fold on a phone — twenty batteries push everything else off the screen. `layout`
keeps the rack to a single row, two ways, and neither drops a battery:

| `layout` | The rack becomes |
|---|---|
| `grid` *(default)* | Wraps every `columns` cells, as many rows as it takes |
| `scroll` | One row of `cell_width` columns, swiped sideways; the row scrolls, the card does not grow |
| `expand` | One row — the first `columns - 1` cells (never fewer than one) and a `+N` cell that unfolds the full grid |

Neither is a truncation, because the rack is sorted by level: what stays in view is whatever is
closest to dying, and the cells that scroll off or fold away are the ones at 90 %.

```yaml
type: custom:button-card
template: battery_rack
variables:
  layout: expand
  columns: 6
```

The `+N` cell toggles a class from an inline `pointerup` handler, and so does a battery cell to
open its dialog. Both details are forced by `button-card`, and both are worth knowing before
writing any template of your own:

- **No native form control works inside a `button-card`.** Its action handler calls
  `preventDefault()` on the card's click, which cancels the activation behaviour of everything
  inside it — a checkbox there never flips, not even through `.click()`, so the tidy
  `:checked ~ …` fold silently does nothing. Same for a `<label for>`, a radio, a `<details>`.
- **`onclick` is dead on a touchscreen.** The same handler cancels `touchend`, and a cancelled
  `touchend` means the browser never synthesises a click at all. A tap delivers
  `pointerdown, touchstart, pointerup, touchend` and no `click`, so anything bound to `onclick`
  works with a mouse and does nothing under a finger — including in the companion app.

Hence `pointerup`, which arrives from both a finger and a mouse, and *only* `pointerup`: also
binding `onclick` would fire everything twice on desktop, and a time window to tell the two
apart would swallow genuine second taps. Keyboard support gets its own `Enter` / `Space`
handler for the same reason the rest exists.

The open state is kept in `localStorage` under `storage_key`, which is also what keeps two racks
on the same dashboard from sharing one fold — give them two keys, or leave both unnamed and they
open together. The rack re-reads that key on every redraw, so a battery reporting in behind your
back cannot fold the card back up under your finger.

One thing to know if you serve Home Assistant through a hardened reverse proxy: cells and the
`+N` toggle both act from inline handlers, so a `Content-Security-Policy` whose `script-src`
drops `'unsafe-inline'` leaves the rack drawn correctly but inert — cells will not open their
dialog and the fold will not open. Home Assistant itself sends no such policy.

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

And the blur radius, right below it:
```yaml
ha-card-backdrop-filter: "blur(12px)"  # 8px = subtle, 20px = heavy
```

### Adding your own backgrounds
The theme uses a Jinja2 map in `uix-view`. Add new conditions:
```yaml
{% set weather_images = {
    'your-condition': 'your-image.jpg',
    ...
} %}
```

---

## Credits

- Glass-morphism inspired by [glassmorphism.com](https://glassmorphism.com)
- Background photos from [Unsplash](https://unsplash.com) (free license)
- Built with [UIX](https://github.com/Lint-Free-Technology/uix) and [button-card](https://github.com/custom-cards/button-card)

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
