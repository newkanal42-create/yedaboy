from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def kb_start():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Сколько можно заработать?", callback_data="step_income")],
        [InlineKeyboardButton(text="Не интересует", callback_data="not_interested")],
    ])

def kb_income():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Что нужно для старта?", callback_data="step_conditions")],
        [InlineKeyboardButton(text="← Назад", callback_data="back_start")],
    ])

def kb_conditions():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Какие бонусы?", callback_data="step_bonus")],
        [InlineKeyboardButton(text="← Назад", callback_data="step_income")],
    ])

def kb_bonus():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Хочу оформиться!", callback_data="step_link")],
        [InlineKeyboardButton(text="← Назад", callback_data="step_conditions")],
    ])

def kb_link():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Я зарегистрировался!", callback_data="confirmed")],
        [InlineKeyboardButton(text="❓ Есть вопросы", callback_data="faq_menu")],
        [InlineKeyboardButton(text="← Назад", callback_data="step_bonus")],
    ])

def kb_confirmed():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❓ Остались вопросы", callback_data="faq_menu")],
    ])

def kb_faq():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚲 Нет транспорта", callback_data="faq_transport")],
        [InlineKeyboardButton(text="🕐 График работы", callback_data="faq_schedule")],
        [InlineKeyboardButton(text="💳 Когда платят?", callback_data="faq_payments")],
        [InlineKeyboardButton(text="📋 Самозанятость", callback_data="faq_selfemployed")],
        [InlineKeyboardButton(text="📝 Документы", callback_data="faq_registration")],
        [InlineKeyboardButton(text="🛡 Безопасность", callback_data="faq_safety")],
        [InlineKeyboardButton(text="← К ссылке", callback_data="step_link")],
    ])

def kb_faq_back():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад к вопросам", callback_data="faq_menu")],
        [InlineKeyboardButton(text="🚀 Оформиться", callback_data="step_link")],
    ])

def kb_reminder():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Уже работаю!", callback_data="confirmed")],
        [InlineKeyboardButton(text="🔗 Ссылка для регистрации", callback_data="step_link")],
        [InlineKeyboardButton(text="❓ Есть вопросы", callback_data="faq_menu")],
    ])
