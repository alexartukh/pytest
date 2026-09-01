# features/login.feature
Feature: Вход в аккаунт

  Scenario: Успешный вход с корректными данными
    Given пользователь на странице логина
    When вводит правильный логин и пароль
    And нажимает кнопку "input.loginBtn"
    Then пользователь в теле страницы видит текст "Bestellungen einsehen"

  Scenario: Неверный пароль
    Given пользователь на странице логина
    When вводит правильный логин и неверный пароль
    And нажимает кнопку "input.loginBtn"
    Then пользователь в теле страницы видит текст "das Passwort gehört nicht zu dieser E-Mail Adresse"
