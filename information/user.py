from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    cost = State()      #цена
    rooms = State()     # кол во комнат
    area = State()      # площадь объекта
    square = State()    # площадь двора(если это дом или зем.участок)
    tip = State()       # тип объекта 
    floors = State()    # кол во этажей
    rooms_house = State()
    area_house = State()
    square_house = State()
    password = State()

class Admin(StatesGroup):
    cost = State()      #цена
    rooms = State()     # кол во комнат
    area = State()      # площадь объекта
    square = State()    # площадь двора(если это дом или зем.участок)
    tip = State()       # тип объекта 
    floors = State()    # кол во этажей
    rooms_house = State()
    area_house = State()
    square_house = State()
    adress = State()
    link = State()
    
    access = State()
    obj_id = State()
    table = State()