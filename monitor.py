import os
import requests

bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")
api_url = f"https://api.telegram.org/bot{bot_token}/getMe"
send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

def send_message(text):
    try:
        requests.post(send_url, data={"chat_id": chat_id, "text": text})
    except Exception as e:
        print("Failed to send alert:", e)

# Повідомлення про запуск
send_message("🤖 Бот запущено!")

# Стан з попереднього запуску
try:
    with open("status.txt", "r") as f:
        last_status = f.read().strip()
except:
    last_status = "unknown"

# Перевірка API
try:
    r = requests.get(api_url, timeout=10)
    if r.status_code == 200:
        current_status = "ok"
        if last_status != "ok":
            send_message("✅ Telegram API знову працює.")
    else:
        current_status = "fail"
        if last_status != "fail":
            send_message(f"⚠️ Telegram API недоступне. Код: {r.status_code}")
except Exception as e:
    current_status = "fail"
    if last_status != "fail":
        send_message(f"🚨 Помилка підключення до Telegram API: {e}")

# Запис нового стану
with open("status.txt", "w") as f:
    f.write(current_status)
