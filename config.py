import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "8764969627:AAEO2xn3cf6fc9RHL4Ng9kyu-cHp_s8fxWs")

PARTNER_LINK = "https://reg.eda.yandex.ru/?advertisement_campaign=forms_for_agents&user_invite_code=d4c5d4608f694cbcac95d2775cd49ac9&utm_content=blank"

# Через сколько дней слать напоминания
REMINDER_DAY_1 = 3   # "Как дела, начал уже?"
REMINDER_DAY_2 = 7   # "Напоминаю про 80 заказов"
REMINDER_DAY_3 = 14  # Финальный дожим
