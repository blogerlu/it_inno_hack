# IT Inno Hack

![images/header.png](images/header.png)

## Ссылки

Сайт соревнования: [it-innohack.ru](https://it-innohack.ru/) \
GitHub: [github.com/blogerlu/it_inno_hack](https://github.com/blogerlu/it_inno_hack) \
Презентация: [google-slides](https://docs.google.com/presentation/d/1Yr8kffI3Ekf8GrSjdYI6fKgN-JYQnfYXKVZQmuAoad4/edit?usp=sharing)

## Структура проекта

```
.
├── app
│   ├── __init__.py
│   ├── cleaners
│   │   ├── __init__.py
│   │   ├── base_cleaner.py
│   │   ├── birthdate_cleaner.py
│   │   ├── email_cleaner.py
│   │   ├── name_cleaner.py
│   │   ├── phone_cleaner.py
│   ├── duplicate_finder.py
│   ├── ml
│   │   ├── __init__.py
│   │   ├── clustering.py
│   │   └── word2vec.py
│   ├── processor.py
├── data
│   ├── concat.csv
│   ├── duplicates.csv
│   ├── main1_clean.csv
│   ├── main3_clean.csv
│   ├── public
│   │   ├── HOW_TO.md
│   │   ├── main1.csv
│   │   ├── main2.csv
│   │   └── main3.csv
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

### Cleaners

Классы с базовыми правилами: регулярными выражениями и другой работой со строками.

* `app/cleaners/base_cleaner.py` - базовый класс для стандартизации данных
* `app/cleaners/birthdate_cleaner.py` - стандартизация даты рождения
* `app/cleaners/email_cleaner.py` - стандартизация почты
* `app/cleaners/name_cleaner.py` - стандартизация имени
* `app/cleaners/phone_cleaner.py` - стандартизация телефона

### Duplicate Finder

Класс для поиска дубликатов.
У него есть 2 режима:

* normal - наилучшее качество за счёт подсчёта расстояний `Jaro–Winkler` и `Damerau–Levenshtein`, кластеризации векторов
  имён.
* fast - хуже качество, но быстрее за счёт отказа от расстояний в пользу обычного совпадения и отказа от `Word2Vec` при
  блокировании.

Внутри класса создаются блоки для более эффективного обращения и сравнения в режиме `normal`.

### Processor

Класс для общения с Duplicate Finder и Cleaner'ами.
Создан для поддержания необходимых форматов данных и стандартизованной передачи (например, где нет столбцов - заполняем
пустыми и тп).

### ML (Word2Vec and MiniBatchKMeans)

Данный функционал не вошёл в финальную версию Processor, тк имел низкие показатели скорости.

Однако мы считаем, что в реальной практике необходимость обработать БД с более чем несколькоми миллионами записей на малых ресурсах возникает крайне
редко и время может стать менее приоритетным параметром.

Поэтому считаем этот метод важным и перспективным для развития. Для нас важно было протестировать гипотезу, что он повысит качество блокирования и поиска по БД - она оправдалась.

`Word2Vec` здесь переводит имена в вектора, а `MiniBatchKMeans` - кластеризует эти векторы. Тем самым, при добавлении новой записи мы сможем точно определить группу для сравнения, тем самым __снизим__ общее время использования.
