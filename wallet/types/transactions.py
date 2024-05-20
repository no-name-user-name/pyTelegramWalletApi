from dataclasses import dataclass

from dataclasses_json import CatchAll, Undefined, dataclass_json


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class AccountAddress:
    address: str | None
    network: str
    network_code: str
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class BalanceAccount:
    currency: str
    available_balance: float
    available_balance_fiat_amount: float
    available_balance_fiat_currency: str
    has_transactions: bool
    addresses: list[AccountAddress]
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class Tx:
    id: int
    type: str
    created_at: str
    amount: int
    currency: str
    status: str
    gateway: str
    username: str
    tg_id: int
    mention: str
    input_addresses: str | None
    recipient_wallet_address: str | None
    # activated_amount: float
    # remaining_amount: float
    # purchase_external_id: int
    photo_url: str
    # details_for_user: None
    pair_transaction_amount: int
    pair_transaction_currency: str
    is_blocked: bool
    # block: str
    is_cancellable: bool
    network: str | None
    unknown_things: CatchAll = None

    @staticmethod
    def to_dict():
        pass

    @staticmethod
    def from_dict(data):
        pass


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class TxResponse:
    limit: int
    offset: int
    size: int
    transactions: list[Tx]
    unknown_things: CatchAll = None

    @staticmethod
    def to_dict():
        pass

    @staticmethod
    def from_dict(data):
        pass


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class TxDetails:
    id: int
    type: str | None
    created_at: str | None
    crypto_amount: float | None
    fiat_amount: float | None
    crypto_currency: str | None
    fiat_currency: str | None
    value_at_time: float | None
    username: str | None
    tg_id: int | None
    mention: str | None
    status: str | None
    gateway: str | None
    input_addresses: str | None
    recipient_wallet_address: str | None
    transaction_link: str | None
    full_number_of_activations: int | None
    number_of_activations: int | None
    amount_of_activations: float | None
    remaining_amount: float | None
    fee_currency: str | None
    fee_amount: float | None
    activation_channel_title: str | None
    activation_channel_name: str | None
    check_url: str | None
    seller: str | None
    buyer: str | None
    avatar_code: str | None
    entity_id: int | None
    photo_url: str | None
    details_for_user: str | None
    pair_transaction_amount: float | None
    pair_transaction_currency: str | None
    is_blocked: str | None
    block: str | None
    is_cancellable: bool
    comment: str | None
    giveaway_gift: str | None
    network: str | None
    unknown_things: CatchAll = None

    @staticmethod
    def to_dict():
        pass

    @staticmethod
    def from_dict(data):
        pass
