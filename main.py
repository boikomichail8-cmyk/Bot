import os
import asyncio
from aiogram import Bot, Dispatcher, types
import subprocess

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")  # Куда бот отправляет уведомления

subscribed_streamers = []

bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher(bot)

async def download_stream(streamer):
    filename = f"{streamer}.mp4"
    # Записываем стрим через streamlink в 720p
    cmd = ["streamlink", f"https://twitch.tv/{streamer}", "720p", "-o", filename]
    subprocess.run(cmd)
    await bot.send_message(chat_id=TG_CHAT_ID, text=f"Запись стрима {streamer} завершена!")

@dp.message_handler(commands=["sub"])
async def subscribe(message: types.Message):
    args = message.get_args()
    if not args:
        await message.answer("Укажи имя стримера: /sub <имя>")
        return
    streamer = args.strip()
    if streamer not in subscribed_streamers:
        subscribed_streamers.append(streamer)
        await message.answer(f"Подписка на {streamer} активирована!")
        # Запуск записи в фоне
        asyncio.create_task(download_stream(streamer))
    else:
        await message.answer(f"Вы уже подписаны на {streamer}!")

@dp.message_handler(commands=["list"])
async def list_subs(message: types.Message):
    if subscribed_streamers:
        await message.answer("Подписки:\n" + "\n".join(subscribed_streamers))
    else:
        await message.answer("Список подписок пуст.")

async def main():
    await dp.start_polling()

if name == "__main__":
    asyncio.run(main())
