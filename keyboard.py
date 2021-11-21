from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


refs = KeyboardButton('Мой кабинет')
#top = KeyboardButton('Что делать?')
wallet = KeyboardButton('Мой кошелёк')

menu = ReplyKeyboardMarkup(resize_keyboard=True).row(refs).row(wallet)

update_cashup = InlineKeyboardButton('Увеличить оборот')

inline_rec = InlineKeyboardMarkup().add(update_cashup)



depout = InlineKeyboardButton('Вывести', callback_data='depout')
qiwi_connect = InlineKeyboardButton('Привязка QIWI', callback_data='qiwi')

wallet_menu = InlineKeyboardMarkup().add(depout).add(qiwi_connect)


act = InlineKeyboardButton('Активировать аккаунт', callback_data='activate')
#ref_link = InlineKeyboardButton('Скопиовать ссылку')
myrefs = InlineKeyboardMarkup().add(act)

my_profile = KeyboardButton('Hi Hitler')
profile = ReplyKeyboardMarkup(resize_keyboard=True).add(my_profile)


def buy_menu(isUrl=True, url='', bill=''):
    check_pay = InlineKeyboardMarkup()
    if isUrl:
        btnUrlQiwi = InlineKeyboardButton(text='Ссылка на оплату', url=url)
        check_pay.insert(btnUrlQiwi)

    check = InlineKeyboardButton(text='Проверить оплату', callback_data='check_'+bill)
    check_pay.insert(check)
    return check_pay
