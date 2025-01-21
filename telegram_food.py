import base64
from dataclasses import dataclass
import enum
import urllib.parse

import urllib


class TelegramDeliveryType(enum.Enum):
    delivery = 1
    pickup = 2


@dataclass
class TelegramOrderPosition:
    name: str
    quantity: int


@dataclass
class TelegramOrder:
    id: str
    positions: list[TelegramOrderPosition]
    name: str
    phone: str
    address: str
    deliveryType: TelegramDeliveryType


def parse_telegram_order_from_base64_url(base64Url: str) -> TelegramOrder:
    decodedRequest = base64.b64decode(base64Url).decode('utf-8')
    parsedDict = urllib.parse.parse_qs(decodedRequest)
    return parse_telegram_order_from_url_dict(parsedDict)


def parse_telegram_order_from_url_dict(telegramUrlOrderDict: dict) -> TelegramOrder:
    maxPositions = 1000
    positions: list[TelegramOrderPosition] = []
    for i in range(maxPositions):
        key = f'data[basket][{i}]'
        if f'{key}[product_id]' not in telegramUrlOrderDict:
            break

        positions.append(TelegramOrderPosition(name=telegramUrlOrderDict[f'{key}[product_data][name]'][0],
                                               quantity=int(telegramUrlOrderDict[f'{key}[quantity]'][0])))

    return TelegramOrder(positions=positions,
                         name=telegramUrlOrderDict['data[client][name]'][0],
                         phone=telegramUrlOrderDict['data[client][phone]'][0],
                         id=str(telegramUrlOrderDict['data[id]']),
                         address=telegramUrlOrderDict.get(
                             'data[address][addres]', ['None'])[0],
                         deliveryType=TelegramDeliveryType[telegramUrlOrderDict['data[receipt][global]'][0]])
