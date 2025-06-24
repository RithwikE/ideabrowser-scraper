# scrape_ideas.py
from pathlib import Path
import random, time
from playwright.sync_api import sync_playwright

BASE_URL      = "https://www.ideabrowser.com/database?per_page=48&page={}"
STORAGE_STATE = "ideabrowser_storage.json"
OUT_DIR       = Path("idea_pages")
OUT_DIR.mkdir(exist_ok=True)

# same UA list → pick ONE to stay consistent with saved cookies
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
]
UA = random.choice(USER_AGENTS)
VIEWPORT = {"width": random.choice([1280, 1366, 1440]), "height": 800}

DELAY_BETWEEN_PAGES = (1.5, 3.5)  # seconds (min, max)

def scrape_single(page, idx: int) -> bool:
    page.goto(BASE_URL.format(idx), wait_until="networkidle")

    if page.locator("text=No results.").first.is_visible():
        return False

    # small scroll to mimic user viewing the grid (helps lazy images too)
    page.mouse.wheel(0, 2000)

    cards = page.locator("a.group")
    entries = []
    for i in range(cards.count()):
        card  = cards.nth(i)
        title = card.locator("h4").inner_text()
        desc  = card.locator("p").inner_text()
        entries.append(f"TITLE: {title}\n\nDESCRIPTION:\n{desc}\n\n---\n")

    (OUT_DIR / f"page_{idx}.txt").write_text("".join(entries), encoding="utf-8")
    print(f"📝  Saved {cards.count():>2} ideas from page {idx}")
    return True

def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,               # render like a real browser
            args=["--disable-blink-features=AutomationControlled"],
        )
        ctx = browser.new_context(
            storage_state       = STORAGE_STATE,
            user_agent          = UA,
            viewport            = VIEWPORT,
            locale              = "en-US,en;q=0.9",
            device_scale_factor = 1,
        )
        page = ctx.new_page()

        page_no = 1
        while scrape_single(page, page_no):
            time.sleep(random.uniform(*DELAY_BETWEEN_PAGES))  # human pause
            page_no += 1

        browser.close()
        print("🎉  Done.")

if __name__ == "__main__":
    main()
