"""User-facing bot handlers."""

import logging
from pathlib import Path

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import config
from data.content import CONTACTS_TEXT, NEW_PRODUCTS, NEW_PRODUCTS_TEXT, PROMOTIONS, PROMOTIONS_TEXT
from data.schedule import ROUTE_TITLE, SCHEDULE_PAGES, VISIT_DAYS
from keyboards import feedback_types_keyboard, main_menu_keyboard, schedule_nav_keyboard
from keyboards import feedback_cancel_keyboard
from services.storage import get_storage


logger = logging.getLogger(__name__)
router = Router()
storage = get_storage(config)


START_TEXT = (
    'Вітаємо у боті “Свіже з ферми | Виноградар”.\n\n'
    'Тут можна швидко:\n'
    '- дізнатися, коли ми приїдемо;\n'
    '- подивитися акції;\n'
    '- зв’язатися з нами.\n\n'
    'Оберіть потрібний розділ нижче.'
)

FEEDBACK_TYPE_MAP = {
    "❓ Питання": "Питання",
    "⚠️ Скарга": "Скарга",
    "💡 Пропозиція": "Пропозиція",
    "❤️ Подяка": "Подяка",
}


class FeedbackForm(StatesGroup):
    request_type = State()
    customer_name = State()
    contact = State()
    stop_address = State()
    message = State()


async def safe_edit_or_send(callback: CallbackQuery, text: str, reply_markup):
    try:
        await callback.message.edit_text(text, reply_markup=reply_markup)
    except TelegramBadRequest:
        await callback.message.answer(text, reply_markup=reply_markup)


def build_schedule_text(page: int) -> str:
    stops = "\n".join(SCHEDULE_PAGES[page])
    return f"{ROUTE_TITLE}\n{VISIT_DAYS}\n\n{stops}"


def build_promotion_caption(item: dict) -> str:
    return (
        f"🔥 {item.get('title', '')}\n\n"
        f"Ціна: {item.get('price', '')}\n"
        f"Період: {item.get('period', '')}\n"
        f"Доступно: {item.get('availability', '')}\n\n"
        f"{item.get('description', '')}\n\n"
        "Кількість товару може бути обмежена.\n"
        "Деталі уточнюйте у продавця на маршруті."
    )


def build_new_product_caption(item: dict) -> str:
    return (
        f"🆕 {item.get('title', '')}\n\n"
        f"Ціна: {item.get('price', '')}\n"
        f"Доступно: {item.get('availability', '')}\n\n"
        f"{item.get('description', '')}\n\n"
        "Запитуйте у продавця на маршруті."
    )


async def send_card(message: Message, caption: str, image_path: str | None) -> None:
    if image_path and Path(image_path).is_file():
        await message.answer_photo(photo=FSInputFile(image_path), caption=caption)
        return
    await message.answer(caption)


def back_to_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ До меню", callback_data="menu:main")
    return builder.as_markup()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(START_TEXT, reply_markup=main_menu_keyboard())


@router.callback_query(F.data == "menu:main")
async def menu_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await safe_edit_or_send(callback, "Головне меню:", main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "menu:schedule")
async def schedule_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await safe_edit_or_send(callback, build_schedule_text(1), schedule_nav_keyboard(1))
    await callback.answer()


@router.callback_query(F.data.startswith("schedule:page:"))
async def schedule_page_handler(callback: CallbackQuery):
    page = int(callback.data.split(":")[-1])
    await safe_edit_or_send(callback, build_schedule_text(page), schedule_nav_keyboard(page))
    await callback.answer()


@router.callback_query(F.data == "menu:promotions")
async def promotions_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    if PROMOTIONS:
        for item in PROMOTIONS:
            await send_card(callback.message, build_promotion_caption(item), item.get("image_path"))
        await callback.message.answer("⬅️ До меню", reply_markup=back_to_menu_keyboard())
    else:
        await safe_edit_or_send(callback, PROMOTIONS_TEXT, main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "menu:new_products")
