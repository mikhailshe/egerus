import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def parse_fipi_russian_bank(output_csv="fipi_russian_tasks.csv"):
    print("Начало работы парсера...")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    try:
        print("Запускаем веб-драйвер...")
        service = Service('/Users/mikhailshevnin/Downloads/chromedriver_mac_arm64/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Веб-драйвер успешно запущен.")
    except Exception as e:
        print(f"Ошибка при запуске веб-драйвера: {e}")
        return

    base_url = "https://fipi.ru/ege/demoversii-specifikacii-kodifikatory"
    bank_url = "https://fipi.ru/bank-zadaniy-ege"

    try:
        print("Открываем банк заданий...")
        driver.get(bank_url)
        time.sleep(3)

        print("Пытаемся перейти в раздел 'Русский язык'...")
        subject_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Русский язык")
        subject_link.click()
        time.sleep(3)
    except Exception as e:
        print(f"Ошибка при открытии страницы или переходе в раздел: {e}")
        driver.quit()
        return

    tasks_data = []

    for task_num in range(1, 28):
        try:
            print(f"Парсинг задания {task_num}...")
            dropdown = driver.find_element(By.ID, "edit-name")
            dropdown.clear()
            dropdown.send_keys(str(task_num))
            search_btn = driver.find_element(By.ID, "edit-submit-task-bank")
            search_btn.click()
            time.sleep(2)

            questions = driver.find_elements(By.CSS_SELECTOR, ".task-content")
            answers = driver.find_elements(By.CSS_SELECTOR, ".task-answer")

            print(f"Найдено {len(questions)} вопросов и {len(answers)} ответов.")

            for q, a in zip(questions, answers):
                question_text = q.text.strip().replace("\n", " ")
                answer_text = a.text.strip().replace("Ответ: ", "")
                tasks_data.append({
                    "task_type": task_num,
                    "question_text": question_text,
                    "correct_answer": answer_text
                })
        except Exception as e:
            print(f"Ошибка при парсинге задания {task_num}: {e}")
            continue

    driver.quit()

    if not tasks_data:
        print("Задания не были получены.")
        return

    print(f"Собрано {len(tasks_data)} заданий.")

    try:
        with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["task_type", "question_text", "correct_answer"])
            writer.writeheader()
            writer.writerows(tasks_data)
        print(f"Сохранено заданий: {len(tasks_data)} в файл {output_csv}")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
if __name__ == "__main__":
    parse_fipi_russian_bank()
