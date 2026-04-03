import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# ===== CONFIG =====
TOKEN = "8789607245:AAFheb_dkC4et4VwDWtVQmRdfxTThjCKYvk"
ADMIN_CHAT_ID = -1003780960836

# ===== TUMAN ADMINS =====
DISTRICT_ADMINS = {
    "Chilonzor": 8111446081,
    "Sergeli": 1752376943,
    "Yunusobod": 1234567891,
    "Mirzo-Ulug‘bek": 1234567892,
    "Olmazor": 1234567893,
    "Yakkasaroy": 1234567894,
    "Shayxontohur": 1234567895,
    "Uchtepa": 1234567896,
    "Bektemir": 1234567897,
    "Mirobod": 1234567898,
    "Yashnobod": 1234567899,
    "Yangihayot": 1234567800
}

# ===== BOT =====
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ===== STATES =====
class Form(StatesGroup):
    course = State()
    price = State()
    location = State()
    phone = State()

# ===== AUTHORS =====
authors = [
    "Shermukhamedov Bobur Abbasovich",
    "To'xtayev Behzod G'aybullayevich"
]

# ===== KEYBOARDS =====
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔄 Qayta ishga tushirish"),
            KeyboardButton(text="Mualliflar")
        ],
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
        [KeyboardButton(text="Yunusobod"), KeyboardButton(text="Mirzo-Ulug‘bek")],
        [KeyboardButton(text="Chilonzor"), KeyboardButton(text="Olmazor")],
        [KeyboardButton(text="Sergeli"), KeyboardButton(text="Yakkasaroy")],
        [KeyboardButton(text="Shayxontohur"), KeyboardButton(text="Uchtepa")],
        [KeyboardButton(text="Bektemir"), KeyboardButton(text="Mirobod")],
        [KeyboardButton(text="Yashnobod"), KeyboardButton(text="Yangihayot")],
        [KeyboardButton(text="Boshqa")]
    ],
    resize_keyboard=True
)

phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Telefonni yuborish", request_contact=True)],
        [KeyboardButton(text="Asosiy menu")]
    ],
    resize_keyboard=True
)

# ===== GLOBAL: ASOSIY MENU =====
@dp.message(lambda message: message.text == "Asosiy menu")
async def back_to_menu(message: types.Message, state: FSMContext):
    await show_main_page(message, state)

# ===== GLOBAL: RESTART =====
@dp.message(lambda message: message.text == "🔄 Qayta ishga tushirish")
async def restart_bot(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🔄 Bot qayta ishga tushirildi")
    await show_main_page(message, state)

# ===== MAIN PAGE =====
async def show_main_page(message: types.Message, state: FSMContext):
    await state.clear()
    text = "📚 O‘quv markazlar bog'lovchi boti"

    try:
        photo = FSInputFile("image.png")
        await message.answer_photo(photo=photo, caption=text, reply_markup=main_menu)
    except:
        await message.answer(text, reply_markup=main_menu)

    await state.set_state(Form.course)

# ===== START =====
@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await show_main_page(message, state)

# ===== COURSE =====
@dp.message(Form.course)
async def get_course(message: types.Message, state: FSMContext):
    if message.text == "Mualliflar":
        authors_text = "\n".join(f"- {a}" for a in authors)
        await message.answer(f"📌 Mualliflar:\n{authors_text}")
        return

    await state.update_data(course=message.text)
    await message.answer("💰 Narxni tanlang:", reply_markup=price_kb)
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
    await message.answer("📞 Telefon yuboring:", reply_markup=phone_kb)
    await state.set_state(Form.phone)

# ===== PHONE =====
@dp.message(Form.phone)
async def get_phone(message: types.Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text

    data = await state.get_data()
    username = message.from_user.username

    text = f"""📥 Yangi lead
📚 Kurs: {data['course']}
💰 Narx: {data['price']}
📍 Hudud: {data['location']}
📞 Telefon: {phone}
👤 Telegram: @{username if username else "yo‘q"}"""

    try:
        location = data['location']

        # ===== TUMAN ADMINGA =====
        if location in DISTRICT_ADMINS:
            await bot.send_message(DISTRICT_ADMINS[location], text)

        # ===== ASOSIY GURUH =====
        await bot.send_message(ADMIN_CHAT_ID, text)

    except Exception as e:
        print("Xatolik:", e)
        await message.answer("❌ Xatolik yuz berdi")

    await message.answer("✅ So‘rovingiz qabul qilindi")
    await show_main_page(message, state)

# ===== RUN =====
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
