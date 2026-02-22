import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        path = os.path.abspath("index.htm")
        await page.goto(f"file://{path}")

        await page.wait_for_selector("#start-screen", state="visible", timeout=10000)
        await page.click("#btn-start-battle")

        # Wait for countdown
        await asyncio.sleep(6)

        print("Initial terras:", await page.inner_text("#terras-ui"))

        print("Starting digging...")
        await page.keyboard.press("e")

        await asyncio.sleep(1)
        await page.screenshot(path="verification/digging_mid.png")
        progress_width = await page.evaluate("document.getElementById('dig-progress-bar').style.width")
        print(f"Progress width after 1s: {progress_width}")

        await asyncio.sleep(3)
        await page.screenshot(path="verification/digging_after_4s.png")

        terras_text = await page.inner_text("#terras-ui")
        print(f"Final terras: {terras_text}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
