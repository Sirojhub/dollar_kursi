from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import database

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await database.add_user(message.from_user.id, message.from_user.username)
    
    builder = ReplyKeyboardBuilder()
    builder.button(text="💵 Bugungi kurs")
    builder.button(text="🔄 Kalkulyator")
    builder.button(text="📈 Grafik")
    builder.button(text="🔔 Obuna")
    builder.button(text="📍 ATM")
    builder.adjust(2)

    await message.answer(
        "Assalomu alaykum! Men **Antigravity** - Agrobank kursi bo'yicha maslahatchiman.\n\n"
        "Bugungi valyuta kurslarini bilish yoki hisoblash uchun menyudan foydalaning.",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
