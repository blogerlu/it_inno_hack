# IT Inno Hack

![images/header.png](images/header.png)

## Ссылки

Сайт соревнования: [it-innohack.ru](https://it-innohack.ru/) \
GitHub: [github.com/blogerlu/it_inno_hack](https://github.com/blogerlu/it_inno_hack)

## Структура проекта

```
├── app
│   ├── custom_dataframe.py
│   ├── __init__.py
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
├── images
│   └── header.png
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
