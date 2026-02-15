from aiogram import Router, F, types
import database
# import matplotlib.pyplot as plt
# import io

router = Router()

@router.message(F.text == "📈 Grafik")
async def show_chart(message: types.Message):
    # For now, let's just show text based history as installing matplotlib
    # in some environments can be tricky without system deps.
    # If user wants image, we can uncomment.
    
    history = await database.get_history("USD", 7)
    
    if not history:
        await message.answer("📉 Tarixiy ma'lumotlar hozircha yetarli emas.")
        return

    text = "📊 <b>Oxirgi 7 kunlik kurs dinamikasi:</b>\n\n"
    for row in history:
        date = row['updated_at'].split(' ')[0]
        text += f"📅 {date}: {row['buy_rate']} - {row['sell_rate']} UZS\n"
        
    await message.answer(text)

    # Note: To implement real image chart:
    # 1. Collect dates and rates from history
    # 2. plt.plot(dates, rates)
    # 3. buf = io.BytesIO()
    # 4. plt.savefig(buf, format='png')
    # 5. buf.seek(0)
    # 6. await message.answer_photo(types.BufferedInputFile(buf.read(), filename='chart.png'))
