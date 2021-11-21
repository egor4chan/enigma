from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import message
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.types import user
import data
import keyboard as kb

from pyqiwip2p import QiwiP2P
import random

utoken = '2133022895:AAHkiv8Lb8Z7C78V5MxFrtrrGuTlZuTJUHU'
admin = '2044405349'
qiwi_api = 'a9a2c31893e0242c91d6a3a0a90ae52b'
qiwi_num = False

refs_list = []

p2p = QiwiP2P(auth_key='eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6InJybHZ5bS0wMCIsInVzZXJfaWQiOiI3OTUwODMyNDUxNSIsInNlY3JldCI6IjU5OGYyZjY0NDc0ZWVmMDdkMmEyNjYwZjFjMzJkYmRmZTY5OGUyNWQ0MmVmOTMwYWQyZjUwZTE4M2JmNjA0NmIifX0=')

bot = Bot(token=utoken)
dp = Dispatcher(bot)



@dp.message_handler(commands=['start'])
async def process_help_command(message: types.Message):
    ref = message.text[7:] # REF = текст который идет после /start
    user = message.from_user.id
    if data.in_status_database(user) == False:
        data.register_user(user)
    else:
        pass
    if data.check_in_db(user) == False:
        if ref != '' and ref != user: # Если поле РЕФ не пустое
            if data.check_in_db(ref) == True: # если REF параметр есть в БД
                data.set_refer(ref, user)
                await message.reply("Вы успешно зарегистрированы. Ваш рефер: " + str(ref) + '\nПодробнее: /about', reply_markup=kb.menu )
                data.balance_up(ref, 1)
                await bot.send_message(ref, 'У вас новый реферал! Вас баланс пополнен.\nПовышайте обороты и зарабатывайте до 100 рублей за одно приглашение!')
            else: # если такого РЕФЕРА не существует
                data.set_refer(0, user)
                await message.reply('Вы успешно зарегистрированы без рефера!', reply_markup=kb.menu)
        else: # если поле реф пустое
            data.set_refer(0, user)
            await message.reply('Вы успешно зарегистрированы без рефера!', reply_markup=kb.menu)

    else: # Человек уже зарегистрирован и имеет рефера
        await message.answer('Вы успешно авторизованы!', reply_markup=kb.menu)

@dp.message_handler(text='Мой кабинет') # Команда генерирует реферальную ссылку пользователю
async def process_help_command(message: types.Message):
    user = message.from_user.id
    link = 't.me/obejan_bot/?start=' + str(message.from_user.id)
    all_users = data.get_all_users()
    myRefsCount = data.my_refs(user)
    status = data.return_status(user)
    if status == 'неактивен':
        await message.answer(f'Статус акканута: {status}\n\nВы пригласили: ' + str(myRefsCount) + '\nВсего человек зарегистрировано: ' + str(all_users) + '\n\nВаша реферальная ссылка: ' + str(link), reply_markup=kb.myrefs)
    else:
        await message.answer(f'Статус акканута: {status}\n\nВы пригласили: ' + str(myRefsCount) + '\nВсего человек зарегистрировано: ' + str(all_users) + '\n\nВаша реферальная ссылка: ' + str(link))

#@dp.message_handler(text='Что делать?') # Команда SLAVES генерирует реферальную ссылку пользователю
#async def process_help_command(message: types.Message):
#    await message.answer('Главные вопросы:\n\n 1. Что нужно делать?\nНужно приглашать людей в нашего бота по вашей реферальной ссылке, которую вы можете достать, нажав "Рефералы"')

@dp.message_handler(text='Мой кошелёк') # Команда SLAVES генерирует реферальную ссылку пользователю
async def process_help_command(message: types.Message):
    user = message.from_user.id
    local_balance = data.getBalance(user)
    await message.answer('Ваш баланс: ' + str(local_balance) + ' руб.', reply_markup=kb.wallet_menu)

