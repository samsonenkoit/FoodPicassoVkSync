import os
import uuid
import time

from import_order_to_picasso_lambda import build_food_picasso_order_from_telegram_order
from picasso_food import (
    FoodPicassoMenu,
    FoodPicassoOrder,
    FoodPicassoOrderClient,
    FoodPicassoOrderDeliveryType,
    FoodPicassoOrderPosition,
    PicassoClient,
)
from telegram_food import TelegramDeliveryType, TelegramOrder, parse_telegram_order_from_url_dict

"https://docs.google.com/document/d/1kgIDiM0EK-W9Vmg7C_mNe9Rfu9QNZHeUQ1OPMn_C4sQ/edit?tab=t.0"

app2 = {
    "event": ["NEW_ORDER"],
    "data[id]": ["21852"],
    "data[point][id]": ["5"],
    "data[point][name]": ["Салмон Ролл"],
    "data[client][id]": ["24296"],
    "data[client][chat_id]": ["867142138"],
    "data[client][username]": ["sams_r777"],
    "data[client][created_at]": ["1729593711"],
    "data[client][name]": ["Роман"],
    "data[client][lastname]": ["С"],
    "data[client][phone]": ["79139767750"],
    "data[client][bonus]": ["500"],
    "data[client][count_orders]": ["6"],
    "data[client][amount_orders]": ["14505"],
    "data[client][kicked]": ["0"],
    "data[client][active]": ["1"],
    "data[status][id]": ["21"],
    "data[status][name]": ["Новый"],
    "data[status][color]": ["#0ced32"],
    "data[status][sort]": ["0"],
    "data[status][global]": ["new"],
    "data[receipt][id]": ["2"],
    "data[receipt][name]": ["Самовывоз"],
    "data[receipt][global]": ["pickup"],
    "data[payment][id]": ["10"],
    "data[payment][name]": ["Наличными"],
    "data[payment][global]": ["cash"],
    "data[fields][0][id]": ["103"],
    "data[fields][0][name]": ["Комментарий к заказу"],
    "data[fields][0][value]": ["ТЕСТ ЗАКАЗ"],
    "data[created_at]": ["1736594296"],
    "data[price_products]": ["4799.00"],
    "data[discount_bonus]": ["0.00"],
    "data[basket][0][product_id]": ["34054"],
    "data[basket][0][product_data][id]": ["34054"],
    "data[basket][0][product_data][name]": ["Филадельфия макси"],
    "data[basket][0][product_data][description]": [
        "Состав: рис, нори, сыр, огурчик, ролл обёрнут в полный оборот в сёмгу с/с\r\n603ккал\r\n360гр\r\n8шт порция"
    ],
    "data[basket][0][quantity]": ["1"],
    "data[basket][0][price]": ["1499.00"],
    "data[basket][0][amount]": ["1499"],
    "data[basket][1][product_id]": ["37390"],
    "data[basket][1][product_data][id]": ["37390"],
    "data[basket][1][product_data][name]": ["Тортилья с сёмгой с/с "],
    "data[basket][1][product_data][description]": [
        "Состав: тортилья, семга с/с, имбирь, авокадо, поливается спайси соусом"
    ],
    "data[basket][1][quantity]": ["1"],
    "data[basket][1][price]": ["690.00"],
    "data[basket][1][amount]": ["690"],
    "data[basket][2][product_id]": ["37389"],
    "data[basket][2][product_data][id]": ["37389"],
    "data[basket][2][product_data][name]": ["Тортилья Мидори"],
    "data[basket][2][product_data][description]": [
        "Состав: тортилья, жаренная сёмга, перец болгарский, поливается спайси соусом"
    ],
    "data[basket][2][quantity]": ["1"],
    "data[basket][2][price]": ["640.00"],
    "data[basket][2][amount]": ["640"],
    "data[basket][3][product_id]": ["37388"],
    "data[basket][3][product_data][id]": ["37388"],
    "data[basket][3][product_data][name]": ["Тортилья с копчёной сёмгой"],
    "data[basket][3][product_data][description]": [
        "Состав: тортилья, сёмга х/к, лук зелёный"
    ],
    "data[basket][3][quantity]": ["1"],
    "data[basket][3][price]": ["680.00"],
    "data[basket][3][amount]": ["680"],
    "data[basket][4][product_id]": ["37386"],
    "data[basket][4][product_data][id]": ["37386"],
    "data[basket][4][product_data][name]": ["Мехико"],
    "data[basket][4][product_data][description]": [
        "Состав: рис, сыр, нори, болгарский перец, лук зеленый, сёмга х/к"
    ],
    "data[basket][4][quantity]": ["1"],
    "data[basket][4][price]": ["690.00"],
    "data[basket][4][amount]": ["690"],
    "data[basket][5][product_id]": ["37387"],
    "data[basket][5][product_data][id]": ["37387"],
    "data[basket][5][product_data][name]": ["Колорадо"],
    "data[basket][5][product_data][description]": [
        "Состав: тунец, имбирь, помидор, обернут в кунжут"
    ],
    "data[basket][5][quantity]": ["1"],
    "data[basket][5][price]": ["600.00"],
    "data[basket][5][amount]": ["600"],
}

