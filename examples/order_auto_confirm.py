import time

from wallet import Wallet
# from wallet.web_client import Client

if __name__ == '__main__':
    # c = Client(profile='main', headless=True)
    # auth_token = c.get_token()
    # w = Wallet(auth_token)

    w = Wallet.token_from_file('token.txt')

    while True:
        w.update_token()
        active_orders = w.get_own_p2p_order_history(status='ALL_ACTIVE')
        print(f"Available: {len(active_orders)}")

        for order in active_orders:
            if order.status == 'NEW':
                o = w.accept_p2p_order(order_id=order.id, offer_type=order.offerType)

                if o.offerType == 'PURCHASE':
                    s_orders = o.seller.statistics.totalOrdersCount
                    s_rate = o.seller.statistics.successRate
                    if o.seller.isVerified:
                        verif = ' ✅'
                    else:
                        verif = ''

                    print(f'[*] Order accept! '
                          f'    Seller: {o.seller.nickname}{verif} | ID: {o.seller.userId}'
                          f"    Stats: {s_orders} orders | Success {s_rate}%")

                    print('[*] Payment Details:')

                    for m in o.paymentDetails.attributes.values:
                        print(f"    {m.name} | {m.value}")

        time.sleep(10)