@dp.callback_query_handler(lambda c: c.data == 'depout')
async def process_callback_button1(callback_query: types.CallbackQuery):
    user = callback_query.from_user.id
    balance = data.getBalance(user)
    number = data.get_number(user)
    await bot.answer_callback_query(callback_query.id)
    if data.return_number(user) == 'true':
        if int(balance) < 100:
            await bot.send_message(callback_query.from_user.id, 'Выводы доступны от 100 рублей.')
        else:
            await bot.send_message(callback_query.from_user.id, 'Заявка на вывод обрабатывается. Ожидайте.')
            await bot.send_message(admin, f'PANEL: Новая заявка на вывод!\n Сумма: {balance}\nНомер: {number}')
            data.balance_down(user, balance)
    else:
        await bot.send_message(user, 'Для начала привяжите номер.')

@dp.callback_query_handler(lambda c: c.data == 'qiwi')
async def process_callback_button1(callback_query: types.CallbackQuery):
    user = callback_query.from_user.id
    await bot.delete_message(user, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    msg = await bot.send_message(callback_query.from_user.id, 'Введите ваш QIWI в формате +79123456789')
    data.update_qiwi_status(user, 1)

@dp.message_handler()
async def process_help_command(message: types.Message):
    user = message.from_user.id
    message = message.text
    status_qiwi = data.qiwi_status(user)
    if status_qiwi == 1:
        if data.register_number(user, message) == 'success':
            await bot.send_message(user, 'Номер сохранен. Вы можете изменить его в любое время.')
            data.update_qiwi_status(user, 0)
        else:
            await bot.send_message(user, 'Введите корректный номер')
    else:
        pass

@dp.callback_query_handler(lambda c: c.data == 'activate')
async def process_callback_button1(callback_query: types.CallbackQuery):
    user = callback_query.from_user.id
    random_comment = str(str(user) + '_' + str(random.randint(100000, 999999)))
    bill = p2p.bill(amount=1, lifetime=15, comment=random_comment)

    data.add_check(user, 1, bill.bill_id)

    await bot.send_message(user, f'Вам нужно оплатить счет: \n{bill.pay_url}', reply_markup=kb.buy_menu(url=bill.pay_url, bill=bill.bill_id))


@dp.callback_query_handler(text_contains='check_')
async def check(callback_query: types.CallbackQuery):
    user = callback_query.from_user.id
    bill = str(callback_query.data[6:])
    info = data.get_check(bill)
    if info == False:
        if str(p2p.check(bill_id=bill).status) == "PAID":
            await bot.delete_message(user, callback_query.message.message_id)
            await bot.send_message(user, text='Счет оплачен. Ваш аккаунт активирован.')
            # НУЖНО СДЕЛАТЬ НАГРАДУ ДЛЯ РЕФЕРОВ
            data.delete_check(bill)
            data.set_status(user, 1)
        else:
            await bot.send_message(user, 'Не оплачено. Повтроите позже.', reply_markup=kb.buy_menu(False, bill=bill))
    else:
        await bot.send_message(user, 'Счет не найден')
        print(str(p2p.check(bill_id=bill).status))


@dp.message_handler(text='Акт')
async def process_help_command(message: types.Message):
    user = message.from_user.id # ЮЗЕР
    second_user = data.second_refer(user) # РЕФЕР
    third_user = data.third_refer(user) # РЕФЕР РЕФЕРА
    if second_user != '0': # ЕСЛИ РЕФЕР ЕСТЬ
        print(second_user)
        #data.balance_up(data.second_refer, 10)
        try:
            await bot.send_message(third_user, 'Вам зачилена награда директора. \nУ вас новый партнер!')
            await bot.send_message(second_user, 'Вам зачилена награда лидера. \nВаш реферал пригласил нового партнера.')
        except:
            print("Отправка сообщения недоступна")
        if third_user != '0':
            print(third_user)
            #data.balance_up(data.third_refer, 100)
            try:
                await bot.send_message(second_user, 'Вам зачилена награда лидера. \nВаш реферал пригласил нового партнера.')
            except:
                print("Отправка сообщения недоступна")
        else:
            print('Лидера ')
    else:
        pass


@dp.message_handler(text='Пользователи')
async def process_help_command(message: types.Message):
    all = len(data.get_refs(message.from_user.id))
    user = data.get_refs(message.from_user.id)
    number = 0
    userlist_refs = []
    for i in range(all):
        userlist_refs.append(user[number][0])
        number += 1
    await bot.send_message(message.from_user.id, userlist_refs)




if __name__ == '__main__':
    executor.start_polling(dp)
