<br/>
<p align="center">
  <a href="https://github.com/no-name-user-name/pyTelegramWalletApi">
    <img src="https://wallet.tg/icon.svg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Telegram Wallet API</h3>

  <p align="center">
    Unofficial library for managing your personal Wallet account
    <br/>
    <br/>
  </p>
</p>



## Table Of Contents

* [About the Project](#about-the-project)
* [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Example](#example)
* [Realised methods](#realised-methods)

## About The Project

Send and receive tokens | Trade on P2P Market

## Built With

To obtain an authorization token, the "selenium" library is used.
Working with the API is implemented using "requests"

## Getting Started

```bazaar
pip install pyTelegramWalletApi
```

### Send by address

```python
from wallet import Wallet, Client

# use chromedriver to loging tg and parse auth_token
c = Client(profile='main', headless=True)
auth_token = c.get_token()

w = Wallet(auth_token)
balance = w.get_user_balances('USDT')
print(f'[*] Balance: {balance.available_balance} TON')

w.send_to_address(balance.available_balance, 'USDT', 'UQC_tRAxYGgMuU4sSqN6eRWArwvL4qI3gXn_', network='ton')
```

### Send by username
```python
from wallet import Client, Wallet

c = Client(profile='main', headless=True)

# To send coins within a telegram, you need to receive an “auth_token”
# from Wallet directly in chat with the recipient

auth_token = c.get_token(username='username_to_recieve')
print(c.receiver_id)  # browser parse tg_id by username

w = Wallet(auth_token, log_response=True)
w.send_to_user(amount=1, currency='USDT', receiver_tg_id=c.receiver_id)
```

### Parse P2P market

```python
import time
from wallet import Wallet

w = Wallet.token_from_file('token.txt')  # load token from file method

while True:
    try:
        o = w.get_p2p_market('TON', 'RUB', 'SALE', desired_amount=5000)[0]

        print(f'Top offer ID: {o.id}\n'
              f'Price: {o.price.value} {o.price.quoteCurrencyCode}\n'
              f'Volume: {o.availableVolume} TON\n'
              f'User: {o.user.nickname} | Orders: {o.user.statistics.totalOrdersCount}\n'
              f'=============================')
        """
        Top offer ID: 187885
        Price: 590.0 RUB
        Volume: 30.682475494 TON
        User: Lucky Goose | Orders: 3127
        =============================
        """
        
    except Exception as e:
        print(f"[!] Error: {e}")

    time.sleep(5)

```

### Create own offers

```python
from wallet import Wallet

w = Wallet.token_from_file('token.txt')  # load token from file method
 
new_offer = w.create_p2p_offer(
    comment='Hello',
    currency='TON',
    fiat='RUB',
    amount=10,
    margine=90,
    offer_type='PURCHASE',
    order_min_price=500,
    pay_methods=['tinkoff'],
)

w.activate_p2p_offer(new_offer.id, new_offer.type)
```

## Wallet realised methods

### Account methods

```
get_user_balances(currency)
```
```
get_transactions(limit, last_id, crypto_currency, transaction_type, transaction_gateway)
```
```
get_wallet(crypto_currency)
```
```
get_exchange_pair_info(from_currency, to_currency, from_amount)
```
```
get_earn_campings()
```
```
test_get_transaction_details(tx_id)
```
```
get_user_region_verification()
```
```
send_to_address(amount, currency, address, network)
```
```
send_to_user(amount, currency, receiver_tg_id)
```
```
create_exchange(from_currency, to_currency, from_amount, local_currency)
```

### P2P matket methods


```
get_own_p2p_user_info()
```
```
get_user_p2p_payments()
```
```
get_own_p2p_order_history(offset, limit, status)
```
```
get_p2p_order(order_id)
```
```
get_p2p_rate(base, quote)
```
```
get_p2p_payment_methods_by_currency(currency)
```
```
create_p2p_offer(currency, amount, fiat, margine, offer_type,
                 order_min_price, pay_methods, comment, price_type,
                 confirm_timeout_tag:)
```
```
edit_p2p_offer(currency, offer_id, margine, volume, order_amount_min, comment)
```
```
activate_p2p_offer(offer_id, offer_type)
```
```
deactivate_p2p_offer(offer_id, offer_type)
```
```
enable_p2p_bidding()
```
```
disable_p2p_bidding()
```
```
get_own_p2p_offers(offset limit, offer_type, status)
```
```
get_p2p_offer(offer_id)
```
```
get_own_p2p_offer(offer_id)
```
```
accept_p2p_order(order_id, offer_type)
```
```
get_p2p_market(base_currency_code, quote_currency_code, offer_type, offset, limit,desired_amount)
```

