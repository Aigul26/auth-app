# Auth app

Сервис с простым модулем CRUD
Свагер доступен по адресу:
- При локальном разворачивании через docker-compose.yml: http://localhost:8001/docs

Для успешного разворачивания при локальной разработке:
1. На основе .env.example создать и заполнить значениями .env файл в корневой директории репозитория
2. Поднять docker-контейнер с БД PostgreSQL 
3. Запустить docker-контейнер auth app командой в терминале
    ```bash
    docker compose -f docker-compose-dev.yml up -d --build
    ```
4. Накатить миграции командой в терминале
    ```bash
    alembic upgrade head
    ```
