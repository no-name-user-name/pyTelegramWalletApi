class PaymentMethods:
    def __init__(self, data):
        self.code = data['code']
        self.name = data['name']
        self.origin_name_locale = data['originNameLocale']
        self.name_eng = data['nameEng']


class AttrValues:
    def __init__(self, data):
        self.name = data['name']
        self.value = data['value']


class Attributes:
    def __init__(self, data):
        self.version = data['version']
        self.values = [AttrValues(value) for value in data['values']]


class PaymentDetails:
    def __init__(self, data):

        self.id = data['id']
        self.userId = data['userId']
        self.currency = data['currency']
        self.attributes = Attributes(data['attributes'])
        self.name = data['name']

        if type(data['paymentMethod']) == dict:
            self.payment_method = PaymentMethods(data['paymentMethod'])
        else:
            self.payment_method = [PaymentMethods(method) for method in data['paymentMethod']]


class UserStatistic:
    def __init__(self, data):
        self.success_percent = data['successPercent']
        self.success_rate = data['successRate']
        self.total_orders_count = data['totalOrdersCount']
        self.user_id = data['userId']


class User:
    def __init__(self, data):
        self.avatar_code = data['avatarCode']
        self.nickname = data['nickname']
        self.userId = data['userId']
        self.statistics = UserStatistic(data['statistics'])


class Offer:
    def __init__(self, data: dict, rate=None):

        self.id = int(data['id'])
        self.number = data['number']

        if 'status' in data:
            self.status = data['status']

        self.type = data['type']

        self.available_volume = data['availableVolume']
        if 'amount' in data['availableVolume']:
            self.available_volume = data['availableVolume']['amount']

        self.available_volume = float(self.available_volume)

        self.base_currency_code = data['price']['baseCurrencyCode']
        self.quote_currency_code = data['price']['quoteCurrencyCode']

        self.price_type = data['price']['type']

        if self.price_type == 'FIXED':
            self.price = float(data['price']['value'])

            if rate is None:
                self.profit_percent = None
            else:
                self.profit_percent = round(100 + (self.price - rate) / rate * 100, 4)
        else:
            self.price = float(data['price']['estimated'])
            self.profit_percent = round(float(data['price']['value']))

        self.min_order_amount = float(data['orderAmountLimits']['min'])
        self.max_order_amount = float(data['orderAmountLimits']['max'])

        self.max_order_volume = float(data['orderVolumeLimits']['max'])
        self.max_order_volume = float(data['orderVolumeLimits']['max'])

        if 'paymentDetails' in data:
            self.payment_details = [PaymentDetails(pd) for pd in data['paymentDetails']]
        elif 'paymentMethods' in data:
            self.payment_method = [PaymentMethods(method) for method in data['paymentMethods']]

        if 'user' in data:
            self.user = User(data['user'])


class ActionTypes:
    price_change = 'price_change'
    offer_delete = 'offer_delete'
    offer_add = 'offer_add'
    volume_change = 'volume_change'


class Action:
    def __init__(
            self,
            action_type: ActionTypes,
            order_id: int,
            offer_type: str,
            user_stats: UserStatistic,
            old_price=None,
            new_price=None,
            old_volume=None,
            new_volume=None,

    ):
        self.old_price = None
        self.new_price = None
        self.order_id = order_id
        self.user_stats = user_stats
        self.offer_type = offer_type

        if action_type == ActionTypes.price_change:
            self.old_price = old_price
            self.new_price = new_price

        elif action_type == ActionTypes.volume_change:
            self.old_volume = old_volume
            self.new_volume = new_volume

        elif action_type == ActionTypes.offer_add:
            pass

        elif action_type == ActionTypes.offer_delete:
            pass