appOrderUrlDict = {
    "event": ["NEW_ORDER"],
    "data[id]": ["21841"],
    "data[point][id]": ["5"],
    "data[point][name]": ["Салмон Ролл"],
    "data[address][id]": ["5869"],
    "data[address][addres]": ["Россия, Омск, улица Дмитриева, 11/3"],
    "data[address][coordinates][0]": ["73.309452"],
    "data[address][coordinates][1]": ["54.980354"],
    "data[client][id]": ["24296"],
    "data[client][chat_id]": ["867142138"],
    "data[client][username]": ["sams_r777"],
    "data[client][created_at]": ["1729593711"],
    "data[client][name]": ["Роман"],
    "data[client][lastname]": ["С"],
    "data[client][phone]": ["79139767750"],
    "data[client][bonus]": ["500"],
    "data[client][count_orders]": ["5"],
    "data[client][amount_orders]": ["14505"],
    "data[client][kicked]": ["0"],
    "data[client][active]": ["1"],
    "data[status][id]": ["21"],
    "data[status][name]": ["Новый"],
    "data[status][color]": ["#0ced32"],
    "data[status][sort]": ["0"],
    "data[status][global]": ["new"],
    "data[receipt][id]": ["1"],
    "data[receipt][name]": ["Доставка"],
    "data[receipt][global]": ["delivery"],
    "data[payment][id]": ["181"],
    "data[payment][name]": ["Безналичный"],
    "data[payment][global]": ["cash"],
    "data[fields][0][id]": ["103"],
    "data[fields][0][name]": ["Комментарий к заказу"],
    "data[fields][0][value]": ["ТЕСТ ЗАКАЗ"],
    "data[created_at]": ["1736593520"],
    "data[price_products]": ["1750.00"],
    "data[price_delivery]": ["400.00"],
    "data[discount_bonus]": ["0.00"],
    "data[basket][0][product_id]": ["37898"],
    "data[basket][0][product_data][id]": ["37898"],
    "data[basket][0][product_data][name]": ['Моти "Чёрная смородина"'],
    "data[basket][0][product_data][description]": [
        "Состав: Творожный сыр, сливки 33%, белый шоколад, смородиновая начинка(чёрная смородина, сахар).\r\nМоти нужно разморозить в холодильнике, это займёт 30 минут. \r\nСрок годности в холодильнике 48 часов, в морозилке 30 дней.\r\nЕсли кушать подмороженным-на вкус будет как мороженое, если дать полностью растаять-это настоящий десерт моти."
    ],
    "data[basket][0][quantity]": ["7"],
    "data[basket][0][price]": ["250.00"],
    "data[basket][0][amount]": ["1750"],
}

FOOD_PICASSO_API_URL = "https://api-ru6.posterix.pro/v2"
FOOD_PICASSO_MENU_ID = 2
FOOD_PICASSO_COMPANY_ID = 3028
FOOD_PICASSO_TOKEN = "1d15f821dadf1ba043291eae570440e53fae3baa"

picassoClient = PicassoClient(
    url=FOOD_PICASSO_API_URL,
    token=FOOD_PICASSO_TOKEN,
    companyId=FOOD_PICASSO_COMPANY_ID,
)

menu = picassoClient.load_menu(2)

telegramOrder = parse_telegram_order_from_url_dict(appOrderUrlDict)
foodPicassoMenu = picassoClient.load_menu(FOOD_PICASSO_MENU_ID)

foodPicassoOrder = build_food_picasso_order_from_telegram_order(
    telegramOrder, foodPicassoMenu
)

picassoClient.add_order(foodPicassoOrder)
