from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

from configurebot import cfg

mainmenunewsupport = KeyboardButton(cfg['button_new_question'])
mainmenuabout = KeyboardButton(cfg['button_about_us'])
mainmenucomplete = KeyboardButton(cfg['button_complete'])
inline_question_accept_btn = InlineKeyboardButton(cfg['inline_btn_accept_question'],callback_data='accept_btn')
inline_question_accept_kb = InlineKeyboardMarkup().add(inline_question_accept_btn)

inline_start_chat_btn = InlineKeyboardButton(cfg['inline_btn_start_chat'],callback_data='start_chat_btn')
inline_start_chat_kb = InlineKeyboardMarkup().add(inline_start_chat_btn)

mainmenu = ReplyKeyboardMarkup(resize_keyboard=True).row(mainmenunewsupport, mainmenucomplete, mainmenuabout)