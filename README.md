# IT Inno Hack

![images/header.png](images/header.png)

## Ссылки

Сайт соревнования: [it-innohack.ru](https://it-innohack.ru/) \
GitHub: [github.com/blogerlu/it_inno_hack](https://github.com/blogerlu/it_inno_hack)

## Архитектура

```
├── app
│   └── __init__.py
├── data
│   └── public
├── docker-compose
│   ├── docker-compose.yaml
│   └── docker-entrypoint-initdb.d
│       └── 00_initial_datasets_tables.sh
├── images
│   └── header.png
├── notebooks
│   └── data_analitics.ipynb
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Setup

Используйте docker-compose:
```bash
docker-compose up
```
