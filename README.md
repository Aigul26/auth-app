# Auth app

Сервис с простым модулем CRUD
- При локальном разворачивании через docker-compose.yml свагер доступен: http://localhost:8001/docs

Для успешного разворачивания при локальной разработке:
1. На основе .env.example создать и заполнить значениями .env файл в корневой директории репозитория
2. Запустить docker-контейнер auth app командой в терминале
    ```bash
    docker-compose up --build -d
    ```
3. Накатить миграции командой в терминале
    ```bash
    alembic upgrade head
    ```
