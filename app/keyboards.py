from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.requests import get_prev_categories, get_next_categories

from aiogram import Router

router = Router()

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Показать список категорий')],
], 
resize_keyboard=True,
input_field_placeholder='Выберите пункт меню.')

def get_keyboard_with_pages(page, count_per_page, buttons):
    keyboard = InlineKeyboardBuilder()
    control_keyboard = InlineKeyboardBuilder()

    start = page * count_per_page
    end = start + count_per_page

    for button in buttons[start:end]:
        keyboard.add(button)
    
    if start == 0:
        control_keyboard.row(InlineKeyboardButton(text=" ", callback_data="_"), 
                    InlineKeyboardButton(text="➡️", callback_data=f"page_{page + 1}"))
    elif start > 0 and end < len(buttons) - 1:
        control_keyboard.row(InlineKeyboardButton(text="⬅️", callback_data=f"page_{page - 1}"), 
                    InlineKeyboardButton(text="➡️", callback_data=f"page_{page + 1}"))
    else:
        control_keyboard.row(InlineKeyboardButton(text="⬅️", callback_data=f"page_{page - 1}"), 
                    InlineKeyboardButton(text=" ", callback_data="_"))

    control_keyboard.row(InlineKeyboardButton(text='🔙 Назад', callback_data='to_backward'), InlineKeyboardButton(text='🏠 На главную', callback_data='to_main'))

    keyboard = keyboard.adjust(1)
    keyboard.attach(control_keyboard.adjust(2))

    return keyboard.as_markup()

async def categories(level, current_level, category_id, page = 0):
    all_categories = None
    if (current_level <= level):
        all_categories = await get_next_categories(level, category_id)
    else:
        all_categories = await get_prev_categories(level, category_id)

    keyboard = InlineKeyboardBuilder()

    count_categories = 0
    buttons = []
    for category in all_categories:

        if (level == 1):
            buttons.append(InlineKeyboardButton(text=category.name + ' ' + str(category.count) + ' шт.', callback_data=f'category_{level}_{category.id}'))
        elif (level == 2):
            buttons.append(InlineKeyboardButton(text=category.name + ' ' + str(category.count) + ' шт.', callback_data=f'category_{level}_{category.id}'))
        elif (level == 3):
            buttons.append(InlineKeyboardButton(text=category.name + ' ' + str(category.count) + ' шт.', callback_data=f'_'))
        # else:
        #     _callback_data = ''
            
        #     if (level == 3):
        #         _callback_data = f'_'
        #     else:
        #         _callback_data = f'category_{level}_{category.prev_category_id}'


        count_categories += 1

    if (count_categories > 20):
        return get_keyboard_with_pages(page, 4, buttons)
    else:
        keyboard.add(*buttons)

        if (level != 1):
            keyboard.add(InlineKeyboardButton(text='🔙 Назад', callback_data='to_backward'))
            keyboard.add(InlineKeyboardButton(text='🏠 На главную', callback_data='to_main'))
        
        return keyboard.adjust(1).as_markup()
