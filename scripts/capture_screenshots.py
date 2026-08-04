"""Screenshot capture for ha-glass-dashboard.

Captures dashboard views with Playwright, at a configurable device scale factor, using a
long-lived access token instead of relying on `trusted_networks` auto-login (which only
works when the browser reaches Home Assistant from an already-trusted source address).

It also captures the per-template close-ups used in the README's *Template Reference*: each
one is cropped by the browser from the card element itself, so there are no coordinates to
re-measure when the layout moves. Cards that only make sense in a given state (a light on
*and* off, a shutter part-way open, a shutter in motion) carry a `setup` entry — the script
drives the entity there, captures, and puts it back where it found it. `frames` turns a
component into an animated GIF, which is the only way to show the moving state.

Usage
-----
    pip install playwright && playwright install chromium

    # 1. Home Assistant -> profile -> Security -> Long-lived access tokens -> Create
    # 2. store it (never pass a token on the command line, it shows up in `ps`)
    install -m 600 /dev/null ~/.ha_token && $EDITOR ~/.ha_token

    HA_URL=http://homeassistant.local:8123 python3 scripts/capture_screenshots.py

    # views + component crops, through an SSH relay (see below)
    HA_URL=http://home.home.arpa HA_SSH_RELAY=root@node1.home.arpa \
    HA_SSH_TARGET=192.168.4.50:80 HA_COMPONENTS=1 python3 scripts/capture_screenshots.py

Environment
-----------
    HA_URL          base URL of the instance          (default http://homeassistant.local:8123)
    HA_TOKEN_FILE   file holding the token            (default ~/.ha_token)
    HA_VIEWS        "path:name,path:name,..."         (default the seven views below)
    HA_OUT          output directory                  (default docs/screenshots)
    HA_SCALE        device scale factor, 1 or 2       (default 2)
    HA_SETTLE_MS    wait after load, for card-mod     (default 7000)
    HA_MAP_HOST     "name=host:port" for --host-resolver-rules (optional, see below)
    HA_VIEWS_ONLY   set to 0 to skip the view captures            (default 1)
    HA_MOBILE       set to 0 to skip the mobile viewport          (default 1)
    HA_COMPONENTS   set to 1 to also capture the per-template cards
    HA_ONLY         space-separated component names to limit the run
    HA_LAMP_ENTITY  switch used for the on/off pair   (default switch.lumiere_wc)
    HA_COVER_ENTITY cover driven for the cover shots  (default cover.volet_roulant_cuisine)
    HA_SSH_RELAY    "user@host" — relay every browser connection through that host
    HA_SSH_TARGET   "ip:port" of HA as seen from the relay host   (default 192.168.4.50:80)
    HA_RELAY_PORT   local port for the relay          (default 18126)

Reaching an instance you have no direct route to
------------------------------------------------
If the browser host cannot open a TCP connection to Home Assistant, forward a local port to
it (`ssh -L <port>:<ha-host>:<ha-port> <jump-host>`) and point HA_URL at 127.0.0.1:<port>.

Two things bite when doing that:

* If a reverse proxy in front of Home Assistant routes by Host name, requests carrying
  `Host: 127.0.0.1:<port>` get a 404. Keep HA_URL on the real host name and set
  HA_MAP_HOST=<name>=127.0.0.1:<port>: Chromium then resolves that name to the tunnel while
  still sending the correct Host header.
* If the jump host refuses port forwarding (`AllowTcpForwarding no`), forward the stream
  instead of the port: a local listener that pipes each connection through
  `ssh <jump-host> nc <ha-host> <ha-port>` does the same job. Reuse one SSH connection
  (`ControlMaster`) or every request pays a full handshake — and keep the ControlPath short,
  a UNIX socket path is capped at 108 bytes.

HA_SSH_RELAY does that second form for you, MAP_HOST included.

Adapting it to your instance
----------------------------
The `COMPONENTS` list, `HA_LAMP_ENTITY` and the `HA_SSH_*` defaults describe the dashboard this
theme was built on: the locators match its card names ("Office AC", "Escalier", "Baie vitr"…)
and the on/off pair drives one of its switches. Point them at your own entities before running
`HA_COMPONENTS=1`, or the locators will simply find nothing. The relay also passes
`StrictHostKeyChecking=no`, which is fine for a host you already trust and wrong for one you
don't.
"""

