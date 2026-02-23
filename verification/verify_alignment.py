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

        # Check joysticks position
        move_joystick = await page.query_selector("#move-joystick-container")
        cam_joystick = await page.query_selector("#joystick-container")

        move_rect = await move_joystick.bounding_box()
        cam_rect = await cam_joystick.bounding_box()

        print(f"Move joystick Y: {move_rect['y']}")
        print(f"Cam joystick Y: {cam_rect['y']}")

        diff = abs(move_rect['y'] - cam_rect['y'])
        if diff < 1:
            print(f"SUCCESS: Joysticks are aligned (diff={diff}).")
        else:
            print(f"FAILURE: Joysticks are NOT aligned (diff={diff}).")

        await page.screenshot(path="verification/alignment_screenshot.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
