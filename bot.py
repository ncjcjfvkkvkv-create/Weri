import asyncio
import os
import json
from telethon import TelegramClient, events
from datetime import datetime
import aiofiles

# ===== تنظیمات با کلید عمومی و توکن ربات =====
API_ID = 6
API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
BOT_TOKEN = "8970253868:AAEwQUg2mJ6E8LQcI0i7Kd74ETP19xSbdhE"  # توکن ربات شما
UPLOAD_DIR = "uploads"
METADATA_FILE = "metadata.json"
# =============================================

os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_metadata(file_name, file_path, message_id, chat_id):
    metadata = {
        "file_name": file_name,
        "file_path": file_path,
        "message_id": message_id,
        "chat_id": chat_id,
        "timestamp": datetime.now().isoformat(),
        "size": os.path.getsize(file_path) if os.path.exists(file_path) else 0
    }
    
    try:
        async with aiofiles.open(METADATA_FILE, "r") as f:
            data = json.loads(await f.read())
    except:
        data = []
    
    data.append(metadata)
    
    async with aiofiles.open(METADATA_FILE, "w") as f:
        await f.write(json.dumps(data, indent=2))

async def main():
    client = TelegramClient("bot_session", API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)
    
    print("✅ ربات HediaBot متصل شد!")
    print("📥 منتظر دریافت فایل‌ها...")
    
    @client.on(events.Message)
    async def handler(event):
        if event.message.file:
            file_name = event.message.file.name or f"unknown_{event.message.id}"
            safe_file_name = file_name.replace("/", "_").replace(" ", "_")
            file_path = os.path.join(UPLOAD_DIR, safe_file_name)
            
            print(f"📥 دانلود: {file_name}")
            await event.message.download_media(file_path)
            
            await save_metadata(
                safe_file_name, 
                file_path, 
                event.message.id, 
                event.chat_id
            )
            
            await event.reply(f"✅ فایل {file_name} دریافت شد!")
            print(f"✅ ذخیره شد: {file_path}")
        else:
            print(f"💬 پیام: {event.message.text}")
    
    # ۵ دقیقه گوش بده بعد بسته بشه (برای GitHub Actions)
    await asyncio.sleep(300)
    await client.disconnect()
    print("⏹️ ربات متوقف شد.")

if __name__ == "__main__":
    asyncio.run(main())
