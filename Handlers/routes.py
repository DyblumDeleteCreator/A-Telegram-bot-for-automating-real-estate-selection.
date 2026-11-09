
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from information.user import Form, Admin
from aiogram.fsm.context import FSMContext 
from os import  getenv
from dotenv import load_dotenv
from DB.database import get_apartments, get_houses, get_lands, save_object, delete_object, podbor_apartments, podbor_houses, podbor_lands

load_dotenv()
PASSWORD = getenv('ADMIN_PASSWORD')


router = Router()

def get_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Заглянуть под капот бота)', url='https://github.com/DyblumDeleteCreator/A-Telegram-bot-for-automating-real-estate-selection./tree/main?tab=readme-ov-file')],
            [InlineKeyboardButton(text='Политика конфиденциальности', url='https://github.com/DyblumDeleteCreator/A-Telegram-bot-for-automating-real-estate-selection./blob/main/PRIVACY.md')],
            [InlineKeyboardButton(text='Пользовательское соглашение', url='https://github.com/DyblumDeleteCreator/A-Telegram-bot-for-automating-real-estate-selection./blob/main/TERMS.md')]
        ]
    )
    return keyboard

def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Начать подборку🏡')],
            [KeyboardButton(text='Связаться с Николаем📞')],
        ],
        
        resize_keyboard=True
    )


    return keyboard


def tip_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='дом'), KeyboardButton(text='квартира')],
            [KeyboardButton(text='земельный участок')],
        ],
        
        resize_keyboard=True
    )


    return keyboard

def admin_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Удалить'), KeyboardButton(text='Добавить')],
            [KeyboardButton(text='Посмотреть базу данных')],
        ],
        
        resize_keyboard=True
    )


    return keyboard

def admin_tip_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Дом'), KeyboardButton(text='Квартира')],
            [KeyboardButton(text='Земельный участок')],
        ],
        
        resize_keyboard=True
    )


    return keyboard

def admin_table_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='houses'), KeyboardButton(text='apartments')],
            [KeyboardButton(text='lands')],
        ],
        
        resize_keyboard=True
    )


    return keyboard


@router.message(Command('start'))
async def start(message: Message):
    await message.answer('Здравствуйте! Я бот-помощник риелтора Николая (Агентство недвижимости «Каян», г. Геленджик).\n\nПомогу вам быстро найти нужный объект без долгих поисков:\n\nКвартиры и апартаменты у моря и в жилых районах\n\nЧастные дома, коттеджи и участки\n\n\nНапиши /help для просмотра всех команд',
 reply_markup=get_main_reply_keyboard())


@router.message(Command('help'))
async def help(message: Message):
    await message.answer('Все команды нашего проекта:\n\n/start - запустить/перезапустить бота\n/help - все команды нашего проекта\n/podbor - запуск вашей подборки объекта\n/contact - контакты для связи с Николаем\n/about - информация о команде проекта')


