# 🤖 Telegram GPT Bot

Бот на **Aiogram 3.x** с интеграцией **ChatGPT** и несколькими режимами:

- 🎲 Рандомный факт
- 💬 GPT-чат
- 🧑‍🎓 Диалог с известной личностью
- 📝 Квиз (варианты A–D, ведётся счёт)
- 🌐 Переводчик
- 🎬 Рекомендации

## 🚀 Запуск

### 1. Подготовка
- Установи [Docker Desktop](https://www.docker.com/products/docker-desktop/).
- Склонируй проект или распакуй архив.

### 2. Настрой `.env`

Создай файл `.env` в корне рядом с `docker-compose.yml`:

```env
TELEGRAM_TOKEN=1234567890:ABCDEF...
OPENAI_API_KEY=sk-...
TZ=Europe/Tallinn
```

> ⚠️ `.env` добавлен в `.dockerignore`, в git он не попадёт.

### 3. Сборка и запуск

```bash
docker compose build
docker compose up -d
```

Проверить логи:
```bash
docker logs -f tg_gpt_aiogram_bot
```

Остановить/перезапустить:
```bash
docker compose restart
docker compose down
```

### 4. Проверка

В Telegram открой своего бота и введи:
```
/start
```

Ты увидишь главное меню (6 кнопок в 3 строки) и кнопку 🏠 **Меню** снизу экрана.

---

## 📂 Структура проекта

```
.
├── bot.py                # Точка входа
├── core/                 # Диспетчер, конфиг
├── handlers/             # Обработчики команд
├── services/             # Работа с OpenAI, утилиты
├── Dockerfile            # Сборка образа
├── docker-compose.yml    # Сервис для запуска
├── requirements.txt      # Python-зависимости
├── healthcheck.py        # Скрипт для проверки бота
└── README.md             # Документация
```

---

## 🛠 Полезные команды

Посмотреть контейнеры:
```bash
docker compose ps
```

Пересобрать после изменений кода:
```bash
docker compose up -d --build
```

Войти внутрь контейнера:
```bash
docker exec -it tg_gpt_aiogram_bot bash
```

---

## ❓ Траблшутинг

- **`Token is invalid` / `NoneType`**  
  Проверь `.env`, токен должен быть в формате `1234567890:ABCDEF...`.

- **Контейнер перезапускается / unhealthy**  
  Проверь интернет доступ к `api.telegram.org` и `api.openai.com`.

- **Изменил код, а бот не обновился**  
  Сделай пересборку:
  ```bash
  docker compose up -d --build
  ```

---

