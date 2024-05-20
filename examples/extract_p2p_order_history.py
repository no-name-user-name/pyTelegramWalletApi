import time

import openpyxl

from wallet.rest import Wallet
from wallet.types import Order
# from wallet.web_client import Client

# web_client = Client(profile='main')
# auth_token = web_client.get_token()

w = Wallet.token_from_file('../token.txt')

offset = 0
limit = 200
i = 1
history: list[Order] = []
temp = []

history += w.get_own_p2p_order_history(offset, limit, status='ALL_COMPLETED')

while len(history) / i == limit:
    time.sleep(1)

    i += 1
    offset += limit
    history += w.get_own_p2p_order_history(offset, limit, status='ALL_COMPLETED')
    print(len(history))
    break

for order in history:
    temp.append(
        (
            i,
            order.number,
            order.offerType,
            order.buyer.nickname,
            order.seller.nickname,
            round(order.price.value, 2),
            round(order.volume.amount, 2),
            round(order.amount.amount, 2),
            order.paymentDetails.paymentMethod.name,
            order.acceptDateTime,
        )
    )

wb = openpyxl.Workbook()
work_list = wb.active

work_list.append(
    ('№', 'OrderID', 'Type ', 'Buyer', 'Seller', 'Price',
     'Volume', "Sum", "Payment Method", "Order End Date")
)

for row in temp:
    work_list.append(row)

wb.save('my_orders.xlsx')
