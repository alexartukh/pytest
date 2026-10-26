# DRAFT — Playwright + Pytest

> **Status: early learning draft (August–September 2026).**
> Kept as a record of my progress. My current, cleaner end-to-end work is in
> [alexartukh/playwright](https://github.com/alexartukh/playwright) — Playwright + TypeScript with page objects, fixtures, API calls, network mocking and CI.

## What it is

The same order scenario as in my TypeScript and C# drafts, written in **Python with pytest**,
plus a first try of **BDD with Gherkin** (`pytest-bdd`). The tests run against a locally hosted
e-commerce shop (CosmoShop, German storefront) in a Vagrant virtual machine.

## Contents

| File | What it shows |
|---|---|
| `shop_test.py` | Full order flow (login → product → cart → checkout → thank-you page) and a negative registration test. After the order, the order number is checked in the database. |
| `db_checker.py` | Opens an **SSH tunnel** to the shop VM (`sshtunnel`) and queries **MySQL** (`pymysql`) to confirm the order was stored. |
| `features/login.feature` | Gherkin scenarios: successful login and wrong password. |
| `step_defs/test_login_steps.py` | Step definitions for the feature file, including parameterized steps (`parsers.parse`). |
| `conftest.py` | Shared fixture override: browser context that ignores HTTPS errors of the local VM. |

## What is interesting here

- **UI + database check in one test**: what the user sees is verified against what the backend actually saved.
- **BDD**: readable scenarios in Gherkin, mapped to Python step functions.
- pytest-playwright fixtures (`page`, `browser_context_args`) and report data via `user_properties`.

## Known limitations (why it is a draft)

- Runs only against my local shop VM.
- Fixed waits, `networkidle` navigation and assertions on the whole `body`; selectors depend on German UI texts.
- Some tests are temporarily skipped; no page objects.

## Running (requires the local shop VM)

```bash
pip install -r requirements.txt
playwright install
```

Connection settings for the database check come from environment variables (nothing secret is stored in the repository).
PowerShell example:

```powershell
$env:SSH_KEY_PATH = "C:\path\to\.vagrant\machines\default\virtualbox\private_key"
$env:DB_USER      = "..."
$env:DB_PASSWORD  = "..."
$env:DB_NAME      = "..."
# optional, defaults shown: SSH_HOST=127.0.0.1, SSH_PORT=2222, SSH_USER=vagrant, DB_HOST=127.0.0.1, DB_PORT=3306

pytest                 # all tests
pytest step_defs       # only the BDD login scenarios
```

## Stack

Python · pytest · pytest-playwright · pytest-bdd · sshtunnel · PyMySQL
