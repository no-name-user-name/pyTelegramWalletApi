import pprint
from dataclasses import dataclass, asdict
from typing import Literal

from dataclasses_json import dataclass_json, Undefined, CatchAll


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class Value:
    name: str
    value: str
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class Attributes:
    version: str
    values: list[Value]
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class AvailableVolume:
    currencyCode: str
    amount: float
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class AmountLimits:
    currencyCode: str
    min: float
    max: float
    approximate: bool
    makerDefinedMax: str | None = None
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class OrderVolumeLimits:
    currencyCode: str
    min: float
    max: float
    approximate: bool
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class PaymentMethod:
    code: str
    name: str
    originNameLocale: str
    nameEng: str
    unknown_things: CatchAll = None

    @staticmethod
    def to_dict():
        pass


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class Price:
    type: str
    baseCurrencyCode: str
    quoteCurrencyCode: str
    value: float
    estimated: float | None = None
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class Statistics:
    userId: int
    totalOrdersCount: int
    successRate: str
    successPercent: int
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class User:
    userId: int
    nickname: str
    avatarCode: str
    statistics: Statistics
    isVerified: bool
    onlineStatus: Literal["ONLINE", "OFFLINE"]
    lastOnlineMinutesAgo: int | None = None
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class UserID:
    userId: int
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class Volume:
    currencyCode: str
    amount: float
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class ChangeLogItem:
    status: str
    createDateTime: str
    initiatorUserId: int | None = None
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class ChangeLog:
    items: list[ChangeLogItem]
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class PaymentDetails:
    id: int
    userId: int
    paymentMethod: PaymentMethod
    currency: str
    attributes: Attributes
    name: str
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class PaymentDetailsHistory:
    paymentMethod: PaymentMethod
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class Fee:
    rate: float
    # initVolume: Volume
    availableVolume: Volume
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class OrderRounding:
    mode: str
    scale: float
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class Offer:
    id: int
    number: str
    type: str
    price: Price
    availableVolume: AvailableVolume
    orderAmountLimits: AmountLimits
    orderVolumeLimits: OrderVolumeLimits
    orderRounding: OrderRounding | None = None
    status: str | None = None
    changeLog: ChangeLog | None = None
    comment: str | None = None
    createDateTime: str | None = None
    paymentConfirmTimeout: str | None = None
    # initVolume: Volume | None = None
    user: User | None = None
    paymentMethods: list[PaymentMethod] | None = None
    fee: Fee | None = None
    paymentDetails: list[PaymentDetails] | None = None
    orderConfirmationTimeout: str | None = None
    orderAcceptTimeout: str | None = None
    unknown_things: CatchAll = None

    @staticmethod
    def to_dict():
        pass

    @staticmethod
    def from_dict(data):
        pass


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class MarketOffer:
    id: int
    number: str
    user: User
    type: str
    price: Price
    orderAmountLimits: AmountLimits
    orderVolumeLimits: AmountLimits
    paymentMethods: list[PaymentMethod]
    availableVolume: float
    unknown_things: CatchAll = None

    @staticmethod
    def to_dict():
        pass

    @staticmethod
    def from_dict(data):
        pass


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class Order:
    id: int
    number: str
    seller: User
    buyer: User
    offerId: int
    offerType: str
    offerComment: str
    isExpress: bool
    price: Price
    paymentDetails: PaymentDetails
    volume: Volume
    amount: Volume
    feeVolume: Volume
    paymentConfirmTimeout: str
    createDateTime: str
    holdRestrictionsWillBeApplied: bool
    status: str
    changeLog: ChangeLog
    buyerSendingPaymentConfirmationTimeout: str
    confirmationDateTime: str | None
    statusUpdateDateTime: str | None
    cancelReason: str | None = None
    acceptDateTime: str | None = None
    unknown_things: CatchAll = None

    @staticmethod
    def to_dict():
        pass

    @staticmethod
    def from_dict(data):
        pass


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class OrderHistory:
    amount: Volume
    buyer: UserID
    id: int
    number: str
    paymentDetails: PaymentDetailsHistory
    seller: UserID
    status: str
    statusUpdateDateTime: str | None
    volume: Volume
    unknown_things: CatchAll = None

    @staticmethod
    def to_dict():
        pass

    @staticmethod
    def from_dict(data):
        pass
