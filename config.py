import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_NAME = "agrobank_rates.db"
CBU_API_URL = "https://cbu.uz/oz/arkhiv-kurs-valyut/json/"
AGROBANK_URL = "https://agrobank.uz/uz/person/exchange_rates"
ADMIN_ID = os.getenv("ADMIN_ID") # Optional for admin commands
