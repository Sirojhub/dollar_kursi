from aiogram import Router, F, types
import database
import sys

router = Router()

@router.message(F.text == "🔔 Obuna")
async def toggle_subscription(message: types.Message):
    user_id = message.from_user.id
    is_subscribed = await database.toggle_subscription(user_id)
    
    if is_subscribed:
        await message.answer("✅ Siz muvaffaqiyatli obuna bo'ldingiz! Kurs o'zgarganda xabar beraman.")
    else:
        await message.answer("❌ Obuna bekor qilindi.")

@router.message(F.text == "📍 ATM")
async def show_atms(message: types.Message):
    # Static list for now as requested/planned
    await message.answer(
        "📍 **Agrobank Bankomatlari:**\n\n"
        "1. Toshkent sh, Chilonzor filiali (24/7)\n"
        "2. Toshkent sh, Oloy Bozori yonida\n"
        "3. Samarqand sh, Registon maydoni\n"
        "4. Buxoro sh, Labi hovuz\n\n"
        "Yaqin orada GPS orqali qidirish imkoniyati qo'shiladi."
    )

if __name__ == "__main__":
    print("\n❌ ERROR: Do not run this file directly!")
    print("👉 Please run 'main.py' instead: python main.py\n")
