import asyncio
import os
import sys
from telethon import TelegramClient, events

API_ID = 6
API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
BOT_TOKEN = "8970253868:AAEwQUg2mJ6E8LQcI0i7Kd74ETP19xSbdhE"

os.makedirs("uploads", exist_ok=True)

async def main():
    client = TelegramClient("bot_session", API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)
    print("✅ ربات متصل شد!")
    print("📥 منتظر دریافت فایل...")

    file_received = False

    @client.on(events.NewMessage)
    async def handler(event):
        nonlocal file_received
        if file_received:
            return
        
        if event.message.file:
            file_name = event.message.file.name or f"file_{event.message.id}"
            file_path = f"uploads/{file_name}"
            
            print(f"📥 دانلود: {file_name}")
            await event.message.download_media(file_path)
            print(f"✅ دانلود شد: {file_path}")
            
            await event.reply(f"✅ فایل {file_name} دریافت شد!")
            
            file_received = True
            print("⏹️ کار تموم شد!")
            await client.disconnect()
            sys.exit(0)

    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except SystemExit:
        print("✅ ربات با موفقیت کار رو تموم کرد!")
