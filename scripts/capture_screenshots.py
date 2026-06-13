"""
Screenshot capture script for ha-glass-dashboard
Captures each dashboard view in desktop and mobile viewports
"""
import asyncio
import os
from playwright.async_api import async_playwright

HA_URL = "http://home.home.arpa:8123"
OUTPUT_DIR = os.path.expanduser("~/ha-glass-dashboard/docs/screenshots")

# Views to capture (path, filename_prefix, description)
VIEWS = [
    ("/lovelace/0", "home", "Home view with weather background"),
    ("/lovelace/1", "meteo", "Weather view with badges"),
    ("/lovelace/2", "remote", "Remote control"),
    ("/lovelace/3", "programmation", "Scheduling view"),
    ("/lovelace/4", "proxmox", "Proxmox infrastructure"),
    ("/lovelace/5", "routeurs", "Network/routers"),
    ("/lovelace/6", "nas", "NAS/Storage"),
]

# Viewports
DESKTOP = {"width": 1920, "height": 1080}
MOBILE = {"width": 390, "height": 844}  # iPhone 14 Pro


async def capture_screenshots():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Desktop captures
        print("=== Desktop captures (1920x1080) ===")
        context = await browser.new_context(
            viewport=DESKTOP,
            ignore_https_errors=True,
        )
        page = await context.new_page()
        
        # Login to HA
        await page.goto(f"{HA_URL}/auth/authorize?response_type=code&client_id={HA_URL}/")
        await page.wait_for_load_state("networkidle")
        
        # Check if we need to login
        if "auth" in page.url:
            print("Login required - trying local auth...")
            # HA trusted networks should auto-login from LAN
            # If not, we need credentials
            try:
                await page.goto(HA_URL, wait_until="networkidle", timeout=10000)
                await page.wait_for_selector("home-assistant", timeout=10000)
            except:
                print("ERROR: Cannot auto-login. Configure trusted_networks in HA or provide credentials.")
                print("Add to configuration.yaml:")
                print("  homeassistant:")
                print("    auth_providers:")
                print("      - type: trusted_networks")
                print("        trusted_networks:")
                print("          - 192.168.20.0/24")
                await browser.close()
                return
        
        # Wait for dashboard to fully load
        await page.wait_for_timeout(3000)
        
        for path, name, desc in VIEWS:
            url = f"{HA_URL}{path}"
            print(f"  Capturing {name} ({desc})...")
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(2000)  # Wait for card-mod to render
            
            filepath = os.path.join(OUTPUT_DIR, f"{name}-desktop.png")
            await page.screenshot(path=filepath, full_page=False)
            print(f"    -> {filepath}")
        
        await context.close()
        
        # Mobile captures
        print("\n=== Mobile captures (390x844) ===")
        context = await browser.new_context(
            viewport=MOBILE,
            ignore_https_errors=True,
            is_mobile=True,
        )
        page = await context.new_page()
        await page.goto(HA_URL, wait_until="networkidle", timeout=15000)
        await page.wait_for_timeout(3000)
        
        for path, name, desc in VIEWS:
            url = f"{HA_URL}{path}"
            print(f"  Capturing {name} mobile...")
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(2000)
            
            filepath = os.path.join(OUTPUT_DIR, f"{name}-mobile.png")
            await page.screenshot(path=filepath, full_page=False)
            print(f"    -> {filepath}")
        
        await context.close()
        await browser.close()
    
    print(f"\nDone! Screenshots saved to {OUTPUT_DIR}")
    print("Files:")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            size = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f} ({size//1024}KB)")


if __name__ == "__main__":
    asyncio.run(capture_screenshots())
