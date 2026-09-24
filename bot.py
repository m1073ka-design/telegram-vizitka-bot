import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    first_name = message.from_user.first_name or "do‘stim"
    await message.answer(
        f"Assalomu alaykum, <b>{html.quote(first_name)}</b>! 👋\n"
        "Men vizitka botman. Buyruqlar uchun /help ni bosing."
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "<b>Buyruqlar:</b>\n"
        "/start — botni boshlash\n"
        "/help — buyruqlar ro‘yxati\n"
        "/about — men haqimda\n"
        "/kontakt — aloqa ma’lumotlari\n"
        "/rasm — rasm yuborish\n"
        "/qosh 5 7 — ikki sonni qo‘shish"
    )


@router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(
        "<b>Men haqimda</b>\n"
        "Ism: Muhammadrasul\n"
        "Yosh: 16\n"
        "Qiziqishlar: dasturlash, kitob o‘qish va sport."
    )


@router.message(Command("kontakt"))
async def cmd_kontakt(message: Message):
    await message.answer(
        "<b>Kontaktlarim</b>\n"
        "Telefon: +998905827101\n"
        '<a href="@muhammad1onov17">Telegram</a>\n'
        '<a href="@muhammad1onov17">Instagram</a>',
        disable_web_page_preview=True,
    )


@router.message(Command("rasm"))
async def cmd_rasm(message: Message):
    await message.answer_photo(
        photo="https://picsum.photos/600/400",
        caption="🌄 Rasm: ",
    )


@router.message(Command("qosh"))
async def cmd_qosh(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("Ikkita son kiriting. Masalan: <code>/qosh 5 7</code>")
        return

    parts = command.args.split()
    if len(parts) != 2:
        await message.answer("Ikkita son kiriting. Masalan: <code>/qosh 5 7</code>")
        return

    try:
        a, b = (float(part) for part in parts)
    except ValueError:
        await message.answer("Iltimos, faqat  ikkita son kiriting. Masalan: <code>/qosh 5 7</code>")
        return

    result = a + b
    if result.is_integer():
        result = int(result)
    await message.answer(f"{a:g} + {b:g} = <b>{result}</b>")


@router.message(F.text)
async def text_replies(message: Message):
    text = message.text.lower().strip()

    if text in ("salom", "assalomu alaykum"):
        await message.reply("Va alaykum assalom! 🤝")
    elif "qalaysan" in text or "ishlar qalay" in text:
        await message.reply("Yaxshi, rahmat! Sizda ishlar qalay? 😊")
    else:
        await message.answer("Tushunmadim, /help ni bosing.")


@router.message(F.photo)
async def photo_handler(message: Message):
    file_id = message.photo[-1].file_id
    await message.answer(
        f"Rasm qabul qilindi. Uning file_id si:\n<code>{html.quote(file_id)}</code>"
    )


@router.message(F.sticker)
async def sticker_handler(message: Message):
    await message.answer("Stikeringiz zo‘r ekan 😄")


@router.message(F.voice)
async def voice_handler(message: Message):
    await message.answer("Ovozli xabaringizni oldim 🎙️")


@router.message(F.video)
async def video_handler(message: Message):
    await message.answer("Videongizni oldim 🎬")


@router.message()
async def unknown_handler(message: Message):
    await message.answer("Tushunmadim, /help ni bosing.")


async def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN .env faylida topilmadi")

    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
