import openpyxl

from wallet.rest import Wallet
from wallet.web_client import Client

# login to tg in chrome driver if it needed
web_client = Client.auth(profile_name='main')
# web_client = Client('profile_name='main'')

token = web_client.get_token()

w = Wallet(auth_token=token)

offset = 0
limit = 200
i = 1
temp = []

history = w.get_user_p2p_order_history(offset)

if history['data']:
    for row in history['data']:

        # filter | Only COMPLETED orders
        if row['status'] != 'COMPLETED':
            continue

        temp.append(
            (
                i,
                row['number'],
                row['offerType'],
                row['buyer']['nickname'],
                row['seller']['nickname'],
                round(float(row['price']['value']), 2),
                round(float(row['volume']['amount']), 2),
                round(float(row['amount']['amount']), 2),
                row['paymentDetails']['paymentMethod']['name'],
                row['acceptDateTime'],
            )
        )
        i += 1
        offset += limit

wb = openpyxl.Workbook()
work_list = wb.active

work_list.append(
    ('№', 'OrderID', 'Type ', 'Buyer', 'Seller', 'Price',
     'Volume', "Sum", "Payment Method", "Order End Date")
)
for row in temp:
    try:
        work_list.append(row)
    except Exception as e:
        print(row)
        raise

wb.save('my_orders.xlsx')
