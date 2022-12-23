from aiogram import types

import kb
from bot import dp, bot
from handlers.fsm import *
from handlers.db import db_profile_exist, db_profile_insertone, db_profile_banned, db_statistics_insertone, \
    db_statistics_updateone, db_statistics_find_last
from configurebot import cfg
import datetime
from handlers.fsm import echo

welcomemessage = cfg['welcome_message']
errormessage = cfg['error_message']
devid = cfg['dev_id']
aboutus = cfg['about_us']
question_first_msg = cfg['question_type_ur_question_message']
complete_message = cfg['complete_message']

handler_button_new_question = cfg['button_new_question']
handler_button_about_us = cfg['button_about_us']
handler_button_complete = cfg['button_complete']


async def client_start(message: types.Message):
    try:
        if(message.chat.type != 'private'):
            await message.answer('Данную команду можно использовать только в личных сообщениях с ботом.')
            return
        if db_profile_exist(message.from_user.id):
            await message.answer(f'{welcomemessage}',parse_mode='Markdown', reply_markup=kb.mainmenu)
        else:
            db_profile_insertone({
                '_id': message.from_user.id,
                'username': message.from_user.username,
                'access': 0,
                'ban': 0,
                'joined': (datetime.datetime.now())
            })
            print('Новый пользователь!')
            await message.answer(f'{welcomemessage}',parse_mode='Markdown', reply_markup=kb.mainmenu)
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{errormessage}",
                             parse_mode='Markdown')
        await bot.send_message(devid, f"Случилась *ошибка* в чате *{cid}*\nСтатус ошибки: `{e}`",
                               parse_mode='Markdown')

async def client_newquestion(message: types.Message):
    try:
        if message.text == handler_button_new_question:
            await message.answer(f"Введите предмет:")
            await FSMQuestion.subject.set()

        elif message.text == handler_button_about_us:
            await message.answer(f"{aboutus}", disable_web_page_preview=True, parse_mode='Markdown')

        elif message.text == handler_button_complete:
            await message.answer(f"{complete_message}", disable_web_page_preview=True, parse_mode='Markdown')
            # TODO Инфа уходит в базу и статус вопроса выполнен
            id = (db_statistics_find_last({'user_id': message.from_user.id})['_id'])
            db_statistics_updateone({'_id': id}, {"$set": {"status": 1, "updated_at":(datetime.datetime.now())}})
            FSMQuestion.canChat = False

        elif FSMQuestion.canChat == True:
            #await echo(message)  1 - variant
            await echo(message, FSMQuestion.support_id, FSMQuestion.student_id)
            print(message)

    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{errormessage}",
                             parse_mode='Markdown')
        await bot.send_message(devid, f"Случилась *ошибка* в чате *{cid}*\nСтатус ошибки: `{e}`",
                               parse_mode='Markdown')


async def client_getgroupid(message: types.Message):
    try:
        await message.answer(f"Chat id is: *{message.chat.id}*\nYour id is: *{message.from_user.id}*", parse_mode='Markdown')
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{errormessage}",
                             parse_mode='Markdown')
        await bot.send_message(devid, f"Случилась *ошибка* в чате *{cid}*\nСтатус ошибки: `{e}`",
                               parse_mode='Markdown')

def register_handler_client():
    dp.register_message_handler(client_start, commands='start', state=None)
    dp.register_message_handler(client_getgroupid, commands='getchatid')
    dp.register_message_handler(client_newquestion)