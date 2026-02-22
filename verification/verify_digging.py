import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        # Get absolute path
        path = os.path.abspath("index.htm")
        await page.goto(f"file://{path}")

        print("Waiting for start screen...")
        await page.wait_for_selector("#start-screen", state="visible", timeout=10000)

        print("Clicking INICIAR...")
        await page.click("#btn-start-battle")

        print("Waiting for countdown (5s)...")
        await asyncio.sleep(5)

        print("Waiting for game UI...")
        await page.wait_for_selector("#terras-ui", state="visible", timeout=10000)

        # Verify Terras is 0
        terras_text = await page.inner_text("#terras-ui")
        print(f"Initial terras: {terras_text}")

        print("Pressing 'e' to dig...")
        await page.keyboard.down("e")
        await asyncio.sleep(0.1)
        await page.keyboard.up("e")

        # Wait for digging UI
        try:
            await page.wait_for_selector("#dig-ui", state="visible", timeout=5000)
            await page.screenshot(path="verification/digging.png")
            print("Digging UI visible")
        except:
            print("Digging UI NOT visible!")
            await page.screenshot(path="verification/dig_failed.png")

        # Wait for digging to complete (2s + buffer)
        await asyncio.sleep(3)

        # Check Terras again
        terras_text = await page.inner_text("#terras-ui")
        print(f"Final terras: {terras_text}")
        await page.screenshot(path="verification/dig_complete.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
