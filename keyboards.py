"""Inline keyboards for bot navigation."""

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Create main menu inline keyboard."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🚚 Коли ми приїдемо?", callback_data="menu:schedule")
    builder.button(text="🔥 Акції", callback_data="menu:promotions")
    builder.button(text="🆕 Новинка", callback_data="menu:new_products")
    builder.button(text="☎️ Подзвонити / контакти", callback_data="menu:contacts")
    builder.button(text="✍️ Написати нам", callback_data="menu:feedback")
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def schedule_nav_keyboard(page: int) -> InlineKeyboardMarkup:
    """Navigation keyboard for schedule pages."""
    builder = InlineKeyboardBuilder()
    if page > 1:
        builder.button(text="⬅️ Назад", callback_data=f"schedule:page:{page-1}")
    if page < 3:
        builder.button(text="Наступна частина ➡️", callback_data=f"schedule:page:{page+1}")
    builder.button(text="До меню", callback_data="menu:main")
    builder.adjust(2, 1)
    return builder.as_markup()


def feedback_types_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting feedback type."""
    builder = InlineKeyboardBuilder()
    for item in ["❓ Питання", "⚠️ Скарга", "💡 Пропозиція", "❤️ Подяка"]:
        builder.button(text=item, callback_data=f"feedback:type:{item}")
    builder.button(text="❌ Скасувати", callback_data="feedback:cancel")
    builder.adjust(1)
    return builder.as_markup()


def feedback_cancel_keyboard() -> InlineKeyboardMarkup:
    """Keyboard with cancel action for feedback form steps."""
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Скасувати", callback_data="feedback:cancel")
    return builder.as_markup()
