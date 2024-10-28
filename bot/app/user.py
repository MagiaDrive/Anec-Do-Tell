from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile
import os
import json

# File for handles commands from users
router_users = Router()

class BotStates(StatesGroup):
    waiting_for_answer = State()

def load_language(language_file):
    file_path = os.path.join('bot', 'app', 'resourses', language_file)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
msg_send = load_language('eng.json')

@router_users.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await message.answer("""Welcome to our bot - Anec-Do-Tell! Please enjoy your puns ans stories!\n\nAt this moment the Bot is in development
                            which means we cannot provide full service. Feel free to check the commands as /language to switch model language, 
                            /tell for new anecdote and /info for more information! \n------------------------\n Добро пожаловать в бот Анекдотель!
                            Здесь вы сможете насладиться анекдотами на английском и русском языках! На данный момент бот находится в разработке
                            и его функционал ограничен. Используйте команды /language для смены языковой модели бота, /tell для получения нового
                            анекдота и /info для дополнительнойинформации!""")
    await state.set_state(BotStates.waiting_for_answer)


@router_users.message(F.text == "/info")
async def info_called(message: Message, state: FSMContext):
    await message.answer(msg_send['info'])
    await state.set_state(BotStates.waiting_for_answer)


@router_users.message(F.text == "/language")
async def language_called(message: Message, state: FSMContext):
    eng_button = InlineKeyboardButton(text="English", callback_data="english")
    ru_button = InlineKeyboardButton(text="Русский", callback_data="russian")
    builder = InlineKeyboardBuilder()
    builder.add(eng_button)
    builder.add(ru_button)
    await message.answer(msg_send['lang_pick'],
                         reply_markup=builder.as_markup())


@router_users.callback_query(F.data == "russian")
async def ru_system(callback: CallbackQuery, state: FSMContext):
    msg_send = load_language('rus.json')
    await callback.message.answer(msg_send['language'])
    language = 1 
    await state.set_state(BotStates.waiting_for_answer)


@router_users.callback_query(F.data == "english")
async def eng_system(callback: CallbackQuery, state: FSMContext):
    msg_send = load_language('eng.json')
    await callback.message.answer(msg_send['language'])
    language = 0
    await state.set_state(BotStates.waiting_for_answer)


@router_users.message(F.text == "/tell")
async def info_called(message: Message, state: FSMContext):
    await message.answer(msg_send['tell'])
    await state.set_state(BotStates.waiting_for_answer)