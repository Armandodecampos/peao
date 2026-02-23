import asyncio
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size({"width": 800, "height": 600})

        import os
        path = os.path.abspath("index.htm")
        await page.goto(f"file://{path}")
        await page.wait_for_selector("#loading-screen", state="hidden")
        await page.click("#btn-start-battle")
        await asyncio.sleep(5)

        # Check jump button position relative to right joystick
        jump_btn = await page.query_selector("#ctrl-jump")
        cam_joystick = await page.query_selector("#joystick-container")

        jump_rect = await jump_btn.bounding_box()
        cam_rect = await cam_joystick.bounding_box()

        print(f"Jump button: {jump_rect}")
        print(f"Cam joystick: {cam_rect}")

        if jump_rect['y'] < cam_rect['y']:
            print("SUCCESS: Jump button is above the camera joystick.")
        else:
            print("FAILURE: Jump button is NOT above the camera joystick.")

        if jump_rect['x'] > 400:
            print("SUCCESS: Jump button is on the right side.")
        else:
            print("FAILURE: Jump button is NOT on the right side.")

        await page.screenshot(path="verification/new_layout_screenshot.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
