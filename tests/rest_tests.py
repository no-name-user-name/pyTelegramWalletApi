from wallet.rest import Wallet
from wallet.types import Offer, OwnOffer

AUTH_TOKEN = ''
ADDRESS = ''

w = Wallet(AUTH_TOKEN)


def test_get_own_p2p_offer():
    offers = w.get_own_p2p_offers()
    assert isinstance(offers[0], OwnOffer)
    # offer = w.get_own_p2p_offer(offer_id=offers[0].id)
    # offer = w.get_own_p2p_offer(tag=offers[0].number)
    # assert isinstance(offer, OwnOffer | [])


def test_get_user_balance():
    balance = w.get_user_balance()
    assert 'available_balance' in balance


def test_get_p2p_market():
    market = w.get_p2p_market('TON', 'RUB')
    assert isinstance(market[0], Offer)


def test_get_user_payment():
    up = w.get_user_p2p_payment()
    assert 'data' in up


def test_get_user_p2p_order_history():
    uoh = w.get_user_p2p_order_history()
    assert 'data' in uoh


def test_get_p2p_payment_methods_by_currency():
    result = w.get_p2p_payment_methods_by_currency()
    assert 'data' in result


def test_get_transactions():
    txs = w.get_transactions(limit=20)
    assert 'transactions' in txs


def test_get_transaction_detail():
    tx_id = 0
    tx = w.get_transaction_details(tx_id)
    assert 'status' in tx


def test_withdrawals_validate_amount():
    v = w.withdrawals_validate_amount(amount=0.01, currency='TON', address=ADDRESS)
    assert 'status' in v


def test_send_to_address():
    r = w.send_to_address(amount=0.01, currency='TON', address=ADDRESS)
    assert 'transaction_id' in r
