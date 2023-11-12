import pprint
from dataclasses import dataclass, asdict


@dataclass
class Value:
    name: str
    value: str

    @staticmethod
    def from_dict(obj: dict) -> 'Value':
        _name = str(obj.get("name"))
        _value = str(obj.get("value"))
        return Value(_name, _value)


@dataclass
class Attributes:
    version: str
    values: list[Value]

    @staticmethod
    def from_dict(obj: dict) -> 'Attributes':
        _version = str(obj.get("version"))
        _values = [Value.from_dict(y) for y in obj.get("values")]
        return Attributes(_version, _values)


@dataclass
class AvailableVolume:
    currencyCode: str
    amount: float

    @staticmethod
    def from_dict(obj: dict) -> 'AvailableVolume':
        _currencyCode = str(obj.get("currencyCode"))
        _amount = float(obj.get("amount"))
        return AvailableVolume(_currencyCode, _amount)


@dataclass
class OrderAmountLimits:
    currencyCode: str
    min: float
    max: float
    approximate: bool

    @staticmethod
    def from_dict(obj: dict) -> 'OrderAmountLimits':
        _currencyCode = str(obj.get("currencyCode"))
        _min = float(obj.get("min"))
        _max = float(obj.get("max"))
        _approximate = obj.get('approximate')
        return OrderAmountLimits(_currencyCode, _min, _max, _approximate)


@dataclass
class OrderVolumeLimits:
    currencyCode: str
    min: float
    max: float
    approximate: bool

    @staticmethod
    def from_dict(obj: dict) -> 'OrderVolumeLimits':
        _currencyCode = str(obj.get("currencyCode"))
        _min = float(obj.get("min"))
        _max = float(obj.get("max"))
        _approximate = obj.get('approximate')
        return OrderVolumeLimits(_currencyCode, _min, _max, _approximate)


@dataclass
class PaymentMethod:
    code: str
    name: str
    originNameLocale: str
    nameEng: str

    @staticmethod
    def from_dict(obj: dict) -> 'PaymentMethod':
        _code = str(obj.get("code"))
        _name = str(obj.get("name"))
        _originNameLocale = str(obj.get("originNameLocale"))
        _nameEng = str(obj.get("nameEng"))
        return PaymentMethod(_code, _name, _originNameLocale, _nameEng)


@dataclass
class Price:
    type: str
    baseCurrencyCode: str
    quoteCurrencyCode: str
    value: float

    @staticmethod
    def from_dict(obj: dict) -> 'Price':
        _type = str(obj.get("type"))
        _baseCurrencyCode = str(obj.get("baseCurrencyCode"))
        _quoteCurrencyCode = str(obj.get("quoteCurrencyCode"))
        _value = float(obj.get("value"))
        return Price(_type, _baseCurrencyCode, _quoteCurrencyCode, _value)


@dataclass
class Statistics:
    userId: int
    totalOrdersCount: int
    successRate: str
    successPercent: int

    @staticmethod
    def from_dict(obj: dict) -> 'Statistics':
        _userId = int(obj.get("userId"))
        _totalOrdersCount = int(obj.get("totalOrdersCount"))
        _successRate = str(obj.get("successRate"))
        _successPercent = int(obj.get("successPercent"))
        return Statistics(_userId, _totalOrdersCount, _successRate, _successPercent)


@dataclass
class User:
    userId: int
    nickname: str
    avatarCode: str
    statistics: Statistics
    isVerified: bool

    @staticmethod
    def from_dict(obj: dict) -> 'User':
        _userId = int(obj.get("userId"))
        _nickname = str(obj.get("nickname"))
        _avatarCode = str(obj.get("avatarCode"))
        _statistics = Statistics.from_dict(obj.get("statistics"))
        _isVerified = obj.get('isVerified')
        return User(_userId, _nickname, _avatarCode, _statistics, _isVerified)


@dataclass
class PaymentDetails:
    id: int
    userId: int
    paymentMethod: PaymentMethod
    currency: str
    attributes: Attributes
    name: str

    @staticmethod
    def from_dict(obj: dict) -> 'PaymentDetails':
        _id = int(obj.get("id"))
        _userId = int(obj.get("userId"))
        _paymentMethod = PaymentMethod.from_dict(obj.get("paymentMethod"))
        _currency = str(obj.get("currency"))
        _attributes = Attributes.from_dict(obj.get("attributes"))
        _name = str(obj.get("name"))
        return PaymentDetails(_id, _userId, _paymentMethod, _currency, _attributes, _name)


@dataclass
class Offer:
    id: int
    number: str
    user: User
    type: str
    price: Price
    availableVolume: float
    orderAmountLimits: OrderAmountLimits
    orderVolumeLimits: OrderVolumeLimits
    paymentMethods: list[PaymentMethod]
    paymentDetails: list[PaymentDetails]
    profit_percent: float = None

    @staticmethod
    def from_dict(obj: dict) -> 'Offer':
        _id = int(obj.get("id"))
        _number = str(obj.get("number"))
        _user = User.from_dict(obj.get("user"))
        _type = str(obj.get("type"))
        _price = Price.from_dict(obj.get("price"))
        _availableVolume = float(obj.get("availableVolume"))
        _orderAmountLimits = OrderAmountLimits.from_dict(obj.get("orderAmountLimits"))
        _orderVolumeLimits = OrderVolumeLimits.from_dict(obj.get("orderVolumeLimits"))

        _paymentMethods = []
        _paymentDetails = []

        if obj.get('paymentDetails'):
            _paymentDetails = [PaymentDetails.from_dict(y) for y in obj.get("paymentDetails")]
        if obj.get('paymentMethods'):
            _paymentMethods = [PaymentMethod.from_dict(y) for y in obj.get("paymentMethods")]

        return Offer(_id, _number, _user, _type, _price, _availableVolume, _orderAmountLimits, _orderVolumeLimits,
                     _paymentMethods, _paymentDetails)

    def to_dict(self):
        return {k: v for k, v in asdict(self).items()}

@dataclass
class OwnOffer:
    id: int
    number: str
    status: str
    type: str
    price: Price
    availableVolume: AvailableVolume
    orderAmountLimits: OrderAmountLimits
    orderVolumeLimits: OrderVolumeLimits
    paymentMethods: list[PaymentMethod]
    paymentDetails: list[PaymentDetails]

    @staticmethod
    def from_dict(obj: dict) -> 'OwnOffer':
        _id = int(obj.get("id"))
        _number = str(obj.get("number"))
        _status = str(obj.get("status"))
        _type = str(obj.get("type"))
        _price = Price.from_dict(obj.get("price"))
        _availableVolume = AvailableVolume.from_dict(obj.get("availableVolume"))
        _orderAmountLimits = OrderAmountLimits.from_dict(obj.get("orderAmountLimits"))
        _orderVolumeLimits = OrderVolumeLimits.from_dict(obj.get("orderVolumeLimits"))

        _paymentMethods = []
        _paymentDetails = []

        if obj.get('paymentDetails'):
            _paymentDetails = [PaymentDetails.from_dict(y) for y in obj.get("paymentDetails")]
        if obj.get('paymentMethods'):
            _paymentMethods = [PaymentMethod.from_dict(y) for y in obj.get("paymentMethods")]

        return OwnOffer(_id, _number, _status, _type, _price, _availableVolume, _orderAmountLimits, _orderVolumeLimits,
                        _paymentMethods, _paymentMethods)

    def to_dict(self):
        return {k: v for k, v in asdict(self).items()}


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
            user_stats: Statistics,
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
