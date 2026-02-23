import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        file_path = "file://" + os.path.abspath("index.htm")
        await page.goto(file_path)
        await asyncio.sleep(2)

        # Verify NOVO JOGO confirmation and navigate to start-screen
        # Set up a listener for the dialog
        async def handle_dialog(dialog):
            print(f"Confirmation dialog text: {dialog.message}")
            await dialog.accept()

        page.on("dialog", lambda dialog: asyncio.create_task(handle_dialog(dialog)))

        # Click NOVO JOGO
        await page.click("button:has-text('NOVO JOGO')")
        await asyncio.sleep(2)

        # Check if we are on start-screen
        start_screen_visible = await page.is_visible("#start-screen")
        print(f"Start screen visible: {start_screen_visible}")

        if start_screen_visible:
            # Try to click MOEDAS
            # Note: The element might be hidden if modals are open, but they are not yet.
            # We use force=True if needed but better to check why it's not visible
            # Maybe it needs some time or it's outside viewport?
            await page.click("#top-stats-bar .stat-item:has-text('MOEDAS')")
            await asyncio.sleep(1)
            shop_visible = await page.is_visible("#shop-modal")
            print(f"Shop visible after click: {shop_visible}")
            await page.screenshot(path="verification/shop_open.png")

            # Close shop
            await page.click("#shop-modal button:has-text('VOLTAR')")
            await asyncio.sleep(1)

            # Try to click PONTOS
            await page.click("#top-stats-bar .stat-item:has-text('PONTOS')")
            await asyncio.sleep(1)
            skills_visible = await page.is_visible("#skills-modal")
            print(f"Skills visible after click: {skills_visible}")
            await page.screenshot(path="verification/skills_open.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
