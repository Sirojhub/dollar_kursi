from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
import scraper

router = Router()

class CalculatorState(StatesGroup):
    waiting_for_amount = State()

@router.message(F.text == "🔄 Kalkulyator")
async def start_calculator(message: types.Message, state: FSMContext):
    await message.answer(
        "Konvertatsiya summasini kiriting (masalan: `100 USD` yoki `1000000 UZS`):"
    )
    await state.set_state(CalculatorState.waiting_for_amount)

@router.message(StateFilter(CalculatorState.waiting_for_amount))
async def process_calculation(message: types.Message, state: FSMContext):
    text = message.text.upper().strip()
    
    # Simple parsing logic
    try:
        if "USD" in text:
            amount = float(text.replace("USD", "").strip())
            currency = "USD"
        elif "UZS" in text:
            amount = float(text.replace("UZS", "").strip())
            currency = "UZS"
        elif text.isdigit():
            # Default to USD if only number, or ask? Let's assume USD for now
            amount = float(text)
            currency = "USD" 
        else:
            await message.answer("Iltimos, formatni to'g'ri kiriting: `100 USD`")
            return

        rates = await scraper.get_current_rates()
        if not rates:
            await message.answer("Kurs ma'lumotlari mavjud emas.")
            await state.clear()
            return
            
        rate_buy = rates['buy']
        rate_sell = rates['sell']
        
        if currency == "USD":
            result = amount * rate_buy
            await message.answer(f"💵 {amount} USD = {result:,.0f} UZS (Sotib olish kursi bo'yicha)")
        else:
            result = amount / rate_sell
            await message.answer(f"🔄 {amount:,.0f} UZS = {result:.2f} USD (Sotish kursi bo'yicha)")
            
    except ValueError:
        await message.answer("Raqam noto'g'ri kiritildi.")
    
    await state.clear()
