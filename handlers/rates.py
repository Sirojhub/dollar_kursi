from aiogram import Router, F, types
from datetime import datetime
import scraper
import database

router = Router()

@router.message(F.text == "💵 Bugungi kurs")
async def show_rates(message: types.Message):
    # Fetch latest rate
    rates = await scraper.get_current_rates()
    
    if not rates:
        await message.answer("⚠️ Hozircha ma'lumot olishning imkoni bo'lmadi via CBU/Agrobank.")
        return

    # Save to DB for history
    await database.save_rate("USD", rates['buy'], rates['sell'], rates['cb'])

    time_now = datetime.now().strftime("%H:%M")
    
    response = (
        f"🏦 <b>Agrobank Valyuta Kursi</b> (YANGILANDI: {time_now})\n\n"
        f"🟢 <b>Sotib olish:</b> {rates['buy']} UZS\n"
        f"🔴 <b>Sotish:</b> {rates['sell']} UZS\n"
        f"📊 <b>MB kursi:</b> {rates['cb']} UZS\n\n"
        f"💡 <b>Maslahat:</b> "
    )

    # Simple advice logic
    if rates['buy'] < rates['cb']:
        response += "Hozir sotib olish uchun qulay vaqt! (MB kursidan past)"
    else:
        response += "Kurs barqaror."

    if rates.get('source') == 'CBU (Fallback)':
        response += "\n\n<i>⚠️ Agrobank sayti vaqtincha ishlamayapti, ma'lumotlar MB asosida taxminiy hisoblandi.</i>"

    await message.answer(response)