import io
import json
import os
import socket
import subprocess
import sys
import threading
import time
import urllib.request

from playwright.sync_api import sync_playwright

HA_URL = os.environ.get("HA_URL", "http://homeassistant.local:8123").rstrip("/")
TOKEN_FILE = os.path.expanduser(os.environ.get("HA_TOKEN_FILE", "~/.ha_token"))
OUT = os.path.expanduser(os.environ.get("HA_OUT", "docs/screenshots"))
SCALE = int(os.environ.get("HA_SCALE", "2"))
SETTLE_MS = int(os.environ.get("HA_SETTLE_MS", "7000"))
MAP_HOST = os.environ.get("HA_MAP_HOST", "")
WANT_VIEWS = os.environ.get("HA_VIEWS_ONLY", "1") != "0"
WANT_MOBILE = os.environ.get("HA_MOBILE", "1") != "0"
WANT_COMPONENTS = os.environ.get("HA_COMPONENTS", "0") == "1"
ONLY = set(os.environ.get("HA_ONLY", "").split()) or None
LAMP_ENTITY = os.environ.get("HA_LAMP_ENTITY", "switch.lumiere_wc")
COVER_ENTITY = os.environ.get("HA_COVER_ENTITY", "cover.volet_roulant_cuisine")
SSH_RELAY = os.environ.get("HA_SSH_RELAY", "")
SSH_TARGET = os.environ.get("HA_SSH_TARGET", "192.168.4.50:80")
RELAY_PORT = int(os.environ.get("HA_RELAY_PORT", "18126"))

DEFAULT_VIEWS = (
    "/lovelace/0:home,/lovelace/1:weather,/lovelace/2:remote,"
    "/lovelace/3:programmation,/lovelace/4:proxmox,/lovelace/5:routeurs,/lovelace/6:nas"
)
VIEWS = [tuple(v.split(":", 1)) for v in os.environ.get("HA_VIEWS", DEFAULT_VIEWS).split(",")]

DESKTOP = {"width": 1920, "height": 1080}
MOBILE = {"width": 390, "height": 844}

# Locators resolve through shadow DOM. A `:has-text()` selector also matches every ancestor
# containing that text, so `pick` says which match to keep: "smallest" for one card,
# "largest" for the row it sits in. "index" is for rows whose cards carry no text at all —
# icons only — and is the one entry that a layout change can silently invalidate.
COMPONENTS = [
    {"name": "glass_climate", "view": "/lovelace/0", "pick": "largest",
     "locator": 'button-card:has-text("Office AC")'},

    {"name": "glass_container_sensors", "view": "/lovelace/0", "pick": "largest",
     "locator": 'hui-card:has(button-card:has-text("Escalier"))'},

    {"name": "state_on_off_on", "view": "/lovelace/0", "pick": "smallest",
     "locator": 'hui-card:has(button-card:has-text("Escalier")) button-card:has-text("WC")',
     "setup": {"entity": LAMP_ENTITY, "want": "on"}},

    {"name": "state_on_off_off", "view": "/lovelace/0", "pick": "smallest",
     "locator": 'hui-card:has(button-card:has-text("Escalier")) button-card:has-text("WC")',
     "setup": {"entity": LAMP_ENTITY, "want": "off"}},

    {"name": "state_on_off", "view": "/lovelace/0", "pick": "index", "index": 2,
     "locator": "hui-card"},

    # un seul aller-retour du volet cuisine : l'animation d'abord, l'etat stabilise ensuite
    {"name": "glass_cover_moving", "view": "/lovelace/0", "pick": "smallest",
     "locator": 'hui-card:has(button-card:has-text("Baie vitr")) button-card:has-text("Cuisin")',
     "setup": {"entity": COVER_ENTITY, "want": 60, "while_moving": True},
     "frames": 12, "interval_ms": 600},

    {"name": "glass_cover", "view": "/lovelace/0", "pick": "smallest",
     "locator": 'hui-card:has(button-card:has-text("Baie vitr")) button-card:has-text("Cuisin")',
     "setup": {"entity": COVER_ENTITY, "want": 60}},

    {"name": "glass_cover_closed", "view": "/lovelace/0", "pick": "smallest",
     "locator": 'button-card:has-text("Porte fen")'},

    {"name": "glass_garage", "view": "/lovelace/0", "pick": "smallest",
     "locator": 'hui-card:has(button-card:has-text("Baie vitr")) button-card:has-text("Garage")'},

    {"name": "field_templates", "view": "/lovelace/0", "pick": "largest",
     "locator": 'button-card:has-text("Météo")'},

    {"name": "field_templates_pair", "view": "/lovelace/0", "pick": "largest",
     "locator": 'hui-card:has-text("Météo")'},

    {"name": "badge_status", "view": "/lovelace/0", "pick": "largest",
     "locator": "hui-view-badges"},

    # le panneau remote n'est pas une carte mais une pile de grilles : on clippe leur union
    {"name": "remote_view", "view": "/lovelace/2", "pick": "union", "pad": 10,
     "locator": "hui-grid-card"},
]


