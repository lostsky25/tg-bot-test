from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()

class CurrentView(StatesGroup):
    level = State()
    category_id = State()
    page = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(f'Добро пожаловать, {message.from_user.id}!', reply_markup=kb.main)

@router.message(F.text == 'Показать список категорий')
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Выберите категорию товара', reply_markup=await kb.categories(1, 1, None))
    
    await state.update_data(level = 1)
    await state.update_data(category_id = None)
    await state.update_data(page = None)


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery, state: FSMContext):
    _level = int(callback.data.split('_')[1])
    _category_id = int(callback.data.split('_')[2])
    
    await callback.answer('')
    await callback.message.edit_text('Выберите категорию товара', reply_markup=await kb.categories(_level + 1, _level, _category_id))
    await state.update_data(level = _level + 1)
    await state.update_data(category_id = _category_id)
    await state.update_data(page = None)

@router.callback_query(F.data == 'to_backward')
async def category(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    _level = data.get('level')
    _category_id = data.get('category_id')
    
    if _level - 1 == 1:
        await callback.answer('')
        await callback.message.edit_text('Выберите категорию товара', reply_markup=await kb.categories(1, 1, None))
    else:
        await callback.answer('')
        await callback.message.edit_text('Выберите категорию товара', reply_markup=await kb.categories(_level - 1, _level, _category_id))
        
    await state.update_data(level = _level - 1)
    await state.update_data(category_id = _category_id)
    await state.update_data(page = None)

@router.callback_query(F.data == 'to_main')
async def category(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text('Выберите категорию товара', reply_markup=await kb.categories(1, 1, None))
    
    await state.update_data(level = 1)
    await state.update_data(category_id = None)
    await state.update_data(page = None)

@router.callback_query(F.data.startswith('page_'))
async def set_keyboard_with_page(callback: CallbackQuery, state: FSMContext):
    go_to_page = int(callback.data.split('_')[1])
    data = await state.get_data()
    _level = data.get('level')
    _category_id = data.get('category_id')
    await state.update_data(page = go_to_page)

    await callback.answer('')
    await callback.message.edit_text('Выберите категорию товара', reply_markup=await kb.categories(_level, _level, _category_id, go_to_page))
