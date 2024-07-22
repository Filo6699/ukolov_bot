# Currency Bot

Бот для перевода одной валюты в другую. Отслеживает курсы валют и обновляет их каждый день.

Протестировать бота можно [тут](https://t.me/techjob_task_bot).

## Технологии
- aiohttp
- aiogram
- apscheduler
- Docker
- Redis

## Фичи
- [x] Получение и сохранение курсов валют в Redis
- [x] /exchange
- [x] /rates
- [x] Завёрнут в докер

## Установка и запуск

### 1. Клонируйте репозиторий

```sh
git clone https://github.com/Filo6699/ukolov_bot
cd ukolov_bot
```

### 2. Настройте `.env` по шаблону `.env.example`

### 3. Запустите `docker-compose up`

```sh
docker-compose up
```

### 4. Устроить меня на работу (пожалуйста)
