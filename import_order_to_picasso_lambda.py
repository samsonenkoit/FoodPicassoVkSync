import base64
import json
import os
import time
import uuid
import urllib.parse
import urllib

from picasso_food import Address, FoodPicassoMenu, FoodPicassoOrder, FoodPicassoOrderClient, FoodPicassoOrderDeliveryType, FoodPicassoOrderPosition, PicassoClient
from telegram_food import TelegramDeliveryType, TelegramOrder, parse_telegram_order_from_base64_url, parse_telegram_order_from_url_dict


def handler(event, context):
    body = event['body']
    print(f'telegram url: {body}')

    token = os.environ['token']
    companyId = int(os.environ['companyId'])
    url = os.environ['url']
    menuId = int(os.environ['menuId'])

    picassoClient = PicassoClient(
        url=url,
        token=token,
        companyId=companyId,
    )
    decodedRequest = base64.b64decode(body).decode('utf-8')
    parsedDict = urllib.parse.parse_qs(decodedRequest)

    if not _is_new_order(parsedDict):
        print('not new order event')
        return

    telegramOrder = parse_telegram_order_from_url_dict(parsedDict)

    print(f'parsed telegram order: {telegramOrder}')
    foodPicassoMenu = picassoClient.load_menu(menuId)

    foodPicassoOrder = _build_food_picasso_order_from_telegram_order(
        telegramOrder, foodPicassoMenu
    )

    saveResult = picassoClient.add_order(foodPicassoOrder)
    print(f'save order result: {saveResult}')

    return {
        'statusCode': 200
    }


def _is_new_order(telegramOrder: dict) -> bool:
    return telegramOrder['event'][0].lower() == 'new_order'


def _parse_address(addressStr: str) -> Address:
    addressArray = addressStr.split(',')

    if len(addressArray) == 4:
        country, city, street, house = addressArray
        return Address(country=country,
                       city=city,
                       house=house,
                       street=street)
    else:
        country, city, street, house, entrance, floor, apartment = addressArray
        return Address(country=country,
                       city=city,
                       house=house,
                       street=street,
                       entrance=entrance,
                       floor=floor,
                       apartment=apartment)


def _build_food_picasso_order_from_telegram_order(
    telegramOrder: TelegramOrder, foodPicassoMenu: FoodPicassoMenu
) -> FoodPicassoOrder:
    id = f"{telegramOrder.id}_{str(uuid.uuid4())}_tl"
    picassoNameToPositionMapper = {p.name: p for p in foodPicassoMenu.products}

    deliveryTypeMapper = {TelegramDeliveryType.delivery: FoodPicassoOrderDeliveryType.courier,
                          TelegramDeliveryType.pickup: FoodPicassoOrderDeliveryType.pickup}

    address: Address = Address()
    if telegramOrder.deliveryType == TelegramDeliveryType.delivery:
        address = _parse_address(telegramOrder.address)

    order = FoodPicassoOrder(
        uid=id,
        erpId=2281,
        date=int(time.time()),
        client=FoodPicassoOrderClient(
            phone=telegramOrder.phone, name=telegramOrder.name
        ),
        deliveryType=deliveryTypeMapper[telegramOrder.deliveryType],
        address=address,
        discount=0,
        fee=telegramOrder.fee,
        dishes=[
            FoodPicassoOrderPosition(
                id=picassoNameToPositionMapper[p.name].id, count=p.quantity
            )
            for p in telegramOrder.positions
        ],
    )
    return order
