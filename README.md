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

### Example

```python
import time

from wallet import Client, Wallet

# for the first tg login
c = Client.auth(profile='main')

# chromedriver headless mode for authorized tg account
# c = Client(profile='main')

# get wallet auth token
auth_token = c.get_token()

w = Wallet(auth_token)

ton_balance = w.get_user_balance('TON')['available_balance']
print(f'[*] Balance: {ton_balance} TON')

tx_id = w.send_to_address(0.01, 'TON', 'EQA5IHeHWX9BkTsI71ECzuD-HeYL-br36UmFoTWZFihU3fLz')['transaction_id']

tx_link = None
status = ''

# wait tx in block
while tx_link is None:
    details = w.get_transaction_details(tx_id)
    tx_link = details["transaction_link"]
    status = details['status']
    time.sleep(2)

print(f'[*] Tx status: {status} | {tx_link}')

""" Logs
[*] Starting parse wallet authorization token...
[*] Token find: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpX....
[*] Balance: 100 TON
[*] Tx status: success | https://tonscan.org/tx/....
"""
```


## Realised methods

Wallet Account Methods:
- send_to_address()
- get_user_balance()
- get_transaction_details()
- get_transactions()
- get_rate()


Wallet P2P Methods:
- get_p2p_market()
- create_p2p_offer()
- edit_p2p_offer()
- get_p2p_offer()
- get_own_p2p_offer_by_id()
- get_user_p2p_payment()
- get_user_p2p_order_history()
- get_own_p2p_offer()
- get_own_p2p_offers()
- enable_p2p_bidding()
- disable_p2p_bidding()
- p2p_offer_activate()
- p2p_offer_deactivate()