class SSHRelay:
    """Local listener that pipes each connection through `ssh <hop> nc <host> <port>`.

    Used instead of `ssh -L` because the only host with a route to Home Assistant here
    refuses port forwarding. One SSH master is shared by every connection.
    """

    def __init__(self, hop, target, port):
        self.hop, self.target, self.port = hop, target, port
        self.cmd = [
            "ssh", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null",
            "-o", "LogLevel=ERROR", "-o", "ControlMaster=auto",
            "-o", "ControlPath=/tmp/.cm-hashot-%C", "-o", "ControlPersist=120",
            hop, "nc", target[0], str(target[1]),
        ]

    def _pipe(self, conn, proc):
        def upstream():
            try:
                while True:
                    data = conn.recv(65536)
                    if not data:
                        break
                    proc.stdin.write(data)
                    proc.stdin.flush()
            except OSError:
                pass
            finally:
                try:
                    proc.stdin.close()
                except OSError:
                    pass

        threading.Thread(target=upstream, daemon=True).start()
        try:
            while True:
                data = proc.stdout.read1(65536)
                if not data:
                    break
                conn.sendall(data)
        except OSError:
            pass
        finally:
            conn.close()
            proc.kill()

    def _serve(self, srv):
        while True:
            try:
                conn, _ = srv.accept()
            except OSError:
                return
            proc = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=subprocess.DEVNULL)
            threading.Thread(target=self._pipe, args=(conn, proc), daemon=True).start()

    def start(self):
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("127.0.0.1", self.port))
        srv.listen(64)
        threading.Thread(target=self._serve, args=(srv,), daemon=True).start()
        print(f"relay 127.0.0.1:{self.port} -> {self.hop} -> "
              f"{self.target[0]}:{self.target[1]}")


def rest(token, path, payload=None, origin=None):
    """Call the REST API, sending the real Host header even through the relay."""
    req = urllib.request.Request(
        (origin or HA_URL) + path,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json",
                 "Host": HA_URL.split("://", 1)[1]},
        method="POST" if payload is not None else "GET",
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode() or "null")


def read_token():
    if not os.path.exists(TOKEN_FILE):
        sys.exit(f"no token file at {TOKEN_FILE} — create a long-lived access token first")
    token = open(TOKEN_FILE).read().strip()
    if not token:
        sys.exit(f"{TOKEN_FILE} is empty")
    return token


def token_init_script(token):
    """Pre-seed the frontend session so the browser never sees the login form."""
    tokens = {
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": 315360000,
        "hassUrl": HA_URL,
        "clientId": None,
        "expires": 9999999999000,
        "refresh_token": "",
    }
    return "window.localStorage.setItem('hassTokens', %s);" % json.dumps(json.dumps(tokens))


def new_page(browser, token, viewport, mobile=False):
    ctx = browser.new_context(viewport=viewport, device_scale_factor=SCALE,
                              is_mobile=mobile, has_touch=mobile,
                              ignore_https_errors=True)
    ctx.add_init_script(token_init_script(token))
    return ctx, ctx.new_page()


