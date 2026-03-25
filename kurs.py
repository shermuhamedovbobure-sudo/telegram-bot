import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "8789607245:AAFheb_dkC4et4VwDWtVQmRdfxTThjCKYvk"
ADMIN_CHAT_ID = -1003780960836

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ===== STATES =====
class Form(StatesGroup):
    course = State()
    price = State()
    location = State()
    phone = State()

# ===== KEYBOARDS =====
course_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ingliz tili")],
        [KeyboardButton(text="Matematika")],
        [KeyboardButton(text="IT")],
        [KeyboardButton(text="Rus tili")],
        [KeyboardButton(text="Mental arifmetika")],
        [KeyboardButton(text="Boshqa")]
    ],
    resize_keyboard=True
)

price_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="600.000 so‘mgacha")],
        [KeyboardButton(text="600.000 – 1.000.000 so‘m")],
        [KeyboardButton(text="1.000.000 so‘mdan yuqori")]
    ],
    resize_keyboard=True
)

location_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Yunusobod")],
        [KeyboardButton(text="Chilonzor")],
        [KeyboardButton(text="Sergeli")],
        [KeyboardButton(text="Boshqa")]
    ],
    resize_keyboard=True
)

phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Telefonni yuborish", request_contact=True)],
        [KeyboardButton(text="⏭️ O‘tkazib yuborish")]
    ],
    resize_keyboard=True
)

# ===== START =====
@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await message.answer("📚 O‘quv kursini tanlang:", reply_markup=course_kb)
    await state.set_state(Form.course)

# ===== COURSE =====
@dp.message(Form.course)
async def get_course(message: types.Message, state: FSMContext):
    await state.update_data(course=message.text)
    await message.answer("💰 Oylik narxni tanlang:", reply_markup=price_kb)
    await state.set_state(Form.price)

# ===== PRICE =====
@dp.message(Form.price)
async def get_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("📍 Hududni tanlang:", reply_markup=location_kb)
    await state.set_state(Form.location)

# ===== LOCATION =====
@dp.message(Form.location)
async def get_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await message.answer("📞 Telefon raqamingizni yuboring:", reply_markup=phone_kb)
    await state.set_state(Form.phone)

# ===== PHONE =====
@dp.message(Form.phone)
async def get_phone(message: types.Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number
    elif message.text == "⏭️ O‘tkazib yuborish":
        phone = "Berilmadi"
    else:
        phone = message.text

    data = await state.get_data()
    data["phone"] = phone

    # ===== LEAD =====
    text = f"""
📥 Yangi lead

📚 Kurs: {data['course']}
💰 Narx: {data['price']}
📍 Hudud: {data['location']}
📞 Telefon: {data['phone']}
"""

    await bot.send_message(ADMIN_CHAT_ID, text)

    await message.answer("✅ So‘rovingiz qabul qilindi.")
    await state.clear()

# ===== RUN =====
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
