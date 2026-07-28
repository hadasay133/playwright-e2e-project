from playwright.async_api import Playwright, Browser

from infrastracture.browser_type import BrowserType


class BrowserFactory:
    @staticmethod
    async def create_browser(
        playwright: Playwright,
        browser_name: str = BrowserType.CHROMIUM.value,
        headless: bool = True
    ) -> Browser:
        match browser_name.lower():
            case BrowserType.CHROMIUM.value:
                launcher = playwright.chromium
            case BrowserType.FIREFOX.value:
                launcher = playwright.firefox
            case BrowserType.WEBKIT.value:
                launcher = playwright.webkit
            case _:
                supported = [b.value for b in BrowserType]
                raise ValueError(
                    f"Unsupported browser: '{browser_name}'. "
                    f"Supported browsers: {supported}"
                )

        return await launcher.launch(headless=headless)