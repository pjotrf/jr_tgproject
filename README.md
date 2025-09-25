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
├── bot.py # точка входа
├── config.py # конфигурация (токены)
├── core/
│ ├── dispatcher.py # инициализация бота и логирование
│ └── logger.py # настройка логгера
├── handlers/ # обработчики команд и callback
│ ├── start.py
│ ├── random_fact.py
│ ├── gpt.py
│ ├── talk.py
│ ├── quiz.py
│ ├── translator.py
│ └── recs.py
├── keyboards/ # клавиатуры
│ ├── inline/
│ │ ├── main_menu.py
│ │ ├── talk.py
│ │ ├── quiz.py
│ │ ├── translator.py
│ │ └── recs.py
│ └── reply/
│ └── main_menu.py
├── services/
│ └── chatgpt.py # обёртка для работы с OpenAI
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
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

