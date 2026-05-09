# Свіже з ферми | Виноградар — MVP Telegram Bot

Простий MVP-бот для маршруту №10 (Виноградар), який показує розклад, акції, новинки, контакти та приймає звернення.

## Стек
- Python 3.11+
- aiogram 3.x
- Google Sheets API (optional)
- python-dotenv

## Структура
- `bot.py` — точка входу
- `config.py` — конфігурація з `.env`
- `keyboards.py` — inline клавіатури
- `handlers/` — обробники бота
- `services/storage.py` — абстракція сховища (Google Sheets або CSV)
- `data/schedule.py` — хардкод розкладу (MVP)
- `data/requests.csv` — локальне збереження звернень (автоматично)

## Quick local test without Google Sheets
1. Створіть `.env`
2. Додайте тільки `BOT_TOKEN`
3. Виконайте `pip install -r requirements.txt`
4. Запустіть `python bot.py`
5. Звернення клієнтів будуть збережені в `data/requests.csv`

## Налаштування Google Sheets (опційно)
1. Заповніть у `.env`:
   - `GOOGLE_SHEET_ID`
   - `GOOGLE_SERVICE_ACCOUNT_FILE`
2. Створіть Google service account, завантажте JSON ключ, надайте доступ до таблиці.
3. У Google Sheet зробіть колонки в такому порядку:
   - created_at
   - telegram_user_id
   - username
   - full_name
   - request_type
   - customer_name
   - contact
   - stop_address
   - message
   - status
   - responsible
   - result

## Запуск
```bash
python bot.py
```

## Примітка
У першій версії розклад береться тільки з `data/schedule.py` (хардкод).

## How to update promotions and new products with images
- Додавайте зображення акцій у папку `media/promotions/`.
- Додавайте зображення новинок у папку `media/new_products/`.
- Поточні очікувані імена файлів:
  - `media/promotions/gauda_maasdam.jpg`
  - `media/promotions/butter.jpg`
  - `media/new_products/tertyi_pyrih.jpg`
- Оновлюйте ціни та тексти в `data/content.py`.
- Після змін перезапустіть бота.
