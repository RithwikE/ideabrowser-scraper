# save_state.py
# rithwik.e.rabelly@gmail.com

from pathlib import Path
from random   import choice
from playwright.sync_api import sync_playwright

STORAGE_FILE = Path("ideabrowser_storage.json")

# Pick one modern Chrome UA (or roll your own list)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
]
UA = choice(USER_AGENTS)

VIEWPORT_W, VIEWPORT_H = (1280, 800)           # normal laptop size

def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ctx = browser.new_context(
            user_agent           = UA,
            viewport             = {"width": VIEWPORT_W, "height": VIEWPORT_H},
            locale               = "en-US,en;q=0.9",
            device_scale_factor  = 1,
            java_script_enabled  = True,
            ignore_https_errors  = False,
        )

        page = ctx.new_page()
        page.goto("https://www.ideabrowser.com/login")

        print(
            f"\n▶  UA in use: {UA}\n"
            "▶  Log in in the browser window, then press ENTER here…"
        )
        input()
        ctx.storage_state(path=STORAGE_FILE)
        print(f"✅ Session stored → {STORAGE_FILE.resolve()}")
        browser.close()

if __name__ == "__main__":
    main()
