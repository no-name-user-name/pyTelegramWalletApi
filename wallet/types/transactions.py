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
class TxDetails:
    id: int
    type: str | None = None
    created_at: str | None = None
    crypto_amount: float | None = None
    fiat_amount: float | None = None
    crypto_currency: str | None = None
    fiat_currency: str | None = None
    value_at_time: float | None = None
    username: str | None = None
    tg_id: int | None = None
    mention: str | None = None
    status: str | None = None
    gateway: str | None = None
    input_addresses: str | None = None
    recipient_wallet_address: str | None = None
    transaction_link: str | None = None
    full_number_of_activations: int | None = None
    number_of_activations: int | None = None
    amount_of_activations: float | None = None
    remaining_amount: float | None = None
    fee_currency: str | None = None
    fee_amount: float | None = None
    activation_channel_title: str | None = None
    activation_channel_name: str | None = None
    check_url: str | None = None
    seller: str | None = None
    buyer: str | None = None
    avatar_code: str | None = None
    entity_id: int | None = None
    photo_url: str | None = None
    details_for_user: str | None = None
    pair_transaction_amount: float | None = None
    pair_transaction_currency: str | None = None
    is_blocked: str | None = None
    block: str | None = None
    is_cancellable: bool | None = None
    comment: str | None = None
    giveaway_gift: str | None = None
    network: str | None = None
    amount: int | None = None
    activated_amount: int | None = None
    currency: str | None = None
    block_reason: str | None = None
    cryptocurrency_exchange: str | None = None
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
    size: int
    transactions: list[TxDetails]
    offset: int = None
    unknown_things: CatchAll = None

    @staticmethod
    def to_dict():
        pass

    @staticmethod
    def from_dict(data):
        pass