@router.message(F.text == 'Начать подборку🏡')
@router.message(Command('podbor'))
async def podborka(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Давайте начнем нашу подборку!\n\nУкажите ваш максимальный бюджет(в виде числа,   Пример: "8000000", т.е вы конкретно в этом примере рассматриваете объекты ДО 8млн рублей):')
    await state.set_state(Form.cost)

@router.message(Form.cost, F.text)
async def process_cost(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Ваш бюджет должен быть записан в виде числа!\nНачните подбор заново с помощью команды /podbor')
        return            

    await state.update_data(cost=int(message.text))

    await message.answer('Какой тип объекта вы подбираете(выберите один из появившихся вариантов):',
    reply_markup=tip_keyboard())
    await state.set_state(Form.tip)

@router.message(Form.tip, F.text == 'квартира')
async def process_tip(message: Message, state: FSMContext):
    await state.update_data(tip=message.text)

    await message.answer('Укажите какая должна быть МИНИМАЛЬНАЯ площадь у вашей искомой квартиры(в виде числа,  Пример: "40", т.е вы конкретно в этом примере рассматриваете квартиры с площадью от 40 м2, указанное число должно быть выражено метрами квадратными):')
    await state.set_state(Form.area)
        
@router.message(Form.area, F.text)
async def process_area(message: Message, state: FSMContext):
        
    if not message.text.isdigit():
        await message.answer('Площадь искомой вами квартиры должна быть записана в виде числа!\nНачните подбор заново с помощью команды /podbor')
        return

    await state.update_data(area=float(message.text))

    await message.answer('Укажите сколько МИНИМУМ комнат должно быть в вашей искомой квартире(в виде числа   Пример: "1", т.е вы конкретно в этом примере рассматриваете квартиры с кол во комнат от 1-ой):')
    await state.set_state(Form.rooms)

@router.message(Form.rooms, F.text)
async def process_rooms(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Кол во комнат в искомой вами квартире должно быть записано в виде числа!\nНачните подбор заново с помощью команды /podbor')
        return

    await state.update_data(rooms=int(message.text))

    data = await state.get_data()
    cost = data.get('cost')
    area = data.get('area')
    rooms = data.get('rooms')
    results = await podbor_apartments(cost, rooms, area)
    
    if not results:
        await message.answer('К сожалению, квартир не найдено')
    else:
        await message.answer(f"Найдено квартир: {len(results)}")
        for r in results:
            await message.answer(f"🏬Найдена квартира:\n\n"f"Адрес: {r.get('adress')}\n\n"f"Цена: {r.get('cost')}\n\n"f"Площадь: {r.get('area')}\n\n"f"Комнат: {r.get('rooms')}\n\n"f"Фотографии и более подробная информация о квартире: {r.get('link')}")

@router.message(Form.tip, F.text == 'земельный участок')
async def process_tip(message: Message, state: FSMContext):
    await state.update_data(tip=message.text)
    
    await message.answer('Укажите какая МИНИМАЛЬНАЯ площадь должна быть у вашего искомого зем.участка(в виде числа, Пример: "10", т.е вы конкретно в этом примере рассматриваете зем.участки с площадью от 10 соток, указанное число должно быть выражено в сотках):')
    await state.set_state(Form.square)

@router.message(Form.square, F.text)
async def process_square(message: Message, state: FSMContext):
    if not message.text.isdigit():
            await message.answer('Площадь зем.участка должна быть записана в виде числа!\nНачните подбор заново с помощью команды /podbor')
            return

    await state.update_data(square=float(message.text))

    data = await state.get_data()
    cost = data.get('cost')
    square = data.get('square')
    results = await podbor_lands(cost, square)

    if not results:
        await message.answer('К сожалению, земельных участков не найдено')
    else:
        await message.answer(f"Найдено земельных участков: {len(results)}")
        for r in results:
            await message.answer(f"⛺Найден земельный участок:\n\n"f"Адрес: {r.get('adress')}\n\n"f"Цена: {r.get('cost')}\n\n"f"Площадь: {r.get('square')} соток\n\n"f"Фотографии и более подробная информация о зем участке: {r.get('link')}")


@router.message(Form.tip, F.text == 'дом')
async def process_tip(message: Message, state: FSMContext):
    await state.update_data(tip=message.text)

    await message.answer('Укажите какая должна быть МИНИМАЛЬНАЯ площадь у вашего искомого дома(в виде числа,  Пример: "130", т.е вы конкретно в этом примере рассматриваете дома с площадью от 130 м2, указанное число должно быть выражено метрами квадратными):')
    await state.set_state(Form.area_house)
        
@router.message(Form.area_house, F.text)
async def process_area_house(message: Message, state: FSMContext):
        
    if not message.text.isdigit():
        await message.answer('Площадь искомого вами дома должна быть записана в виде числа!\nНачните подбор заново с помощью команды /podbor')
        return

    await state.update_data(area_house=float(message.text))

    await message.answer('Укажите сколько МИНИМУМ комнат должно быть в вашем искомом доме(в виде числа   Пример: "3", т.е вы конкретно в этом примере рассматриваете дома с кол во комнат от 3-ех):')
    await state.set_state(Form.rooms_house)

@router.message(Form.rooms_house, F.text)
async def process_rooms_house(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Кол во комнат в искомом вами доме должно быть записано в виде числа!\nНачните подбор заново с помощью команды /podbor')
        return

    await state.update_data(rooms_house=int(message.text))

    await message.answer('Укажите какая МИНИМАЛЬНАЯ площадь должна быть у ДВОРА вашего искомого дома(в виде числа, Пример: "10", т.е вы конкретно в этом примере рассматриваете дома с двором, площадь которого начинается от 10 соток, указанное число должно быть выражено в сотках):')
    await state.set_state(Form.square_house)
    
@router.message(Form.square_house, F.text)
async def process_square_house(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Площадь ДВОРА должна быть записана в виде числа!\nНачните подбор заново с помощью команды /podbor')
        return
    await state.update_data(square_house=float(message.text))

    await message.answer('Укажите сколько этажей МИНИМУМ должно быть у искомого вами дома(в виде числа, Пример "2", т.e вы конкретно в этом примере рассматриваете дома с кол во этажей от 2-ух):')
    await state.set_state(Form.floors)

@router.message(Form.floors, F.text)
async def process_floors(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Кол во этажей искомого вами дома должно быть записано в виде числа!\nНачните подбор заново с помощью команды /podbor')
        return
    await state.update_data(floors=int(message.text))

    data = await state.get_data()
    cost = data.get('cost')
    area = data.get('area_house')
    rooms = data.get('rooms_house')
    square = data.get('square_house')
    floors = data.get('floors')
    results = await podbor_houses(cost, rooms, floors, area, square)
    
    if not results:
        await message.answer('К сожалению, домов не найдено')
    else:
        await message.answer(f"Найдено домов: {len(results)}")
        for r in results:
            await message.answer(f"🏡Найден дом: \n\n"f"Адрес: {r.get('adress')}\n\n"f"Цена: {r.get('cost')}\n\n"f"Площадь дома: {r.get('area')}\n\n"f"Площадь двора: {r.get('square')} соток\n\n"f"Комнат: {r.get('rooms')}\n\n"f"Этажей: {r.get('floors')}\n\n"f"Фотографии и более подробная информация о доме: {r.get('link')} ")


@router.message(F.text == 'Связаться с Николаем📞')
@router.message(Command('contact'))
async def contact(message: Message):
    await message.answer('Контакты Николая:\n\nНомер телефона: +7 (991) 357-00-10\nTelegramm: @nikolay_kayan')

@router.message(Command('about'))
async def about(message: Message):
    await message.answer('Бот создан для защиты проекта по теме:\nПрименение языка программирования Python для создания сервиса автоматического подбора коммерческой и жилой недвижимости.\n\nРазработчик бота: Гриценко Иван\n\nТестер: Михаил Куценко\n\nРуководитель проекта: Антоненко Яна Вячеславна', reply_markup=get_inline_keyboard()) 

#_________________________________________________________________________________________________
#Админ панель
@router.message(Command('admin'))
async def admin_panel(message: Message, state: FSMContext):
    await message.answer('Введите пароль для входа в админ панель:')
    await state.set_state(Form.password)

@router.message(Form.password, F.text)
async def start_admin_panel(message: Message, state: FSMContext):
    if message.text != PASSWORD:
        await message.answer('Пароль неверный')
        return
    await message.answer('Добро пожаловать в админ панель!\n\nВыберите действие:', reply_markup=admin_keyboard())
    await state.set_state(Admin.access)

@router.message(Admin.access, F.text == 'Добавить')
async def admin_add(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Укажите цену объекта:')
    await state.set_state(Admin.cost)

@router.message(Admin.cost, F.text)
async def admin_cost(message: Message, state: FSMContext):
    await state.update_data(cost=int(message.text))

    await message.answer('выберите тип объекта:', reply_markup=admin_tip_keyboard())
    await state.set_state(Admin.tip)

@router.message(Admin.tip, F.text == 'Квартира')
async def admin_tip(message: Message, state: FSMContext):
    await state.update_data(tip=message.text)

    await message.answer('Укажите площадь квартиры:')
    await state.set_state(Admin.area)
        
@router.message(Admin.area, F.text)
async def admin_area(message: Message, state: FSMContext):
    await state.update_data(area=float(message.text))

    await message.answer('Укажите кол во комнат в квартире:')
    await state.set_state(Admin.rooms)

@router.message(Admin.rooms, F.text)
async def admin_rooms(message: Message, state: FSMContext):
    await state.update_data(rooms=int(message.text))
    
    await message.answer('Укажите полный адрес квартиры:')
    await state.set_state(Admin.adress)

@router.message(Admin.adress, F.text)
async def adress_apartment(message: Message, state: FSMContext):
    await state.update_data(adress=message.text)

    await message.answer('Укажите ссылку на объявление:')
    await state.set_state(Admin.link)

@router.message(Admin.link, F.text)
async def link_apartment(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    data = await state.get_data()
    await save_object(data)

@router.message(Admin.tip, F.text == 'Земельный участок')
async def admin_tip(message: Message, state: FSMContext):
    await state.update_data(tip=message.text)
    
    await message.answer('Укажите площадь зем участка в сотках:')
    await state.set_state(Admin.square)

@router.message(Admin.square, F.text)
async def admin_square(message: Message, state: FSMContext):
    await state.update_data(square=float(message.text))
    
    await message.answer('Укажите полный адрес зем участка:')
    await state.set_state(Admin.adress)
    
@router.message(Admin.adress, F.text)
async def adress_land(message: Message, state: FSMContext):
    await state.update_data(adress=message.text)
    
    await message.answer('Укажите ссылку на объявление:')
    await state.set_state(Admin.link)
    
@router.message(Admin.link, F.text)
async def link_land(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    data = await state.get_data()
    await save_object(data)
    
@router.message(Admin.tip, F.text == 'Дом')
async def admin_tip(message: Message, state: FSMContext):
    await state.update_data(tip=message.text)

    await message.answer('Укажите площадь дома:')
    await state.set_state(Admin.area_house)
        
@router.message(Admin.area_house, F.text)
async def admin_area_house(message: Message, state: FSMContext):
    await state.update_data(area_house=float(message.text))

    await message.answer('Укажите кол во комнат в доме:')
    await state.set_state(Admin.rooms_house)

@router.message(Admin.rooms_house, F.text)
async def admin_rooms_house(message: Message, state: FSMContext):
    await state.update_data(rooms_house=int(message.text))

    await message.answer('Укажите площадь двора в сотках:')
    await state.set_state(Admin.square_house)
    
@router.message(Admin.square_house, F.text)
async def admin_square_house(message: Message, state: FSMContext):
    await state.update_data(square_house=float(message.text))

    await message.answer('Укажите кол во этажей в доме:')
    await state.set_state(Admin.floors)

@router.message(Admin.floors, F.text)
async def admin_floors(message: Message, state: FSMContext):
    await state.update_data(floors=int(message.text))

    await message.answer('Укажите полный адрес дома:')
    await state.set_state(Admin.adress)

@router.message(Admin.adress, F.text)
async def adress_house(message: Message, state: FSMContext):
    await state.update_data(adress=message.text)

    await message.answer('Укажите ссылку на объявление:')
    await state.set_state(Admin.link)

@router.message(Admin.link, F.text)
async def link_house(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    data = await state.get_data()
    await save_object(data)

@router.message(Admin.access, F.text == 'Посмотреть базу данных')
async def admin_get_bd(message: Message, state: FSMContext):
    apartments = await get_apartments()
    houses = await get_houses()
    lands = await get_lands()

    for apt in apartments:
        await message.answer(f"🏥Квартира:\n"f"id: {apt.get('id')}\n"f"Адрес: {apt.get('adress')}\n"f"Ссылка: {apt.get('link')}")

    for h in houses:
        await message.answer(f"💒Дом:\n"f"id: {h.get('id')}\n"f"Адрес: {h.get('adress')}\n"f"Ссылка: {h.get('link')}")

    for l in lands:
        await message.answer(f"⛺Участок:\n"f"id: {l.get('id')}\n"f"Адрес: {l.get('adress')}\n"f"Ссылка: {l.get('link')}")

@router.message(Admin.access, F.text == 'Удалить')
async def admin_delete_start(message: Message, state: FSMContext):
    await message.answer('Укажите id объекта, который нужно удалить:')
    await state.set_state(Admin.obj_id)

@router.message(Admin.obj_id, F.text)
async def admin_table_start(message: Message, state: FSMContext):
    await state.update_data(obj_id=int(message.text))

    await message.answer('Выберите таблицу из которой нужно удалить объект:', reply_markup=admin_table_keyboard() )
    await state.set_state(Admin.table)

@router.message(Admin.table, F.text)
async def admin_delete(message: Message, state: FSMContext):
    await state.update_data(table=message.text)
    data = await state.get_data()
    obj_id = data.get('obj_id')
    table = data.get('table')
    await delete_object(table, obj_id)
    await message.answer('Объект удален!')
        
