from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import kb
from bot import bot,dp
from configurebot import cfg
from handlers.db import db_statistics_insertone, db_statistics_updateone, db_statistics_find_last
import datetime

question_first_msg = cfg['question_type_ur_question_message']
tehchatid = cfg['teh_chat_id']
message_seneded = cfg['question_ur_question_sended_message']

class FSMQuestion(StatesGroup):
	subject = State()
	topic = State()
	text = State()
	canChat = State(False)
	support_id = State()
	student_id = State()

# Обработчик инлайн кнопки accept
@dp.callback_query_handler(lambda c: c.data == 'accept_btn')
async def process_callback_accept_btn(callback_query: types.CallbackQuery):
	#await bot.answer_callback_query(callback_query.id)
	await bot.send_message(tehchatid, f'Запрос принял:\n@{callback_query.from_user.username}')
	await bot.send_message(callback_query.from_user.id, f'Вы приняли запрос:\n\n{callback_query.message.text}', reply_markup = kb.inline_start_chat_kb)
	await bot.edit_message_reply_markup(chat_id=tehchatid,message_id=callback_query.message.message_id, reply_markup=None)

# Обработчик инлайн кнопки start_chat_btn
@dp.callback_query_handler(lambda c: c.data == 'start_chat_btn')
async def process_callback_start_chat_btn(callback_query: types.CallbackQuery):
	await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,message_id=callback_query.message.message_id, reply_markup=None)
	user_id = int(callback_query.message.text.split("ответ ")[1].split(' ')[0].strip())
	id = (db_statistics_find_last({'user_id': user_id})['_id'])
	db_statistics_updateone({'_id': id}, {f"$set": {"accepted": callback_query.from_user.username, "updated_at": (datetime.datetime.now())}})
	await bot.send_message(callback_query.from_user.id, 'Напишите ответ:')
	FSMQuestion.canChat = True
	FSMQuestion.support_id = callback_query.from_user.id
	FSMQuestion.student_id = user_id
	print(f'Принял запрос --- {FSMQuestion.support_id}')
	print(f'Задал вопрос --- {user_id}')




# Обработчики
async def newquestion(message: types.Message, state: FSMContext):
	subject = ''
	topic = ''
	async with state.proxy() as data:
		if (message.content_type == 'photo'):
			data['text'] = message.caption
		else:
			data['text'] = message.text
	await state.finish()
	if(message.chat.username == None):
		who = "Ник не установлен"
	else:
		who = "@"+message.chat.username



	if(message.content_type=='photo'):
		ph = message.photo[0].file_id
		await message.reply(f"{message_seneded}",
							parse_mode='html')
		await bot.send_photo(tehchatid, ph, caption=f"✉ | Новый вопрос\n👤 От: {who}\n📚 Предмет: `{data['subject']}`\n🔴 Тема: `{data['topic']}`\n\n❓ Вопрос: `{data['text']}`\n\n📝 Чтобы ответить введите `/ответ {message.chat.id} Ваш ответ`",parse_mode='Markdown',reply_markup=kb.inline_question_accept_kb)
	else:
		await message.reply(f"{message_seneded}",
							parse_mode='html')
		await bot.send_message(tehchatid,
							   f"✉ | Новый вопрос\n👤 От: {who}\n📚 Предмет: `{data['subject']}`\n🔴 Тема: `{data['topic']}`\n\n❓ Вопрос: `{data['text']}`\n\n📝 Чтобы ответить введите `/ответ {message.chat.id} Ваш ответ`", parse_mode='html',reply_markup=kb.inline_question_accept_kb)
	db_statistics_insertone({
		'user_id': message.from_user.id,
		'username': message.from_user.username,
		'subject': data['subject'],
		'topic': data['topic'],
		'status': 0,
		'accepted':0,
		'created_at': (datetime.datetime.now()),
		'updated_at': (datetime.datetime.now())
	})



async def set_subject(message: types.Message, state: FSMContext):
	await state.update_data(subject=message.text)
	await message.answer("Введите тему: ")
	await FSMQuestion.topic.set()

async def set_topic(message: types.Message, state: FSMContext):
	await state.update_data(topic=message.text)
	await message.answer(f"{question_first_msg}")
	await FSMQuestion.text.set()

# async def chat_to_user(message: types.Message, state: FSMContext):
# 	await state.update_data(to_user=message.text)
# 	await bot.send_message(1191068911, FSMContext.data['to_user'])
# 	await FSMQuestion.from_user.set()
#
# async def chat_from_user(message: types.Message, state: FSMContext):
# 	await bot.send_message(1191068911, FSMContext.data['to_user'])
# 	await state.update_data(from_user=message.text)
# 	await bot.send_message(5113744460, FSMContext.data['from_user'])
# 	await FSMQuestion.chat_to_user.set()

# Рабочий вариант только без ограничения участников
# async def echo(message: types.Message):
# 	if message.from_user.id != FSMQuestion.support_id:
# 		print('Echo condition True')
# 		await bot.send_message(FSMQuestion.support_id, message.text)
# 	else:
# 		print('Echo condition False')
# 		await bot.send_message(FSMQuestion.student_id, message.text)

async def echo(message: types.Message, support, student):
	if message.from_user.id != support:
		await bot.send_message(support, message.text)
	else:
		await bot.send_message(student, message.text)


def register_handler_FSM():
	dp.register_message_handler(set_subject,state=FSMQuestion.subject, content_types=['text'])
	dp.register_message_handler(set_topic,state=FSMQuestion.topic, content_types=['text'])
	dp.register_message_handler(newquestion,state=FSMQuestion.text, content_types=['photo', 'text'])



