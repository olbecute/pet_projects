# Проверка установки необходимых библиотек
try:
    import requests
    import pandas as pd
    from time import sleep, time
    from datetime import datetime
    print("Библиотеки 'requests' и 'pandas' установлены!")
    print(f"Версия requests: {requests.__version__}")
    print(f"Версия pandas: {pd.__version__}")
except ImportError as e:
    print(f"Ошибка: {e}. Библиотека не установлена.")
    print("Установите библиотеки командой: pip install requests pandas")
    exit()

def get_vacancy_details(vacancy_id: str) -> dict:
    """Получает детальную информацию о вакансии (навыки и описание)"""
    url = f"https://api.hh.ru/vacancies/{vacancy_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "Ключевые навыки": ", ".join(skill.get("name", "") for skill in data.get("key_skills", [])),
                "Описание": data.get("description", "").replace("\n", " ").strip()
            }
    except Exception as e:
        print(f"Ошибка при получении деталей вакансии {vacancy_id}: {str(e)}")
    return {"Ключевые навыки": "", "Описание": ""}

def get_vacancies(query: str, max_pages: int = 20) -> pd.DataFrame:
    """
    Собирает вакансии с hh.ru по ключевому запросу.
    
    :param query: Поисковый запрос (например, "data scientist")
    :param max_pages: Максимальное количество страниц (на каждой ~50 вакансий)
    :return: DataFrame с вакансиями
    """
    base_url = "https://api.hh.ru/vacancies"
    params = {
        "text": query,
        "area": 113,  # 1 — Москва, можно изменить (2 — СПб, 113 — Россия)
        "per_page": 50,  # Количество вакансий на странице
        "page": 0
    }
    
    all_vacancies = []
    total_start_time = time()
    
    for page in range(max_pages):
        page_start_time = time()
        params["page"] = page
        
        try:
            response = requests.get(base_url, params=params, timeout=10)
            if response.status_code != 200:
                print(f"Ошибка {response.status_code} на странице {page + 1}")
                break
                
            data = response.json()
            vacancies = data.get("items", [])
            
            if not vacancies:
                print(f"На странице {page + 1} нет вакансий. Прерываем.")
                break
            
            for i, vacancy in enumerate(vacancies, 1):
                try:
                    # Основная информация
                    vacancy_info = {
                        "ID вакансии": vacancy.get("id"),
                        "Название": vacancy.get("name"),
                        "Компания": vacancy.get("employer", {}).get("name"),
                        "Зарплата (от)": vacancy.get("salary", {}).get("from") if vacancy.get("salary") else None,
                        "Зарплата (до)": vacancy.get("salary", {}).get("to") if vacancy.get("salary") else None,
                        "Валюта": vacancy.get("salary", {}).get("currency") if vacancy.get("salary") else None,
                        "Город": vacancy.get("area", {}).get("name"),
                        "Опыт": vacancy.get("experience", {}).get("name"),
                        "Тип занятости": vacancy.get("employment", {}).get("name"),
                        "Дата публикации": vacancy.get("published_at"),
                        "Ссылка": vacancy.get("alternate_url"),
                        "Время обработки страницы": None  # Заполним позже
                    }
                    
                    # Получаем детали вакансии (навыки и описание)
                    vacancy_id = vacancy.get("id")
                    if vacancy_id:
                        details = get_vacancy_details(vacancy_id)
                        vacancy_info.update(details)
                    
                    all_vacancies.append(vacancy_info)
                    
                    # Небольшая задержка между запросами деталей вакансий
                    if i % 5 == 0:
                        sleep(0.1)
                
                except Exception as e:
                    print(f"Ошибка обработки вакансии {vacancy.get('id')}: {str(e)}")
            
            page_time = time() - page_start_time
            # Добавляем время обработки ко всем вакансиям текущей страницы
            for v in all_vacancies[-len(vacancies):]:
                v["Время обработки страницы"] = f"{page_time:.2f} сек"
            
            print(f"Страница {page + 1}/{max_pages} обработана за {page_time:.2f} сек. Вакансий: {len(vacancies)}")
            sleep(0.5)  # Задержка между страницами
            
        except Exception as e:
            print(f"Ошибка при обработке страницы {page + 1}: {str(e)}")
            break
    
    total_time = time() - total_start_time
    print(f"Всего обработано страниц: {page + 1}, вакансий: {len(all_vacancies)}")
    print(f"Общее время сбора: {total_time:.2f} секунд")
    
    return pd.DataFrame(all_vacancies)

# Собираем вакансии по трём запросам
queries = ["data science", "аналитик данных", "machine learning engineer"]
df_all = pd.DataFrame()

for query in queries:
    print(f"\n=== Начало сбора по запросу: '{query}' ===")
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Время начала: {start_time}")
    
    df = get_vacancies(query, max_pages=10)  # 10 страницы (~500 вакансий)
    df["Запрос"] = query  # Добавляем столбец с запросом
    df["Время начала сбора"] = start_time
    df["Время окончания сбора"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    df_all = pd.concat([df_all, df], ignore_index=True)

# Сохраняем в CSV
output_filename = f"hh_vacancies_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
df_all.to_csv(output_filename, index=False, encoding="utf-8-sig")
print(f"\nГотово! Данные сохранены в {output_filename}")
print(f"Всего собрано вакансий: {len(df_all)}")