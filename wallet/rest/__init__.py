import time
import requests

from wallet.types import Offer


class Wallet:
    def __init__(self, auth_token: str):
        self.auth_token = auth_token
        self.session = requests.Session()
        self.session.headers = {
            'content-type': 'application/json',
        }
        self.endpoint = 'https://walletbot.me'

        if auth_token == '' or len(auth_token) < 30:
            raise Exception('[!] Bad auth token!')

    def request(self, method, path, json_data=None, params=None, max_attempts=3, delay=2):
        if 'p2p/public-api' in path:
            self.session.headers['authorization'] = 'Bearer ' + self.auth_token
        else:
            self.session.headers['authorization'] = self.auth_token

        counter = 0
        while counter < max_attempts:
            counter += 1
            try:
                response = self.session.request(method, self.endpoint + path, json=json_data, params=params)
                status_code = response.status_code

                if status_code == 200:
                    return response.json()

                elif status_code == 401 or status_code == 400:
                    raise Exception('[*] Wrong Auth token')

                elif status_code == 429:
                    raise Exception('[*] You are Rate Limited')

            except Exception as e:
                print(f'[!] Request error: {e}. Try attemp #{counter}')
                time.sleep(delay)

    def get_user_balance(self, currency='TON') -> dict:
        return self.request('GET', f'/api/v1/accounts/{currency}/')

    def get_user_p2p_payment(self):
        return self.request('POST', '/p2p/public-api/v2/payment-details/get/by-user-id')

    def get_user_p2p_order_history(self, offset=0, limit=200):
        json_data = {
            "offset": offset,
            "limit": limit
        }
        return self.request('POST', '/p2p/public-api/v2/offer/order/get-history/by-user-id', json_data)

    def get_own_p2p_offer(
            self,
            tag: str = None,
            offer_id: int = None,
            offer_type=None,
            status: str = 'ACTIVE'
    ) -> Offer:
        """
        :param offer_type:  PURCHASE | SALE
        :param offer_id:
        :param tag: example 'AS-00057073'
        :param status: None | ACTIVE | INACTIVE
        :return: Offer
        """
        offers = self.get_own_p2p_offers(status=status)

        if tag is not None:
            return [o for o in offers if o.number == tag][0]

        elif offer_id is not None:
            return [o for o in offers if o.id == offer_id][0]

        elif offer_type is not None:
            return [o for o in offers if o.type == offer_type][0]

        else:
            return offers[0]

    def get_own_p2p_offers(self, order_type: str = None, status: str = 'ACTIVE') -> list[Offer]:
        """
        :param status: None | ACTIVE | INACTIVE
        :param order_type: None | PURCHASE | SALE
        :return:
        """
        result = self.request('POST', '/p2p/public-api/v2/offer/user-own/list')

        offers = [Offer(data) for data in result['data']]

        if order_type is not None:
            offers = [offer for offer in offers if offer.type == order_type]

        if status is not None:
            offers = [offer for offer in offers if offer.status == status]

        return offers

    def disable_p2p_bidding(self):
        return self.request('POST', '/p2p/public-api/v2/user-settings/disable-bidding')

    def enable_p2p_bidding(self):
        return self.request('POST', '/p2p/public-api/v2/user-settings/enable-bidding')

    def create_p2p_offer(
            self,
            currency: str,
            amount: int,
            fiat: str,
            margine: int,
            offer_type: str,
            order_min_price: int,
            pay_methods: list,
            comment: str = None,
            price_type: str = "FLOATING"
    ):
        """

        :param pay_methods:
        :param comment:
        :param order_min_price:
        :param margine:
        :param fiat: RUB | KZT etc...
        :param price_type: FLOATING | FIXED
        :param amount:
        :param currency: TON | BTC
        :param offer_type:  SALE | PURCHASE
        :return:
        """

        if offer_type == 'PURCHASE':
            json_data = {
                "type": offer_type,
                "initVolume": {
                    "currencyCode": currency,
                    "amount": str(amount)
                },
                "price": {
                    "type": price_type,
                    "baseCurrencyCode": currency,
                    "quoteCurrencyCode": fiat,
                    "value": margine
                },
                "orderAmountLimits": {
                    "min": order_min_price
                },
                "paymentConfirmTimeout": "PT15M",
                "comment": comment,
                "paymentMethodCodes": pay_methods
            }
        else:
            json_data = {
                "type": offer_type,
                "initVolume": {
                    "currencyCode": currency,
                    "amount": str(amount)
                },
                "price": {
                    "type": price_type,
                    "baseCurrencyCode": currency,
                    "quoteCurrencyCode": fiat,
                    "value": margine
                },
                "orderAmountLimits": {
                    "min": order_min_price
                },
                "paymentConfirmTimeout": "PT15M",
                "comment": comment,
                "paymentDetailsIds": pay_methods
            }

        return self.request('POST', '/p2p/public-api/v2/offer/create', json_data)

    def clone_p2p_offer(self, offer_id, amount=None):
        o = self.get_own_p2p_offer_by_id(offer_id)

        if amount is None:
            amount = o['data']['availableVolume']['amount']
        else:
            amount = round(amount, 9)

        if o['data']['type'] == 'SALE':
            pd = [p['id'] for p in o['data']['paymentDetails']]
        else:
            pd = [m['code'] for m in o['data']['paymentMethods']]

        return self.create_p2p_offer(
            currency=o['data']['price']['baseCurrencyCode'],
            amount=amount,
            fiat=o['data']['price']['quoteCurrencyCode'],
            margine=o['data']['price']['value'],
            offer_type=o['data']['type'],
            order_min_price=o['data']['orderAmountLimits']['min'],
            pay_methods=pd,
            comment=o['data']['comment'],
            price_type=o['data']['price']['type']
        )

    def replace_p2p_offer(self, offer_id, order_type, amount=None):
        new_offer = self.clone_p2p_offer(offer_id, amount)
        self.p2p_offer_deactivate(offer_id, order_type)
        self.p2p_offer_activate(offer_id=new_offer['data']['id'], offer_type=new_offer['data']['type'])
        return new_offer

    def edit_p2p_offer(
            self,
            offer_id: int,
            value: float,
            order_amount_min: float = None,
    ):
        """

        :param order_amount_min:
        :param value:
        :param offer_id:
        :return:
        """

        od = self.get_own_p2p_offer_by_id(offer_id)['data']

        if order_amount_min is None:
            order_amount_min = float(od['orderAmountLimits']['min'])

        if od['type'] == 'PURCHASE':
            json_data = {
                "offerId": offer_id,
                "paymentConfirmTimeout": "PT15M",
                "type": od['type'],
                "price": {
                    "type": od['price']['type'],
                    "value": str(round(value, 4))
                },
                "orderAmountLimits": {
                    "min": str(round(order_amount_min, 2))
                },
                "comment": od['comment'],
                "paymentMethodCodes": [
                    p['code'] for p in od['paymentMethods']
                ]
            }
        else:

            json_data = {
                "offerId": offer_id,
                "paymentConfirmTimeout": "PT15M",
                "type": od['type'],
                "price": {
                    "type": od['price']['type'],
                    "value": str(round(value, 2))
                },
                "orderAmountLimits": {
                    "min": str(round(order_amount_min, 2))
                },
                "comment": od['comment'],
                "paymentDetailsIds": [p['id'] for p in od['paymentDetails']]
            }

        return self.request('POST', '/p2p/public-api/v2/offer/edit', json_data)

    def get_own_p2p_offer_by_id(self, offer_id: int):
        json_data = {
            "offerId": offer_id
        }
        return self.request('POST', '/p2p/public-api/v2/offer/get-user-own', json_data)

    def p2p_offer_activate(self, offer_id, offer_type):
        json_data = {
            "type": offer_type,
            "offerId": offer_id
        }
        return self.request('POST', '/p2p/public-api/v2/offer/activate', json_data)

    def p2p_offer_deactivate(self, offer_id, offer_type):
        json_data = {
            "type": offer_type,
            "offerId": offer_id
        }
        return self.request('POST', '/p2p/public-api/v2/offer/deactivate', json_data)

    def get_p2p_payment_methods_by_currency(self, currency='RUB'):
        json_data = {
            "currencyCode": currency
        }
        return self.request('POST', '/p2p/public-api/v2/payment-details/get-methods/by-currency-code', json_data)

    def get_rate(self, base='TON', quote='RUB'):
        result = self.request('GET', f'/rates/public-api/v1/rate/crypto-to-fiat?base={base}&quote={quote}')
        return float(result['data']['rate'])

    def get_p2p_market(
            self,
            base_currency_code,
            quote_currency_code,
            offer_type='SALE',
            offset=0, limit=100,
            rate=None,
            desired_amount=None
    ) -> list[Offer]:
        """

        :param desired_amount:
        :param rate:
        :param base_currency_code: TON | BTC
        :param quote_currency_code: RUB | KZT etc.
        :param offer_type: SALE | PURCHASE
        :param offset:
        :param limit:
        :return:
        """
        json_data = {
            "baseCurrencyCode": base_currency_code,
            "quoteCurrencyCode": quote_currency_code,
            "offerType": offer_type,
            "offset": offset,
            "limit": limit,
            "desiredAmount": desired_amount
        }
        market = self.request('POST', '/p2p/public-api/v2/offer/depth-of-market', json_data)
        return [Offer(data, rate) for data in market['data']]

    def get_p2p_offer(self, offer_id: int):
        json_data = {
            "offerId": offer_id
        }
        return self.request('POST', '/p2p/public-api/v2/offer/get', json_data)

    def update_p2p_offer_value(self, offer_id, add_amount=None):
        o = self.get_own_p2p_offer(offer_id=offer_id)

        if o.type == 'SALE':
            self.p2p_offer_deactivate(o.id, o.type)
            amount = self.get_user_balance('TON')['available_balance']
        else:
            amount = o.available_volume + add_amount + add_amount * 0.9 / 100

        r = self.replace_p2p_offer(o.id, o.type, amount)
        return Offer(r['data'])

    def get_transactions(self, limit=10, last_id=None) -> dict:

        if last_id is not None:
            return self.request('GET', f'/api/v1/transactions/?limit={limit}&last_id={last_id}')
        else:
            return self.request('GET', f'/api/v1/transactions/?limit={limit}')

    def get_transaction_details(self, tx_id) -> dict:
        return self.request('GET', f'/api/v1/transactions/details/{tx_id}/')

    # not realized
    # def send_to_user(self, amount, currency, receiver_tg_id):
    #     v = self.withdrawals_validate_amount(amount, currency, receiver_tg_id)
    #
    #     if v['status'] == 'ok':
    #
    #         json_data = {
    #             'amount': amount,
    #             'currency': currency
    #         }
    #         return self.request('POST', f'/api/v1/transfers/create_transfer_request/', json_data=json_data)
    #
    #     else:
    #         raise Exception(f'[!] Error withdrawals_validate_amount: {v}')

    def send_to_address(self, amount, currency, address):
        """

        :param amount:
        :param currency:
        :param address:
        :return: dict {'transaction_id': 000000}
        """
        validate = self.withdrawals_validate_amount(amount, currency, address=address)
        if validate['status'] == 'OK':
            withdraw_request = self._create_withdraw_request(amount, currency, address)
            return self._process_withdraw_request(withdraw_request['uid'])
        else:
            raise Exception(f'[!] Bad validate status: {validate}')

    def _process_withdraw_request(self, uid):
        return self.request('POST', f'/api/v1/withdrawals/process_withdraw_request/{uid}/')

    def withdrawals_validate_amount(
            self,
            amount: float,
            currency: str,
            receiver_tg_id: int = None,
            address: str = None
    ):
        params = {
            'amount': amount,
            'currency': currency,
            'receiver_tg_id': receiver_tg_id,
            'address': address
        }
        return self.request('GET', f'/api/v1/withdrawals/validate_amount/', params=params)

    def _create_withdraw_request(self, amount: float, currency: str, address: str):
        params = {
            'amount': str(amount),
            'currency': currency,
            'max_value': 'false',
            'address': address,
        }
        return self.request('POST', '/api/v1/withdrawals/create_withdraw_request/', params=params)

    def process_transfer(self, tx_id: str):
        return self.request('POST', f'/api/v1/transfers/process_transfer/{tx_id}/')
