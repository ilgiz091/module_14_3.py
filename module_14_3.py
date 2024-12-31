from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

inline_kb = InlineKeyboardMarkup(resize_keyboard=True)
inline_kb2 = InlineKeyboardMarkup(resize_keyboard=True)
button_calories = InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')
button2_formulas = InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
button1_Product = InlineKeyboardButton('Продукт 1', callback_data='product_buying')
button2_Product = InlineKeyboardButton('Продукт 2', callback_data='product_buying')
button3_Product = InlineKeyboardButton('Продукт 3', callback_data='product_buying')
button4_Product = InlineKeyboardButton('Продукт 4', callback_data='product_buying')
inline_kb.add(button_calories, button2_formulas)
inline_kb2.row(button1_Product, button2_Product, button3_Product, button4_Product)



kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton('Рассчитать')
button2 = KeyboardButton('Информация')
button3 = KeyboardButton('Купить')
kb.add(button, button2)
kb.add(button3)

@dp.message_handler(commands = ['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

@dp.message_handler(text = 'Купить')
async def get_buying_list(message):
    product_images = [
        ('Astragalus Extract', 'Экстракт Астрагала 500 мг - 90 капсул', 100, 'files/product1.jpg'),
        ('Adam', 'Адам, Витамины для Мужчин Комплекс - 90 вегетарианских капсул', 200, 'files/product2.png'),
        ('OralBiotic', 'Оральный Биотик - 60 таблеток для рассасывания', 300, 'files/product3.png'),
        ('Quercetin & Bromelain', 'Кверцетин и Бромелаин - 120 капсул', 400, 'files/product4.png'),
    ]
    for name, description, price, img_path in product_images:
        await message.answer(f'Название: {name} | Описание: {description} | Цена: {price}')
        with open(img_path, 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=inline_kb2)

@dp.callback_query_handler(text = 'product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = inline_kb)

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес(кг)+6,25 х рост(см)-5 х возраст(г)-161')
    await call.answer()

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    calories = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.answer(f"Ваша норма калорий: {calories}")
    await state.finish()

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)