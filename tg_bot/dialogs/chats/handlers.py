from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from tortoise.exceptions import DoesNotExist

from ...db.models import BotUser, Region, Category, Form
from ...load_all import dp, bot
from . import texts, keyboards
from ...modules.edit_or_send_message import edit_or_send_message
from ...modules.filters import Button, IsBotNewChatMember, AddedByAdmin, FromChat, IsAdmin
import requests
import json


class States(StatesGroup):
    region = State()
    type_category = State()
    form = State()


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message, state: FSMContext):
    b, _ = await BotUser.get_or_create(tg_id=message.chat.id)
    await edit_or_send_message(bot, message, state, text=texts.region, kb=keyboards.region())
    await States.region.set()


async def get_regions(start_num: int, size: int = 50):
    regions = await Region.all()
    regions = sorted(regions, key=lambda a: a.id)
    overall_items = len(regions)
    if start_num >= overall_items:
        return []
    elif start_num + size >= overall_items:
        return regions[start_num:overall_items+1]
    else:
        return regions[start_num:start_num+size]


@dp.inline_handler(state="*")
async def inline_handler(query: types.InlineQuery):
    query_offset = int(query.offset) if query.offset else 0
    results = [types.InlineQueryResultArticle(
        id=str(region.id),
        title=region.name,
        input_message_content=types.InputTextMessageContent(
                message_text=region.name)
    ) for region in await get_regions(query_offset)]
    print(results, flush=True)
    if len(results) < 50:
        await query.answer(results, next_offset="")
    else:
        await query.answer(results, next_offset=str(query_offset+50))


@dp.message_handler(state=States.region)
async def region(message: types.Message, state: FSMContext, bot_user: BotUser):
    try:
        bot_user.region = await Region.get(name=message.text)
    except DoesNotExist:
        await edit_or_send_message(bot, message, state, text=texts.region__try_again, kb=keyboards.region())
    else:
        await bot_user.save()
        await edit_or_send_message(bot, message, state, text=texts.form, kb=await keyboards.form())
        await States.form.set()


@dp.callback_query_handler(state=States.form)
async def form(callback: types.CallbackQuery, state: FSMContext, bot_user: BotUser):
    try:
        bot_user.form = await Form.get(id=int(callback.data))
    except [DoesNotExist, ValueError]:
        await edit_or_send_message(bot, callback, state, text=texts.form__try_again, kb= await keyboards.form())
    else:
        await bot_user.save()
        await edit_or_send_message(bot, callback, state, text=texts.type_category, kb= await keyboards.type_category())
        await States.type_category.set()


@dp.callback_query_handler(state=States.type_category)
async def type_category(callback: types.CallbackQuery, state: FSMContext, bot_user: BotUser):
    try:
        bot_user.category = await Category.get(id=int(callback.data))
    except [DoesNotExist, ValueError]:
        await edit_or_send_message(bot, callback, state, text=texts.type_category__try_again, kb=await keyboards.type_category())
    else:
        await bot_user.save()
        await edit_or_send_message(bot, callback, state, text=texts.form, kb=await keyboards.form())
        await States.type_category.set()

# https://cptgrants.org/api/grants/ - получение информации о грантах
# https://cptgrants.org/api/grants/:id - получение информации о конкретном гранте
