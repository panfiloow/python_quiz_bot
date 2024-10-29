from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

quiz_data = [
    {
        'question': 'Что такое Python?',
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
        'correct_option': 0
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0
    },
    {
        'question': 'Какова основная задача интерпретатора Python?',
        'options': ['Скомпилировать код', 'Выполнить код', 'Создать виртуальную машину', 'Сгенерировать отчет'],
        'correct_option': 1
    },
    {
        'question': 'Какова основная задача компилятора Python?',
        'options': ['Выполнить код', 'Скомпилировать код', 'Создать виртуальную машину', 'Сгенерировать отчет'],
        'correct_option': 1
    },
    {
        'question': 'Какова основная задача виртуальной машины Python?',
        'options': ['Скомпилировать код', 'Выполнить код', 'Создать виртуальную машину', 'Сгенерировать отчет'],
        'correct_option': 1
    },
    {
        'question': 'Какова основная задача отладчика Python?',
        'options': ['Скомпилировать код', 'Выполнить код', 'Создать виртуальную машину', 'Отлаживать код'],
        'correct_option': 3
    },
    {
        'question': 'Какова основная задача профилировщика Python?',
        'options': ['Скомпилировать код', 'Выполнить код', 'Создать виртуальную машину', 'Измерять производительность кода'],
        'correct_option': 3
    },
    {
        'question': 'Какова основная задача статического анализатора Python?',
        'options': ['Скомпилировать код', 'Выполнить код', 'Создать виртуальную машину', 'Проверять код на ошибки'],
        'correct_option': 3
    },
    {
        'question': 'Какова основная задача динамического анализатора Python?',
        'options': ['Скомпилировать код', 'Выполнить код', 'Создать виртуальную машину', 'Проверять код на ошибки'],
        'correct_option': 3
    },
    {
        'question': 'Какова основная задача тестировщика Python?',
        'options': ['Скомпилировать код', 'Выполнить код', 'Создать виртуальную машину', 'Проверять код на ошибки'],
        'correct_option': 3
    }
]

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=f"{option}_answer" if option != right_answer else "right_answer")
        )

    builder.adjust(1)
    return builder.as_markup()