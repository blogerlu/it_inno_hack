# IT Inno Hack

![images/header.png](images/header.png)

## Ссылки

Сайт соревнования: [it-innohack.ru](https://it-innohack.ru/) \
GitHub: [github.com/blogerlu/it_inno_hack](https://github.com/blogerlu/it_inno_hack)

## Структура проекта

```
.
├── app
│   ├── custom_dataframe.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── custom_dataframe.cpython-312.pyc
│   │   ├── __init__.cpython-312.pyc
│   │   └── similarity_system.cpython-312.pyc
│   └── similarity_system.py
├── data
│   └── public
│       ├── docker-compose
│       │   ├── docker-compose.yaml
│       │   ├── docker-entrypoint-initdb.d
│       │   │   └── 00_initial_datasets_tables.sh
│       │   └── input_data
│       ├── HOW_TO.md
│       ├── main1.csv
│       ├── main2.csv
│       └── main3.csv
├── docker-compose
│   ├── docker-compose.yaml
│   └── docker-entrypoint-initdb.d
│       └── 00_initial_datasets_tables.sh
├── docker-compose.yml
├── Dockerfile
├── images
│   └── header.png
├── main.py
├── notebooks
│   ├── clickhouse_connect.ipynb
│   ├── data_analitics.ipynb
│   └── merge_tables.ipynb
├── poetry.lock
├── pyproject.toml
└── README.md

```

## Setup

Используйте docker-compose:

```bash
docker-compose up
```

## Архитектура

На данном этапе мы проводим много локальных тестов в jupyter notebook'ах, однако уже сделали часть централизированной
системы регистрации записей в `app`.

### CustomDataFrame (`custom_dataframe.py`)

Наследник pd.DataFrame для работы с данными.

* Метод `register_row` проверяет наличие "похожих" записей (дубликатов) через `SimilaritySystem` (о ней читать дальше) и вносит запись, если у неё нет дубликатов или дополняет данные дубликата, если есть дополнительные параметры.
* Метод `combine_rows` сливает в одну запись данные из разных записей, оставляя максимальное количество данных.

### SimilaritySystem (`similarity_system.py`)

Класс для работы с сравнением строк.

* Метод `__call__` подсчитывает похожесть двух строк с помощью заранее записанных правил (`Rule`).
* Метод `add_rule` добавляет правило для сравнения строк.

### Rule (`similarity_system.py`)

Абстрактный класс для создания правил сравнения строк.
