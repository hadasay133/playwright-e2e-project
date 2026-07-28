# 🧪 E2E Automation Framework

An End-to-End (E2E) test automation framework built with **Python**, **Playwright**, and **Pytest**, designed around the **Page Object Model (POM)** architecture.

---

## 🏗️ Framework Architecture (POM)

The project decouples UI interaction logic from test assertions by assigning each application view to a dedicated Page Object:

* **`BasePage`** – Base class encapsulating shared page interactions, wait conditions, and common navigation logic.
* **`LoginPage`** – Manages user authentication flows, modal interactions, and session handling.
* **`HomePage`** – Handles product search, filtering, and category navigation (*Phones*, *Laptops*, *Monitors*).
* **`ProductPage`** – Controls product details, cart additions, API response interception, and dynamic browser dialogs (Alerts).
* **`CartPage`** – Handles cart item verification, price calculations, item deletion, and checkout completion.

---

## ⚡ Key Features

* **Asynchronous Execution:** Leverages Playwright's `async_api` and `pytest-asyncio` for high performance and non-blocking operations.
* **Automated Failure Reporting:** Automatically captures screenshots upon test failures and embeds them into the generated HTML reports.
* **Modular Design:** Strictly separates test scenarios, assertions, and page interaction models for enhanced maintainability.

-
