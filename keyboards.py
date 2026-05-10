"""Inline keyboards for bot navigation."""

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Create main menu inline keyboard."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🚚 Коли ми приїдемо?", callback_data="menu:schedule")
    builder.button(text="🔥 Акції", callback_data="menu:promotions")
    builder.button(text="🆕 Новинка", callback_data="menu:new_products")
    builder.button(text="☎️ Контакти", callback_data="menu:contacts")
    builder.button(text="✍️ Написати нам", callback_data="menu:feedback")
    builder.adjust(2, 2, 1)
    return builder.as_markup()




def schedule_sections_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting schedule street/zone section."""
    builder = InlineKeyboardBuilder()
    builder.button(text="Тираспольська / Стеценка", callback_data="schedule:section:tyraspolska_stetsenka")
    builder.button(text="Виговського / Гречка", callback_data="schedule:section:vyhovskoho_hrechka")
    builder.button(text="Гонгадзе", callback_data="schedule:section:gongadze")
    builder.button(text="Свободи / Порика", callback_data="schedule:section:svobody_poryka")
    builder.button(text="Правди / Європейського Союзу", callback_data="schedule:section:pravdy_yevropeiskoho_soiuzu")
    builder.button(text="⬅️ До меню", callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


def schedule_section_nav_keyboard() -> InlineKeyboardMarkup:
    """Navigation keyboard for schedule street/zone sections."""
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ До списку вулиць", callback_data="menu:schedule")
    builder.button(text="⬅️ До меню", callback_data="menu:main")
    builder.adjust(1)
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
