# step_defs/test_login_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import expect

# Подключаем все сценарии из feature-файла
scenarios('../features/login.feature')

@given("пользователь на странице логина")
def open_login_page(page):
    page.goto("https://std131001.test/Mein-Konto")

@when("вводит правильный логин и пароль")
def enter_valid_credentials(page):
    page.locator("input[name='kd_mail']").fill("alex@example.com")
    page.locator("input[name='kd_pwd']").fill("123")

@when("вводит правильный логин и неверный пароль")
def enter_valid_credentials(page):
    page.locator("input[name='kd_mail']").fill("alex@example.com")
    page.locator("input[name='kd_pwd']").fill("321")

@when(parsers.parse('нажимает кнопку "{css_selector}"'))
def click_button(page, css_selector):
    page.locator(css_selector).click()

@then(parsers.parse('пользователь в теле страницы видит текст "{text}"'))
def verify_page(page, text):
    # assert page.locator("body").to_contain_text(text, timeout=10000)
    expect(page.locator("body")).to_contain_text(text, timeout=10000)