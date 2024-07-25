from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import argparse

logit_var = ""
passwd_var = ""

# Время ожидания в секундах
wait_time_seconds = 10 * 60  # 10 минут
# Интервал проверки статуса в секундах
check_interval = 10
# Настройка аргументов командной строки
parser = argparse.ArgumentParser(description='Скрипт для создания и скачивания отчета.')
parser.add_argument('date_value', type=str, help='Дата в формате "ДД.ММ.ГГГГ - ДД.ММ.ГГГГ"')
args = parser.parse_args()
date_value = args.date_value #'10.06.2024 - 15.07.2024'

# Путь к вашему chromedriver
chrome_driver_path = '/home/daniel/Загрузки/1/chromedriver-linux64/chromedriver'
# Путь к исполняемому файлу Chrome
chrome_binary_path = '/home/daniel/Загрузки/1/chrome-linux64/chrome'
# Путь для сохранения файлов
download_dir = '/home/daniel/projekts/Python/files/'
# Создание папки для загрузок, если она не существует
os.makedirs(download_dir, exist_ok=True)

# Настройки для сохранения файлов
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}

# Настройки для Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Опционально, для запуска без графического интерфейса
chrome_options.binary_location = chrome_binary_path
chrome_options.add_experimental_option("prefs", prefs)

# Запуск браузера
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

def clickButton(x):
    create_report_button_final = driver.find_element(By.CSS_SELECTOR, x)
    create_report_button_final.click()
    time.sleep(1)


try:
    # Открытие страницы входа
    driver.get("https://strij.cloud/auth/login")
    print("Страница входа загружена")

    # Ожидание загрузки страницы и поиск поля логина
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Введите ваш логин']"))
    )
    print("Поле логина найдено")
    email_field = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Введите ваш логин']")
    email_field.send_keys(logit_var)
    print("Логин введен")

    # Поиск поля пароля по плейсхолдеру и ввод значения
    password_field = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Введите ваш пароль']")
    password_field.send_keys(passwd_var)
    print("Пароль введен")

    # Отправка формы (нажатие Enter)
    password_field.send_keys(Keys.RETURN)
    print("Форма отправлена")

    # Ожидание загрузки страницы после входа (изменение URL или ожидание элемента на новой странице)
    WebDriverWait(driver, 30).until(
        EC.url_changes("https://strij.cloud/auth/login")
    )
    print("Вход выполнен, URL изменился")

    # Переход на страницу объектов
    driver.get("https://strij.cloud/geo/55126/building")
    print("Перешел на страницу объекта Усачева д. 17")

    # Временная задержка для загрузки элементов
    time.sleep(3)

    # Вывод текущего HTML кода страницы для отладки
    page_source = driver.page_source
    print(page_source)

    # Ожидание загрузки страницы объекта и проверка наличия элемента
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".sj2-btn.sj2-btn-primary.sj2-cursor-pointer.report-btn-top"))
    )
    print("Кнопка 'Создать отчет' найдена")

    # Поиск и нажатие на кнопку "Создать отчет"
    clickButton(".sj2-btn.sj2-btn-primary.sj2-cursor-pointer.report-btn-top")
    print("Нажата кнопка 'Создать отчет'")

    # Временная задержка для загрузки модального окна
    time.sleep(2)

    # Ожидание появления модального окна
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.modal-body"))
    )
    print("Модальное окно 'Создание отчета' появилось")

    # Ожидание появления поля даты
    date_range_selector = "input.pl-3.pr-3.text-center.sj2-datepicker"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, date_range_selector))
    )
    print("Поле ввода даты найдено")

    # Поиск поля даты и ввод даты
    date_range_field = driver.find_element(By.CSS_SELECTOR, date_range_selector)

    # Использование JavaScript для ввода даты и симуляция события change
    driver.execute_script(f"arguments[0].value = '{date_value}'; arguments[0].dispatchEvent(new Event('change'));", date_range_field)
    print(f"Дата начала и окончания введены и применены с использованием JavaScript: {date_value}")

    time.sleep(1)

    # Нажатие на кнопку "Далее"
    next_button = driver.find_element(By.XPATH, "/html/body/modal-container/div/div/div/div/div[3]/div/div/div[2]")
    next_button.click()
    print("Нажата кнопка 'Далее'")

    time.sleep(1)

    # Нажатие на радиокнопку "Вода"
    clickButton("label[for='water']")
    print("Нажата радиокнопка 'Вода'")

    # Нажатие на кнопку "Конфигурации"
    clickButton("body > modal-container > div > div > div > div > div.modal-footer.pl-0.pr-0.bg-platinum > div > div > div.ml-3.btn.sj2-btn.line-height-normal.sj2-line-medium.font-weight-medium")
    print("Нажата кнопка 'Конфигурации'")

    # Селекторы для конфигураци
    configSelectors = [
        # # ХВС потр
        "body > modal-container > div > div > div > div > div.modal-body.h-100.pt-0.mb-4 > div > div:nth-child(11) > label > div.checkboxcontainer__checkbox",
        # #Последнее сообщение
        "body > modal-container > div > div > div > div > div.modal-body.h-100.pt-0.mb-4 > div > div:nth-child(12) > label > div.checkboxcontainer__checkbox",
        # #Внимание
        "body > modal-container > div > div > div > div > div.modal-body.h-100.pt-0.mb-4 > div > div:nth-child(13) > label > div.checkboxcontainer__checkbox",
        # # ГВС потр
        "body > modal-container > div > div > div > div > div.modal-body.h-100.pt-0.mb-4 > div > div:nth-child(19) > label > div.checkboxcontainer__checkbox",
        # #Последнее сообщение
        "body > modal-container > div > div > div > div > div.modal-body.h-100.pt-0.mb-4 > div > div:nth-child(20) > label > div.checkboxcontainer__checkbox",
        # #Внимание
        "body > modal-container > div > div > div > div > div.modal-body.h-100.pt-0.mb-4 > div > div:nth-child(21) > label > div.checkboxcontainer__checkbox",
        #Примечание
        "body > modal-container > div > div > div > div > div.modal-body.h-100.pt-0.mb-4 > div > div:nth-child(22) > label > div.checkboxcontainer__checkbox",
        ]

    for configSelector in configSelectors:
        clickButton(configSelector)

    # Нажатие на кнопку "Создать отчет"
    clickButton("body > modal-container > div > div > div > div > div.modal-footer.pl-0.pr-0.bg-platinum > div > div > button")
    print("Нажата кнопка 'Создать отчет'")

    time.sleep(2)

    # Переход на страницу отчетов
    driver.get("https://strij.cloud/report/list/page")
    print("Переход на страницу отчетов")

    time.sleep(5)

    status_selector = "div.col-1.d-flex.align-items-center.justify-content-start.pr-0 > div.d-flex"
    # Проверка статуса в течение 10 минут
    start_time = time.time()
    status_text = ""

    while time.time() - start_time < wait_time_seconds:
        status_element = driver.find_element(By.CSS_SELECTOR, status_selector)
        status_text = status_element.text
        print(f"Текущий статус элемента: {status_text}")
        if status_text == "готов":
            print("Статус 'готов' подтвержден, продолжаем")
            break

        # Обновление страницы
        driver.refresh()
        time.sleep(check_interval)

    if status_text == "готов":
        # Нажать на кнопку скачать отчет
        clickButton("a.d-flex[target='_blank']")
        print("Нажата кнопка 'Скачать отчет'")
    else:
        print("Статус не изменился на 'готов' в течение 10 минут, скрипт завершен")

finally:
    # Закрытие браузера
    driver.quit()
    print("Браузер закрыт")
