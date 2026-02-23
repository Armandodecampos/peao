import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # Set viewport size to mobile-like
        await page.set_viewport_size({"width": 1280, "height": 720})

        # Absolute path to index.htm
        file_path = "file://" + os.path.abspath("index.htm")
        await page.goto(file_path)
        await asyncio.sleep(2)  # Wait for loading

        # Click "NOVO JOGO" to get to the start screen
        await page.click("button:has-text('NOVO JOGO')")
        await asyncio.sleep(1)

        # Click on the coin item to open the shop
        await page.click("#top-stats-bar .stat-item:has-text('MOEDAS')")
        await asyncio.sleep(1)

        # Take a screenshot of the shop
        await page.screenshot(path="verification/shop_final.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