async def new_products_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    if NEW_PRODUCTS:
        for item in NEW_PRODUCTS:
            await send_card(callback.message, build_new_product_caption(item), item.get("image_path"))
        await callback.message.answer("⬅️ До меню", reply_markup=back_to_menu_keyboard())
    else:
        await safe_edit_or_send(callback, NEW_PRODUCTS_TEXT, main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "menu:contacts")
async def contacts_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await safe_edit_or_send(callback, CONTACTS_TEXT, main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "menu:feedback")
async def feedback_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FeedbackForm.request_type)
    await safe_edit_or_send(callback, "Оберіть, що саме ви хочете написати:", feedback_types_keyboard())
    await callback.answer()


@router.callback_query(F.data == "feedback:cancel")
async def feedback_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await safe_edit_or_send(
        callback,
        "Дію скасовано. Ви можете обрати потрібний розділ у меню.",
        main_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(FeedbackForm.request_type, F.data.startswith("feedback:type:"))
async def feedback_type_selected(callback: CallbackQuery, state: FSMContext):
    request_type = FEEDBACK_TYPE_MAP.get(callback.data.split(":", maxsplit=2)[-1], "")
    await state.update_data(request_type=request_type)
    await state.set_state(FeedbackForm.customer_name)
    await callback.message.answer("Напишіть ваше ім’я:", reply_markup=feedback_cancel_keyboard())
    await callback.answer()


@router.message(FeedbackForm.customer_name)
async def feedback_name(message: Message, state: FSMContext):
    await state.update_data(customer_name=message.text.strip())
    await state.set_state(FeedbackForm.contact)
    await message.answer(
        "Напишіть ваш телефон або Telegram для зворотного зв’язку:",
        reply_markup=feedback_cancel_keyboard(),
    )


@router.message(FeedbackForm.contact)
async def feedback_contact(message: Message, state: FSMContext):
    await state.update_data(contact=message.text.strip())
    await state.set_state(FeedbackForm.stop_address)
    await message.answer("Напишіть адресу або точку зупинки:", reply_markup=feedback_cancel_keyboard())


@router.message(FeedbackForm.stop_address)
async def feedback_stop(message: Message, state: FSMContext):
    await state.update_data(stop_address=message.text.strip())
    await state.set_state(FeedbackForm.message)
    await message.answer("Опишіть ситуацію коротко:", reply_markup=feedback_cancel_keyboard())


@router.message(FeedbackForm.message)
async def feedback_message(message: Message, state: FSMContext):
    data = await state.get_data()
    data["message"] = (message.text or "").strip()
    data["telegram_user_id"] = message.from_user.id
    data["username"] = message.from_user.username or ""
    data["full_name"] = message.from_user.full_name

    saved = storage.save_request(data)

    admin_text = (
        "📝 Нове повідомлення | Виноградар\n\n"
        f"Тип: {data.get('request_type', '')}\n"
        f"Клієнт: {data.get('customer_name', '')}\n"
        f"Контакт: {data.get('contact', '')}\n"
        f"Точка: {data.get('stop_address', '')}\n"
        "\nТекст:\n"
        f"{data.get('message', '')}\n\n"
        "Статус: new"
    )

    if config.admin_telegram_id:
        try:
            await message.bot.send_message(config.admin_telegram_id, admin_text)
        except Exception as exc:
            logger.error("Failed to send admin notification: %s", exc)
    else:
        logger.warning("ADMIN_TELEGRAM_ID is empty. Admin notification skipped")

    confirmation_text = (
        "Дякуємо. Ваше повідомлення прийнято.\n"
        "Ми передамо його відповідальному по маршруту “Виноградар”."
    )
    if not saved:
        confirmation_text = (
            "Дякуємо. Ваше звернення отримано, але сталася технічна помилка збереження. "
            "Ми вже перевіряємо."
        )

    await message.answer(confirmation_text, reply_markup=main_menu_keyboard())
    await state.clear()
