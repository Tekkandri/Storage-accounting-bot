from aiogram.fsm.state import StatesGroup, State

class FSMstates(StatesGroup):
    GET_NUM = State()
    BUY_NEW_ITEM = State()
    GET_COUNT = State()
    GET_AUTO = State()
    ADMIN_PASS_STATE = State()
    BALANCE_PASS_STATE = State()
    ADMIN_STATE = State()
    DELETE_PURCHASE_STATE = State()
    GET_PRICE = State()
    GET_OTHER_ITEMS = State()
    GET_OTHER_ITEMS_SUM = State()
    GET_CATEGORY_NAME = State()
    CATEGORY = State()
    CHANGE_BALANCE_HIST = State()
    CHANGE_CUR_BALANCE = State()