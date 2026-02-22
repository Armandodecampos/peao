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

        print("Starting digging...")
        await page.keyboard.press("e")

        for i in range(15):
            await asyncio.sleep(1)
            progress = await page.evaluate("document.getElementById('dig-progress-bar').style.width")
            terras = await page.inner_text("#terras-ui")
            print(f"Time {i+1}s: Progress {progress}, {terras}")
            if terras == "TERRAS: 20":
                print("Digging completed!")
                break

        await page.screenshot(path="verification/dig_final_long.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
