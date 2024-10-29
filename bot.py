import aiosqlite
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F
from config import API_TOKEN, DB_NAME
from database import create_table, update_quiz_index, get_quiz_index, update_quiz_result
from questions import quiz_data, generate_options_keyboard

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()
# Словарь для хранения результатов квиза
user_results = {}

# Словарь для подсчета правильных ответов
user_correct_answers = {}


async def set_bot_commands():
    commands = [
        types.BotCommand(command="/start", description="Запуск бота"),
        types.BotCommand(command="/quiz", description="Начать новый квиз"),
        types.BotCommand(command="/stats", description="Показать последний результат")
    ]
    await bot.set_my_commands(commands)


@dp.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']
    user_answer = quiz_data[current_question_index]['options'][correct_option]

    await callback.message.answer("Верно!")
    await callback.message.answer(f"Ваш ответ: {user_answer}")

    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)
    user_correct_answers[callback.from_user.id] = user_correct_answers.get(callback.from_user.id, 0) + 1

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await finish_quiz(callback.message, callback.from_user.id)

@dp.callback_query(F.data.endswith("_answer"))
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']
    correct_answer = quiz_data[current_question_index]['options'][correct_option]
    user_answer = callback.data.split("_")[0]

    await callback.message.answer(f"Неправильно. Правильный ответ: {correct_answer}")
    await callback.message.answer(f"Ваш ответ: {user_answer}")

    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await finish_quiz(callback.message, callback.from_user.id)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    user_correct_answers[user_id] = 0  
    await update_quiz_index(user_id, current_question_index)
    await get_question(message, user_id)

@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer(f"Давайте начнем квиз!")
    await new_quiz(message)

async def finish_quiz(message, user_id):
    await message.answer("Это был последний вопрос. Квиз завершен!")
    await message.answer("Вот ваш результат:")
    correct_answers = user_correct_answers[user_id]
    await message.answer(f"Вы ответили на {correct_answers} из {len(quiz_data)} вопросов")
    await update_quiz_result(user_id, correct_answers)

@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    user_id = message.from_user.id
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT result FROM quiz_results WHERE user_id = (?)', (user_id, )) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                await message.answer(f"Ваш последний результат: {results[0]} из {len(quiz_data)} вопросов")
            else:
                await message.answer("Вы еще не проходили квиз.")

async def main():
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())