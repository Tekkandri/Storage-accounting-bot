from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
from database import sqlite_db
from config import tz
#----------common markup------------------------------
common_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="↩️В Главное меню",
                          callback_data="exit")]
], resize_keyboard=True)

common_and_continue_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Продолжить",
                          callback_data="continue")],
    [InlineKeyboardButton(text="↩️В Главное меню",
                          callback_data="exit")]
], resize_keyboard=True)

confirm_and_continue_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить товар",
                          callback_data="continue")],
    [InlineKeyboardButton(text="✅Подтвердить",
                          callback_data="confirm_action")]
], resize_keyboard=True)

#----------start markup-------------------------------
balance_info_btn = InlineKeyboardButton(text="💲Баланс/История пополнения",
                                        callback_data="balance_info")
top_up_balance_btn = InlineKeyboardButton(text="💳Пополнить баланс",
                                        callback_data="top_up")
buy_new_item_btn = InlineKeyboardButton(text="📦Покупка товара",
                                        callback_data="buy_new_item")
get_stat_btn = InlineKeyboardButton(text="📈Статистика месячная/дневная",
                                    callback_data = "stat")

start_markup = InlineKeyboardMarkup(inline_keyboard=[
    [balance_info_btn],
    [top_up_balance_btn],
    [buy_new_item_btn],
    [get_stat_btn]
], resize_keyboard=True)
#-----------------------------------------------------

#----------new balance markup-------------------------
new_balance_btn = InlineKeyboardButton(text="✅Пополнить",
                                       callback_data="confirm_top_up")
new_balance_markup = InlineKeyboardMarkup(inline_keyboard=[
    [new_balance_btn]
], resize_keyboard=True)
#-----------------------------------------------------
#----------new item markup----------------------------

confirm_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅Подтвердить",
                          callback_data="confirm_action")]
], resize_keyboard=True)

def build_item_markup() -> InlineKeyboardMarkup:
    list = []
    data_list = sqlite_db.get_categories()
    for data in data_list:
        if sqlite_db.get_price(data[0]) > 0:
           list.append([InlineKeyboardButton(text=data[0],
                                             callback_data=f"{data[0]}::cat")])
    list.append([InlineKeyboardButton(text="Прочее",
                                      callback_data="other")])
    return InlineKeyboardMarkup(inline_keyboard=list)

#-----------------------------------------------------
#----------stat markup--------------------------------
stat_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🗳️Месячная статистика закупок товара",
                          callback_data="month_item_stat")],
    [InlineKeyboardButton(text="💰Месячная статистика пополнений",
                          callback_data="month_money_stat")],
    [InlineKeyboardButton(text="🍱Дневная статистика закупок товара",
                          callback_data="day_item_stat")]
], resize_keyboard=True)

month_dict = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь"
}
month_item_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f"{month_dict[(datetime.now(tz=tz)-timedelta(days=60)).month]} {(datetime.now(tz=tz)-timedelta(days=60)).year}",
                          callback_data=f"{(datetime.now(tz=tz)-timedelta(days=60)).month}_{(datetime.now(tz=tz)-timedelta(days=60)).year}_item"),],
    [InlineKeyboardButton(text=f"{month_dict[(datetime.now(tz=tz)-timedelta(days=30)).month]} {(datetime.now(tz=tz)-timedelta(days=30)).year}",
                          callback_data=f"{(datetime.now(tz=tz)-timedelta(days=30)).month}_{(datetime.now(tz=tz)-timedelta(days=30)).year}_item"),],
    [InlineKeyboardButton(text=f"{month_dict[datetime.now(tz=tz).month]} {datetime.now(tz=tz).year}",
                          callback_data=f"{datetime.now(tz=tz).month}_{datetime.now(tz=tz).year}_item"),]
], resize_keyboard=True)

month_money_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f"{month_dict[(datetime.now(tz=tz)-timedelta(days=60)).month]} {(datetime.now(tz=tz)-timedelta(days=60)).year}",
                          callback_data=f"{(datetime.now(tz=tz)-timedelta(days=60)).month}_{(datetime.now(tz=tz)-timedelta(days=60)).year}_money"),],
    [InlineKeyboardButton(text=f"{month_dict[(datetime.now(tz=tz)-timedelta(days=30)).month]} {(datetime.now(tz=tz)-timedelta(days=30)).year}",
                          callback_data=f"{(datetime.now(tz=tz)-timedelta(days=30)).month}_{(datetime.now(tz=tz)-timedelta(days=30)).year}_money"),],
    [InlineKeyboardButton(text=f"{month_dict[datetime.now(tz=tz).month]} {datetime.now(tz=tz).year}",
                          callback_data=f"{datetime.now(tz=tz).month}_{datetime.now(tz=tz).year}_money"),],
], resize_keyboard=True)
#-----------------------------------------------------
#----------admin markup-------------------------------

main_admin_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Категории",
                          callback_data="check_categories")],
    [InlineKeyboardButton(text="Изменить историю пополнений",
                          callback_data="change_balance_hist")],
    [InlineKeyboardButton(text="Изменить текущий баланс",
                          callback_data="change_current_balance")],
    [InlineKeyboardButton(text="Удалить запись",
                          callback_data="delete")]
])

def get_admin_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[])
    data_list = sqlite_db.get_categories()
    for data in data_list:
        markup.inline_keyboard.append([InlineKeyboardButton(text=data[0],
                                                            callback_data=f"{data[0]}::cat")])
    markup.inline_keyboard.append([InlineKeyboardButton(text="Добавить категорию",
                                                       callback_data="add_category")])
    markup.inline_keyboard.append([InlineKeyboardButton(text="Назад",
                                                        callback_data="back_to_main_menu")])
    return markup

category_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Изменить цену",
                         callback_data="change_price")],
    [InlineKeyboardButton(text="Удалить категорию",
                          callback_data="delete_category")]
])
#-----------------------------------------------------