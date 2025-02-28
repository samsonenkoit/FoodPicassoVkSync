from dataclasses import dataclass
import enum
import json
import time
import uuid
import requests


@dataclass
class FoodPicassoOrderClient:
    phone: str
    name: str


@dataclass
class FoodPicassoOrderPosition:
    id: str
    count: int


class FoodPicassoOrderDeliveryType(enum.Enum):
    courier = 1
    pickup = 2


@dataclass
class Address:
    country: str = ''
    city: str = ''
    house: str = ''
    street: str = ''
    entrance: str = ''
    floor: str = ''
    apartment: str = ''


@dataclass
class FoodPicassoOrder:
    uid: str
    erpId: int
    date: int
    client: FoodPicassoOrderClient
    discount: int
    dishes: list[FoodPicassoOrderPosition]
    address: Address
    deliveryType: FoodPicassoOrderDeliveryType
    fee: float


@dataclass
class FoodPicassoMenuProduct:
    id: str
    name: str
    price: int
    description: str


@dataclass
class FoodPicassoMenu:
    products: list[FoodPicassoMenuProduct]


# https://docs.google.com/document/d/1kgIDiM0EK-W9Vmg7C_mNe9Rfu9QNZHeUQ1OPMn_C4sQ/edit?tab=t.0#heading=h.6n0elmg7bdbs


class PicassoClient:
    def __init__(self, url: str, companyId: int, token: str) -> None:
        self.companyId = companyId
        self.token = token
        self.url = url

    def add_order(self, order: FoodPicassoOrder) -> dict:
        body = {
            "order": {
                "erpId": order.erpId,
                "orderUid": order.uid,
                "date": order.date,
                "client": {"phone": order.client.phone, "name": order.client.name},
                "address": {
                    "city": order.address.city,
                    "street": order.address.street,
                    "house": order.address.house,
                    "apartment": order.address.apartment,
                    "entrance": order.address.entrance,
                    "floor": order.address.floor,
                },
                "deliveryMethod": order.deliveryType.name,
                "paymentType": 'cash',
                "dishes": [
                    {"id": position.id, "count": position.count}
                    for position in order.dishes
                ],
                "fee": order.fee,
                "discount": order.discount,
            }
        }
        additionalPayloadParams = {"id": str(uuid.uuid4())}
        return self._post(
            "CreateOrder", body=body, additionalPayloadParams=additionalPayloadParams
        )

    def load_menu(self, menuNumber: int) -> FoodPicassoMenu:
        body = {"menu": menuNumber}
        additionalPayloadParams = {"id": str(uuid.uuid4())}
        response = self._post(
            methodName="GetMenu",
            body=body,
            additionalPayloadParams=additionalPayloadParams,
        )
        products = [
            FoodPicassoMenuProduct(
                id=p["id"],
                name=p["name"],
                price=p["price"],
                description=p["description"],
            )
            for p in response["result"]["products"]
        ]
        return FoodPicassoMenu(products=products)

    def _post(self, methodName: str, body={}, additionalPayloadParams={}) -> dict:
        headers = {"Content-Type": "application/json"}
        requestBody = {"token": self.token, "company": self.companyId}
        requestBody.update(body)
        payload = {
            "jsonrpc": "2.0",
            "method": methodName,
            "params": requestBody,
        }
        payload.update(additionalPayloadParams)

        response = requests.post(
            self.url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            result = response.json()
            if 'error' in result:
                raise Exception(result)

            return result
        else:
            raise Exception(
                f"Request to picasso status {response.status_code}")
