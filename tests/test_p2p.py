from tests.utils import check_api_update
from wallet.rest import Wallet

w = Wallet.token_from_file('../token.txt')


def test_get_own_info():
    assert 'nickname' in w.get_own_p2p_user_info()


def test_get_own_permissions():
    print(w.get_own_p2p_permissions())


def test_get_user_p2p_payment():
    assert 'name' in w.get_user_p2p_payments()[0]


def test_get_own_p2p_order_history():
    orders = w.get_own_p2p_order_history(status='COMPLETED_FOR_REQUESTER')
    for o in orders:
        check_api_update(o)


def test_get_p2p_order():
    o = w.get_own_p2p_order_history(status='CANCELLED_OR_CANCELLING')[0]
    check_api_update(
        w.get_p2p_order(order_id=o.id)
    )


def test_get_p2p_rate():
    assert 'rate' in w.get_p2p_rate()


def test_get_p2p_payment_methods_by_currency():
    assert 'name' in w.get_p2p_payment_methods_by_currency()[0]


def test_create_p2p_order_SALE():
    pid = w.get_user_p2p_payments()[0]['id']

    new_offer = w.create_p2p_offer(
        comment='',
        currency='USDT',
        fiat='RUB',
        amount=10,
        margine=120,
        offer_type='SALE',
        order_min_price=500,
        order_max_price=1000,
        pay_methods=[pid],
        order_rounding_required=True,
    )
    check_api_update(new_offer)
    w.activate_p2p_offer(new_offer.id, new_offer.type)


def test_create_p2p_order_PURCHASE():
    new_offer = w.create_p2p_offer(
        comment='',
        currency='USDT',
        fiat='RUB',
        amount=10,
        margine=90,
        offer_type='PURCHASE',
        order_min_price=500,
        pay_methods=['tinkoff'],
    )
    check_api_update(new_offer)
    w.activate_p2p_offer(new_offer.id, new_offer.type)


def test_enable_p2p_bidding():
    assert w.enable_p2p_bidding()


def test_disable_p2p_bidding():
    assert w.disable_p2p_bidding()


def test_edit_p2p_offer():
    offer = w.get_own_p2p_offers()[0]
    check_api_update(
        w.edit_p2p_offer(offer.id, volume=11, comment='Test')
    )


def test_get_own_p2p_offers():
    check_api_update(
        w.get_own_p2p_offers()[0]
    )


def test_get_own_p2p_offer():
    o = w.get_own_p2p_offers()[0]
    check_api_update(
        w.get_own_p2p_offer(o.id)
    )


def test_get_p2p_offer():
    o = w.get_own_p2p_offers()[0]
    check_api_update(
        w.get_p2p_offer(o.id)
    )


def test_accept_p2p_order():
    o = w.get_own_p2p_order_history(status='ALL_ACTIVE')[0]
    check_api_update(
        w.accept_p2p_order(o.id, o.offerType)
    )


def test_get_p2p_market():
    check_api_update(
        w.get_p2p_market('TON', 'RUB', 'SALE')[0]
    )


def test_get_p2p_market_verified():
    check_api_update(
        w.get_p2p_market('TON', 'RUB', 'SALE', merchant_verified="VERIFIED")[0]
    )


def test_send_to_address():
    assert 'transaction_id' in w.send_to_address(amount=5, currency='TON', address='address')
