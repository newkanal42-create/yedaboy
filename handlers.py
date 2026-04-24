from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import texts
import keyboards as kb
from database import upsert_user, set_status, all_users_stats

router = Router()


# ─── /start ─────────────────────────────────────────────────────────────────

@router.message(CommandStart())
async def cmd_start(msg: Message):
    await upsert_user(msg.from_user.id, msg.from_user.username or "", msg.from_user.first_name or "")
    await set_status(msg.from_user.id, "funnel")
    await msg.answer(texts.START, reply_markup=kb.kb_start())


# ─── ВОРОНКА (callback) ──────────────────────────────────────────────────────

@router.callback_query(F.data == "back_start")
async def cb_back_start(call: CallbackQuery):
    await call.message.edit_text(texts.START, reply_markup=kb.kb_start())

@router.callback_query(F.data == "step_income")
async def cb_income(call: CallbackQuery):
    await call.message.edit_text(texts.STEP_INCOME, reply_markup=kb.kb_income(), parse_mode="Markdown")

@router.callback_query(F.data == "step_conditions")
async def cb_conditions(call: CallbackQuery):
    await call.message.edit_text(texts.STEP_CONDITIONS, reply_markup=kb.kb_conditions(), parse_mode="Markdown")

@router.callback_query(F.data == "step_bonus")
async def cb_bonus(call: CallbackQuery):
    await call.message.edit_text(texts.STEP_BONUS, reply_markup=kb.kb_bonus(), parse_mode="Markdown")

@router.callback_query(F.data == "step_link")
async def cb_link(call: CallbackQuery):
    await set_status(call.from_user.id, "link_sent")
    await call.message.edit_text(texts.STEP_LINK, reply_markup=kb.kb_link(), parse_mode="Markdown")

@router.callback_query(F.data == "confirmed")
async def cb_confirmed(call: CallbackQuery):
    await set_status(call.from_user.id, "registered")
    await call.message.edit_text(texts.STEP_CONFIRMED, reply_markup=kb.kb_confirmed(), parse_mode="Markdown")

@router.callback_query(F.data == "not_interested")
async def cb_not_interested(call: CallbackQuery):
    await call.message.edit_text(texts.NOT_INTERESTED)


# ─── FAQ ─────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "faq_menu")
async def cb_faq_menu(call: CallbackQuery):
    await call.message.edit_text(
        "❓ *Частые вопросы* — выбери что интересует:",
        reply_markup=kb.kb_faq(),
        parse_mode="Markdown"
    )

FAQ_TEXTS = {
    "faq_transport":     texts.FAQ_TRANSPORT,
    "faq_schedule":      texts.FAQ_SCHEDULE,
    "faq_payments":      texts.FAQ_PAYMENTS,
    "faq_selfemployed":  texts.FAQ_SELFEMPLOYED,
    "faq_registration":  texts.FAQ_REGISTRATION,
    "faq_safety":        texts.FAQ_SAFETY,
}

@router.callback_query(F.data.in_(FAQ_TEXTS.keys()))
async def cb_faq_item(call: CallbackQuery):
    await call.message.edit_text(
        FAQ_TEXTS[call.data],
        reply_markup=kb.kb_faq_back(),
        parse_mode="Markdown"
    )


# ─── ADMIN: статистика ───────────────────────────────────────────────────────

@router.message(Command("stats"))
async def cmd_stats(msg: Message):
    rows = await all_users_stats()
    lines = ["📊 *Статистика бота:*\n"]
    labels = {
        "new": "Новые",
        "funnel": "В воронке",
        "link_sent": "Получили ссылку",
        "registered": "Зарегистрировались",
        "done": "Выполнили 80 заказов",
    }
    total = 0
    for status, count in rows:
        lines.append(f"• {labels.get(status, status)}: *{count}*")
        total += count
    lines.append(f"\n👥 Всего пользователей: *{total}*")
    await msg.answer("\n".join(lines), parse_mode="Markdown")