def capture_views(page, suffix, mobile=False):
    for path, name in VIEWS:
        page.goto(HA_URL + path, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(SETTLE_MS)
        target = os.path.join(OUT, f"{name}-{suffix}.png")
        page.screenshot(path=target, full_page=mobile)
        print(f"  {target}")


def visible_boxes(page, selector):
    loc = page.locator(selector)
    out = []
    for i in range(loc.count()):
        node = loc.nth(i)
        try:
            box = node.bounding_box(timeout=5000)
        except Exception:
            box = None
        if box and box["width"] > 1 and box["height"] > 1:
            out.append((box, node))
    return out


def capture_card(page, spec, target):
    """Shoot one component and return its CSS box.

    A `:has-text()` selector matches the card *and* every ancestor that contains it, plus
    inner labels, and some of those matches are not rendered at all. Rather than guessing a
    position in that list, pick by geometry. Some components are not a single element at all
    — the remote panel is a stack of grid rows — so "union" clips the page to the whole set.
    """
    pick = spec.get("pick", "smallest")
    if pick == "index":
        card = page.locator(spec["locator"]).nth(spec["index"])
        card.screenshot(path=target, timeout=20000)
        return card.bounding_box()

    boxed = visible_boxes(page, spec["locator"])
    if not boxed:
        raise RuntimeError(f"{spec['name']}: no visible match for {spec['locator']}")

    if pick == "union":
        pad = spec.get("pad", 0)
        x0 = min(b["x"] for b, _ in boxed) - pad
        y0 = min(b["y"] for b, _ in boxed) - pad
        x1 = max(b["x"] + b["width"] for b, _ in boxed) + pad
        y1 = max(b["y"] + b["height"] for b, _ in boxed) + pad
        clip = {"x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0}
        page.screenshot(path=target, clip=clip)
        return clip

    boxed.sort(key=lambda t: t[0]["width"] * t[0]["height"])
    box, card = boxed[0] if pick == "smallest" else boxed[-1]
    card.screenshot(path=target, timeout=20000)
    return box


def capture_animation(page, spec, target):
    """Save an animated GIF of a card that is currently moving.

    Element screenshots come back as PNG bytes; a handful of them a few hundred ms apart is
    enough to show the pulsing icon and the position climbing in the badge.
    """
    from PIL import Image                       # only needed for the animated components

    boxed = visible_boxes(page, spec["locator"])
    if not boxed:
        raise RuntimeError(f"{spec['name']}: no visible match for {spec['locator']}")
    boxed.sort(key=lambda t: t[0]["width"] * t[0]["height"])
    box, card = boxed[0] if spec.get("pick", "smallest") == "smallest" else boxed[-1]

    interval = spec.get("interval_ms", 600)
    frames = []
    for _ in range(spec.get("frames", 10)):
        frames.append(Image.open(io.BytesIO(card.screenshot(timeout=20000))).convert("RGB"))
        page.wait_for_timeout(interval)

    palette = [f.quantize(colors=128) for f in frames]
    palette[0].save(target, save_all=True, append_images=palette[1:],
                    duration=interval, loop=0, optimize=True)
    return box


class Stage:
    """Puts entities in the state a component needs, and undoes it afterwards.

    Every entity is snapshotted the first time it is touched — state for a switch, position
    for a cover — and restored at the end, including when a capture raises.
    """

    def __init__(self, token, origin):
        self.token, self.origin = token, origin
        self.initial = {}

    def _get(self, entity):
        s = rest(self.token, f"/api/states/{entity}", origin=self.origin)
        return s["state"], s["attributes"].get("current_position")

    def _set(self, entity, want):
        if isinstance(want, int):
            rest(self.token, "/api/services/cover/set_cover_position",
                 {"entity_id": entity, "position": want}, origin=self.origin)
        else:
            domain = entity.split(".", 1)[0]
            rest(self.token, f"/api/services/{domain}/turn_{want}",
                 {"entity_id": entity}, origin=self.origin)

    def settle(self, entity, target, timeout=180):
        """Wait until the entity actually reached `target`.

        Waiting for "not moving" is not enough: a cover reports its old state for a second or
        two after the command, so the first poll would return immediately and the caller would
        capture — or report a restore — while the shutter is still travelling.
        """
        deadline = time.time() + timeout
        time.sleep(3)
        while time.time() < deadline:
            state, pos = self._get(entity)
            moving = state in ("opening", "closing")
            if isinstance(target, int):
                if not moving and pos is not None and abs(pos - target) <= 2:
                    return state, pos
            elif not moving and state == target:
                return state, pos
            time.sleep(2)
        state, pos = self._get(entity)
        print(f"  WARNING {entity} is {state} ({pos}%), wanted {target} after {timeout}s")
        return state, pos

    def want(self, entity, target, while_moving=False):
        if entity not in self.initial:
            self.initial[entity] = self._get(entity)
            was = self.initial[entity]
            print(f"  {entity} was {was[0]}" + (f" at {was[1]}%" if was[1] is not None else ""))
        state, pos = self._get(entity)
        if (isinstance(target, int) and pos == target) or state == target:
            return
        self._set(entity, target)
        if while_moving:
            time.sleep(2)                     # laisser l'animation demarrer
        else:
            self.settle(entity, target)
            time.sleep(3)                     # laisser le badge se stabiliser

    def restore(self):
        for entity, (state, pos) in self.initial.items():
            target = pos if pos is not None else state
            self._set(entity, target)
            now, back = self.settle(entity, target)
            detail = f" at {back}%" if back is not None else ""
            print(f"  {entity} restored to {now}{detail} (was {state})")


def capture_components(page, token, origin):
    out = os.path.join(OUT, "components")
    os.makedirs(out, exist_ok=True)
    stage = Stage(token, origin)
    view = None
    try:
        for spec in COMPONENTS:
            if ONLY and spec["name"] not in ONLY:
                continue
            setup = spec.get("setup")
            moving = bool(setup and setup.get("while_moving"))
            if setup and not moving:
                stage.want(setup["entity"], setup["want"])
                view = None                   # forcer un rechargement pour l'etat courant
            if spec["view"] != view:
                page.goto(HA_URL + spec["view"], wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(SETTLE_MS)
                view = spec["view"]
            if moving:
                # la page est deja chargee : le dashboard suit l'etat en direct, un rechargement
                # ici brulerait le trajet du volet pendant SETTLE_MS
                stage.want(setup["entity"], setup["want"], while_moving=True)
                view = None                   # l'etat aura change pour la suite
            if spec.get("frames"):
                target = os.path.join(out, f"{spec['name']}.gif")
                box = capture_animation(page, spec, target)
            else:
                target = os.path.join(out, f"{spec['name']}.png")
                box = capture_card(page, spec, target)
            print(f"  {target}  ({box['width']:.0f}x{box['height']:.0f} css)")
    finally:
        stage.restore()


def main():
    token = read_token()
    os.makedirs(OUT, exist_ok=True)

    map_host = MAP_HOST
    origin = HA_URL
    if SSH_RELAY:
        ip, _, port = SSH_TARGET.partition(":")
        SSHRelay(SSH_RELAY, (ip, int(port or 80)), RELAY_PORT).start()
        time.sleep(1)
        map_host = map_host or f"{HA_URL.split('://', 1)[1]}=127.0.0.1:{RELAY_PORT}"
        origin = f"http://127.0.0.1:{RELAY_PORT}"

    args = [f"--host-resolver-rules=MAP {map_host.replace('=', ' ')}"] if map_host else []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=args)
        ctx, page = new_page(browser, token, DESKTOP)
        page.goto(HA_URL + VIEWS[0][0], wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(SETTLE_MS)
        if "/auth/" in page.url:
            sys.exit("still on the login page — is the token still valid?")

        if WANT_VIEWS:
            print(f"=== desktop {DESKTOP['width']}x{DESKTOP['height']} @{SCALE}x ===")
            capture_views(page, "desktop")
        if WANT_COMPONENTS:
            print(f"=== components @{SCALE}x ===")
            capture_components(page, token, origin)
        ctx.close()

        if WANT_VIEWS and WANT_MOBILE:
            print(f"=== mobile {MOBILE['width']}x{MOBILE['height']} @{SCALE}x ===")
            ctx, page = new_page(browser, token, MOBILE, mobile=True)
            capture_views(page, "mobile", mobile=True)
            ctx.close()

        browser.close()

    print(f"\nDone — {OUT}")


if __name__ == "__main__":
    main()
