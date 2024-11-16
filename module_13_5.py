from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

# Токен вашего бота
api = "Согласно заданию: не забудьте убрать ключ для подключения к вашему боту!"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Определяем состояния
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Создаем клавиатуру
def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Рассчитать", "Информация"]
    keyboard.add(*buttons)
    return keyboard

# Хэндлер для приветствия "Привет!"
@dp.message_handler(lambda message: message.text.lower() == "привет!")
async def greet(message: types.Message):
    await message.answer("Введите команду /start, чтобы начать общение.")

# Хэндлер команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот, помогающий твоему здоровью.\n"
        "Выберите одну из опций ниже:",
        reply_markup=get_main_keyboard()
    )

# Хэндлер нажатия кнопки "Рассчитать"
@dp.message_handler(text="Рассчитать")
async def set_age(message: types.Message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()

# Хэндлер для ввода возраста
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом. Попробуйте еще раз:")
        return
    await state.update_data(age=int(message.text))
    await message.answer("Введите свой рост в сантиметрах:")

    # Переход к следующему состоянию
    await UserState.growth.set()

# Хэндлер для ввода роста
@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Рост должен быть числом. Попробуйте еще раз:")
        return
    await state.update_data(growth=int(message.text))
    await message.answer("Введите свой вес в килограммах:")

    # Переход к следующему состоянию
    await UserState.weight.set()

# Хэндлер для ввода веса и расчета калорий
@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Вес должен быть числом. Попробуйте еще раз:")
        return
    await state.update_data(weight=int(message.text))
    data = await state.get_data()

    # Формула Миффлина - Сан Жеора для женщин:
    bmr = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] - 161
    await message.answer(f"Ваша норма калорий: {bmr:.2f}")

    # Завершаем состояние
    await state.finish()

# Хэндлер для кнопки "Информация"
@dp.message_handler(text="Информация")
async def info(message: types.Message):
    await message.answer(
        "Этот бот помогает рассчитать вашу норму калорий. "
        "Используйте кнопку 'Рассчитать', чтобы начать расчет."
    )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

###   Вывод в телеграмм-боте:
"""
Alex, [16.11.2024 16:04]
Привет!

Vika, [16.11.2024 16:04]
Введите команду /start, чтобы начать общение.

Alex, [16.11.2024 16:04]
/start

Vika, [16.11.2024 16:04]
Привет! Я бот, помогающий твоему здоровью.
Выберите одну из опций ниже:

Alex, [16.11.2024 16:04]
### отправлено сообщение с кнопки "Рассчитать":
Рассчитать

Vika, [16.11.2024 16:04]
Введите свой возраст:

Alex, [16.11.2024 16:04]
67

Vika, [16.11.2024 16:04]
Введите свой рост в сантиметрах:

Alex, [16.11.2024 16:04]
182

Vika, [16.11.2024 16:04]
Введите свой вес в килограммах:

Alex, [16.11.2024 16:04]
87

Vika, [16.11.2024 16:04]
Ваша норма калорий: 1511.50
"""