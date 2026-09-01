import re
import uuid
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from db_checker import check_order

# Настройка контекста браузера (аналог ContextOptions() в C#)
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": True,
    }


def attach_text(name: str, body: str):
    """Аналог AttachText из C# — сохраняет текст во вложение теста."""
    attachments_dir = Path("attachments")
    attachments_dir.mkdir(exist_ok=True)
    file_path = attachments_dir / f"{name}_{uuid.uuid4().hex}.txt"
    file_path.write_text(body, encoding="utf-8")
    return file_path


class TestPlaceOrder:

    @pytest.mark.skip(reason="IGNORE")
    def test_register_user_failed(self, page: Page):
        page.goto("https://std131001.test/Mein-Konto", wait_until="networkidle")

        page.locator("a:has-text('Konto anlegen')").click()
        expect(page.locator("body")).to_contain_text("Daten bearbeiten", timeout=10000)

        page.locator("#kd_vorname").fill("ALEX")
        page.locator("#kd_nachname").fill("ARTUKH")

        # SS
        page.screenshot(path="screenshots/registration-page-before.png")

        expect(page.locator("body")).not_to_contain_text(
            "Bitte füllen Sie alle markierten Pflichtfelder aus!", timeout=10000
        )

        page.locator("input[name='button_submit']").click(timeout=10000)

        expect(page.locator("body")).to_contain_text(
            "Bitte füllen Sie alle markierten Pflichtfelder aus!", timeout=10000
        )

        # SS
        page.screenshot(path="screenshots/registration-page-after.png")

    @pytest.mark.skip(reason="IGNORE")
    def test_place_order(self, page: Page, request):
        # лог для отчёта (аналог testInfo.attach с текстом)
        path = attach_text("setTimeout", "Global timeout = 60000")
        request.node.user_properties.append(("setTimeout", str(path)))

        # my account
        page.goto("https://std131001.test/Mein-Konto", wait_until="networkidle")
        page.locator("input[name='kd_mail']").fill("alex@example.com")
        page.locator("input[name='kd_pwd']").fill("123")
        page.locator("input.loginBtn").click()
        expect(page.locator("body")).to_contain_text("Bestellungen einsehen", timeout=10000)

        # home page
        page.goto("https://std131001.test/")
        page.locator("a[alt='p1']").click()

        # PDP
        expect(page.locator("body")).to_contain_text("In den Warenkorb", timeout=10000)
        page.locator("input[value='In den Warenkorb']").click()
        page.locator("a[alt='zum Warenkorb']").wait_for(state="visible")
        page.locator("a[alt='zum Warenkorb']").click(timeout=10000)

        # WK
        page.locator("input[name='button_submit']").wait_for(state="visible")
        page.locator("input[name='dhl_agree_checkbox']").check()
        page.locator("input[name='button_submit']").click(timeout=10000)
        page.wait_for_timeout(4000)

        # step 3
        expect(page.locator("body")).to_contain_text("Adresse und Lieferung", timeout=10000)
        page.locator("input[name='best_vorname']").wait_for(state="visible")
        page.locator("input[name='button_submit']").click(timeout=10000)
        page.wait_for_timeout(4000)

        # step 4
        expect(page.locator("body")).to_contain_text("Zahlungsart und Versand", timeout=10000)
        page.locator("input[name='bestagb']").wait_for(state="visible")
        page.locator("input[name='bestagb']").check()
        page.locator("input[name='button_submit']").click(timeout=10000)
        page.wait_for_timeout(4000)

        # step 5
        expect(page.locator("body")).to_contain_text(
            "Ein letzter Check - bitte kontrollieren Sie Ihre Angaben vor dem Absenden nochmals auf ihre Richtigkeit.",
            timeout=10000,
        )
        page.locator("input[value='zahlungspflichtig bestellen']").wait_for(state="visible")
        page.locator("input[value='zahlungspflichtig bestellen']").click(timeout=10000)
        page.wait_for_timeout(10000)

        # thank you page
        expect(page.locator("body")).to_contain_text("Vielen Dank für Ihre Bestellung", timeout=10000)

        heading_text = page.locator("h5[role='heading']").inner_text()
        match = re.search(r"\d+$", heading_text)
        if match:
            order_number = match.group()

            path = attach_text("orderNumber", f"Order Number = {order_number}")
            request.node.user_properties.append(("orderNumber", str(path)))

            details = check_order(order_number)

            path = attach_text("orderDetails", f"Order Details = {details}")
            request.node.user_properties.append(("orderDetails", str(path)))

