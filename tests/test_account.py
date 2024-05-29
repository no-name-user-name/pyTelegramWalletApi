from tests.utils import check_api_update
from wallet import Wallet

w = Wallet.token_from_file('../token.txt')


def test_get_earn_campings():
    assert 'campaigns' in w.get_earn_campings()


def test_get_user_balance():
    check_api_update(
        w.get_user_balances(currency='TON')
    )


def test_get_transactions():
    txs = w.get_transactions()
    assert len(txs) > 0


def test_get_transaction_details():
    check_api_update(
        w.get_transaction_details(tx_id=49159406)
    )


def test_get_passcode_info():
    assert 'recoveryEmail' in w.get_passcode_info()


def test_get_recovery_email():
    assert 'email' in w.get_recovery_email('wallet')


def test_get_wallet():
    assert 'address' in w.get_wallet(crypto_currency='NOT')[0]


def test_exchange_pair_info():
    assert 'rate' in w.get_exchange_pair_info('TON', 'USDT')
