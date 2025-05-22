
# JobInsight: Анализ рынка вакансий в направлении Data Science

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Проект для сбора и анализа вакансий с hh.ru в области Data Science, аналитики данных и Machine Learning.

## 📌 О проекте

Проект состоит из двух основных компонентов:

1. **Парсер вакансий** (`hh_parser.py`) - собирает до 500 вакансий по каждой специализации
2. **Аналитический блокнот** (`vacancy_analysis.ipynb`) - проводит полный анализ собранных данных

## 📊 Специализации

- Data Scientist
- Аналитик данных
- Machine Learning Engineer

## 🛠 Технологический стек

- **Парсинг**: Python, requests, pandas
- **Анализ**: pandas, numpy, matplotlib, seaborn, scikit-learn
- **Визуализация**: plotly, seaborn
- **Инструменты**: Jupyter Notebook


## 📂 Структура проекта

```
├── parsing/
│   ├── hh_parsing.py                  # Скрипт парсинга сайта                  
│   └── README.md                      # Описание скрипта          
├── hh_vacancies_20250325_2040.csv     # Собранные данные 25 марта 2025
├── hh_vacancies_20250331_2040.csv     # Собранные данные 31 марта 2025
├── test.ipynb                         # Просмотр собранных данных       
├── vacancy_analysis.ipynb             # Основной блокнот
├── описание.csv                       # Данные для модели BERT
├── описание_BERT.ipynb                # Блокнот для анализа с помощью модели BERT     
└── README.md                          # Описание проекта       
```
