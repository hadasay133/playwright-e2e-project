import base64
import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
from infrastracture.browser_type import BrowserType


def pytest_addoption(parser):
    parser.addoption(
        "--browser-name",
        action="store",
        default=BrowserType.CHROMIUM.value,
        help="Browser to run tests on: chromium, firefox, webkit"
    )


@pytest.fixture(scope="session")
def base_url():
    return "https://www.demoblaze.com/index.html#"


@pytest_asyncio.fixture
async def page(request, base_url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )

        context = await browser.new_context(no_viewport=True)
        page = await context.new_page()

        page.set_default_timeout(5000)
        page.set_default_navigation_timeout(10000)

        await page.goto(base_url)
        yield page

        await context.close()
        await browser.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            try:
                import asyncio
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    screenshot_bytes = loop.run_until_complete(page.screenshot())
                else:
                    screenshot_bytes = asyncio.run(page.screenshot())

                encoded = base64.b64encode(screenshot_bytes).decode("utf-8")
                html = f'<div><img src="data:image/png;base64,{encoded}" style="width:600px; border:1px solid red;" /></div>'
                extra.append(pytest_html.extras.html(html))
            except Exception as e:
                print(f"Failed to take screenshot for HTML report: {e}")

    report.extra = extra