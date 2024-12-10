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
    rate: float
    is_created: bool
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class Balances:
    available_balance_total_fiat_amount: float
    available_balance_total_fiat_currency: str
    accounts: list[BalanceAccount]
    unknown_things: CatchAll = None

    @staticmethod
    def to_dict():
        pass

    @staticmethod
    def from_dict(data):
        pass
