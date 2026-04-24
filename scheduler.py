from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError

import texts
import keyboards as kb
from database import get_users_for_reminder, mark_reminded


def start_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()

    async def send_reminder(day: int, text: str):
        user_ids = await get_users_for_reminder(day)
        for uid in user_ids:
            try:
                await bot.send_message(uid, text, reply_markup=kb.kb_reminder(), parse_mode="Markdown")
                await mark_reminded(uid, day)
            except TelegramForbiddenError:
                # Пользователь заблокировал бота
                await mark_reminded(uid, day)
            except Exception as e:
                print(f"Reminder {day} error for {uid}: {e}")

    # Проверяем раз в час — кому пора слать напоминание
    scheduler.add_job(lambda: send_reminder(1, texts.REMINDER_1), "interval", hours=1)
    scheduler.add_job(lambda: send_reminder(2, texts.REMINDER_2), "interval", hours=1)
    scheduler.add_job(lambda: send_reminder(3, texts.REMINDER_3), "interval", hours=1)

    return scheduler
