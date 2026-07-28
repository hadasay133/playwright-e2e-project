import json
from pathlib import Path

import pytest
from playwright.async_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage


def load_test_data():
    """Load test data from a JSON file with safe type conversion."""
    json_path = Path(__file__).parent / "test_data.json"
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Convert data to values suitable for parameterization
    return [
        (
            item["user_name"],
            item["password"],
            item["query"],
            item["category"],
            float(item["max_price"]),
            int(item["limit"])
        )
        for item in data
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_name, password,query, category, max_price, limit",
    load_test_data()
)
async def test_search_items_by_name_under_price(page, base_url, user_name, password,query, category, max_price, limit):
    # 1. Initialize the Page Objects
    login_page = LoginPage(page)
    home_page = HomePage(page)

    # 2. Log in
    await home_page.navigate_to_page("Log in")
    await login_page.login(user_name, password)
    await expect(page.locator("#nameofuser")).to_contain_text(f"Welcome {user_name}", timeout=10000)

    # 3. Search and add items to the cart
    list_of_product = await home_page.search_items_by_name_under_price(query, max_price, limit)
    await home_page.add_items_to_cart(list_of_product)

    # 4. Navigate to the cart and verify the total
    cart_page = await home_page.navigate_to_page("cart")
    await cart_page.assert_cart_total_not_exceeds(max_price, len(list_of_product))

    # Teardown: Clean the cart
    await cart_page.clean_cart()