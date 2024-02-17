from datetime import datetime
from enum import IntEnum
from tortoise import fields
from tortoise_api_model import Model, TsModel, User, DatetimeSecField
from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel
from tortoise.contrib.pydantic.creator import PydanticMeta
from tortoise.functions import Count
from tortoise.queryset import QuerySet


class ClientStatus(IntEnum):
    block = 0
    wait = 1
    pause = 2
    active = 3


class AdvStatus(IntEnum):
    defActive = 0
    active = 1
    two = 2
    old = 3
    four = 4
    notFound = 9


class OrderStatus(IntEnum):
    zero = 0
    one = 1
    two = 2
    three = 3
    done = 4
    fifth = 5
    canceled = 6
    paid_and_canceled = 7
    # COMPLETED, PENDING, TRADING, BUYER_PAYED, DISTRIBUTING, COMPLETED, IN_APPEAL, CANCELLED, CANCELLED_BY_SYSTEM


class ExType(IntEnum):
    p2p = 1
    cex = 2
    main = 3  # p2p+cex
    dex = 4
    futures = 8


class DepType(IntEnum):
    earn = 1
    stake = 2
    beth = 3
    lend = 4


class AssetType(IntEnum):
    spot = 1
    earn = 2
    found = 3


class TradeType(IntEnum):
    BUY = 0
    SELL = 1


class PmType(IntEnum):
    bank = 0
    web_wallet = 1
    cash = 2
    gift_card = 3
    credit_card = 4


class Country(Model):
    id = fields.SmallIntField(pk=True)
    code: int | None = fields.IntField(null=True)
    short: str | None = fields.CharField(3, unique=True, null=True)
    name: str | None = fields.CharField(63, unique=True, null=True)
    cur: fields.ForeignKeyRelation["Cur"] = fields.ForeignKeyField("models.Cur", related_name="countries")
    curexs: fields.ManyToManyRelation["Curex"]
    fiats: fields.BackwardFKRelation["Fiat"]

    _icon = 'location'


class Cur(Model):
    id = fields.SmallIntField(pk=True)
    ticker: str = fields.CharField(3, unique=True)
    country: str | None = fields.CharField(63, null=True)

    pms: fields.ManyToManyRelation["Pm"] = fields.ManyToManyField("models.Pm", through="pmcur")
    pmcurs: fields.ReverseRelation["Pmcur"]  # no need. use pms
    pairs: fields.ReverseRelation["Pair"]
    countries: fields.ReverseRelation[Country]

    _name = 'ticker'
    _icon = 'currency-yuan'

    class Meta:
        table_description = "Fiat currencies"


class Coin(Model):
    id: int = fields.SmallIntField(pk=True)
    ticker: str = fields.CharField(15, unique=True)
    rate: float | None = fields.FloatField(null=True)
    is_fiat: bool = fields.BooleanField(default=False)
    exs: fields.ManyToManyRelation["Ex"] = fields.ManyToManyField("models.Ex", through="coinex")

    assets: fields.ReverseRelation["Asset"]
    deps: fields.ReverseRelation["Dep"]
    deps_reward: fields.ReverseRelation["Dep"]
    deps_bonus: fields.ReverseRelation["Dep"]

    _name = 'ticker'
    _icon = 'coin'

    def repr(self):
        return super().repr() + (self.is_fiat and ' (fiat)' or '')

    class Meta:
        table_description = "Crypro coins"


class Ex(Model):
    id: int = fields.SmallIntField(pk=True)
    name: str = fields.CharField(31)
    type: ExType = fields.IntEnumField(ExType)

    pmcurs: fields.ManyToManyRelation["Pmcur"] = fields.ManyToManyField("models.Pmcur", through="pmcurex")
    coins: fields.ManyToManyRelation[Coin]

    pairs: fields.ReverseRelation["Pair"]
    deps: fields.ReverseRelation["Dep"]
    test: fields.BackwardOneToOneRelation["TestEx"]

    _icon = 'exchange'

    class Meta:
        table_description = "Exchanges"
        unique_together = (("name", "type"),)


class Curex(Model):
    cur: fields.ForeignKeyRelation[Cur] = fields.ForeignKeyField("models.Cur")
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex")
    countries: fields.ManyToManyRelation[Country] = fields.ManyToManyField("models.Country", through="curexcountry",
                                                                           backward_key="curexs")


class Pair(TsModel):
    id = fields.SmallIntField(pk=True)
    coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField("models.Coin", related_name="pairs")
    cur: fields.ForeignKeyRelation[Cur] = fields.ForeignKeyField("models.Cur", related_name="pairs")
    fee: float = fields.FloatField()
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex", related_name="pairs")
    directions: fields.ReverseRelation["Direction"]

    _icon = 'circles-relation'

    class Meta:
        table_description = "Coin/Currency pairs"
        unique_together = (("coin", "cur", "ex"),)

    def repr(self):
        return f"{self.coin.ticker}/{self.cur.ticker}"


class Direction(Model):
    id = fields.SmallIntField(pk=True)
    pair: fields.ForeignKeyRelation[Pair] = fields.ForeignKeyField("models.Pair", related_name="directions")
    sell: bool = fields.BooleanField()
    total: int = fields.IntField()
    ads: fields.ReverseRelation["Ad"]

    _icon = 'direction-sign'

    class Meta:
        table_description = "Trade directions"
        unique_together = (("pair", "sell"),)

    def repr(self):
        return f"{self.pair.coin.ticker}/{self.pair.cur.ticker} {'SELL' if self.sell else 'BUY'}"


class Client(TsModel):
    id: int = fields.SmallIntField(pk=True)
    name: str = fields.CharField(127)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="clients")
    user_id: int
    ref: fields.ForeignKeyNullableRelation["Client"] = fields.ForeignKeyField("models.Client", related_name="refs", null=True)
    ref_id: int | None
    status: ClientStatus = fields.IntEnumField(ClientStatus, default=ClientStatus.wait)

    agents: fields.BackwardFKRelation["Agent"]
    fiats: fields.BackwardFKRelation["Fiat"]
    refs: fields.BackwardFKRelation["Client"]

    _icon = 'heart-handshake'

    class Meta:
        table_description = "Our clients"


class Agent(TsModel):
    id: int
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex", related_name="agents")
    auth: {} = fields.JSONField(null=True)
    client: fields.ForeignKeyRelation["Client"] = fields.ForeignKeyField("models.Client", related_name="agents")
    assets: fields.ReverseRelation["Asset"]
    orders: fields.ReverseRelation["Order"]
    ads: fields.ReverseRelation["Ad"]

    _icon = 'spy'

    def repr(self):
        return f'{self.ex.name}-{self.client.name}'

    class Meta:
        table_description = "Agents"


class Adpm(Model):
    ad: fields.ForeignKeyRelation["Ad"] = fields.ForeignKeyField("models.Ad")
    pm: fields.ForeignKeyRelation["Pm"] = fields.ForeignKeyField("models.Pm")

    # no need repr()

    class Meta:
        table_description = "P2P Advertisements - Payment methods"


class Ad(TsModel):
    id: int = fields.BigIntField(pk=True)
    direction: fields.ForeignKeyRelation[Direction] = fields.ForeignKeyField("models.Direction", related_name="ads")
    price: float = fields.FloatField()
    pms: fields.ManyToManyRelation["Pm"] = fields.ManyToManyField("models.Pm", through="adpm")  # only root pms
    maxFiat: float = fields.FloatField()
    minFiat: float = fields.FloatField()
    detail: str = fields.CharField(4095, null=True)
    autoMsg: str = fields.CharField(255, null=True)
    agent: fields.ForeignKeyRelation[Agent] = fields.ForeignKeyField("models.Agent", "ads")
    status: AdvStatus = fields.IntEnumField(AdvStatus)

    orders: fields.ReverseRelation["Order"]

    _icon = 'ad'

    def repr(self):
        return f"{TradeType(int(self.direction.sell.name)).name}: {self.price:.3g}"

    class Meta:
        table_description = "P2P Advertisements"


class Pm(Model):
    name: str = fields.CharField(63, unique=True)
    identifier: str | None = fields.CharField(63, unique=True, null=True)
    rank: int | None = fields.SmallIntField(default=0)
    # # type: PmType|None = fields.IntEnumField(PmType, null=True)
    type: int | None = fields.SmallIntField(null=True)
    template: int | None = fields.SmallIntField(null=True)
    ico: str | None = fields.CharField(127, null=True)
    logo: str | None = fields.CharField(127, null=True)
    color: str | None = fields.CharField(7, null=True)
    multiAllow: bool | None = fields.BooleanField(null=True)
    riskLevel: int | None = fields.SmallIntField(null=True)
    chatNeed: bool | None = fields.BooleanField(null=True)

    ads: fields.ManyToManyRelation[Ad]
    curs: fields.ManyToManyRelation[Cur]
    exs: fields.ManyToManyRelation[Ex] = fields.ManyToManyField("models.Ex",
                                                                through="pmex")  # no need. use pmexs[.exid]
    orders: fields.ReverseRelation["Order"]
    pmcurs: fields.ReverseRelation["Pmcur"]  # no need. use curs
    pmexs: fields.ReverseRelation["Pmex"]

    _icon = 'currency'

    class Meta:
        table_description = "Payment methods"


class Pmcur(Model):  # for fiat with no exs tie
    pm: fields.ForeignKeyRelation[Pm] = fields.ForeignKeyField("models.Pm")
    pm_id: int
    cur: fields.ForeignKeyRelation[Cur] = fields.ForeignKeyField("models.Cur")
    cur_id: int

    fiats: fields.ReverseRelation["Fiat"]
    exs: fields.ManyToManyRelation[Ex]

    _name = 'pm__name'

    # _sorts = ['-limits_count']

    def repr(self):
        return f"{self.pm.name}-{self.cur.ticker}"

    @classmethod
    def pydListItem(cls) -> type[PydanticModel]:
        if not cls._pydListItem:
            mo = PydanticMeta
            mo.max_recursion = 1
            mo.exclude_raw_fields = True  # default: True
            # mo.backward_relations = False # default: True
            cls._pydListItem = pydantic_model_creator(cls, name=cls.__name__ + 'ListItem', meta_override=mo,
                                                      exclude=('pmcurexs',))
        return cls._pydListItem

    @classmethod
    def pageQuery(cls, sorts: list[str], limit: int = 1000, offset: int = 0, q: str = None, **kwargs) -> QuerySet:
        query = super().pageQuery([], limit, offset, q)
        if kwargs.pop('only_empty', None):
            query = query.exclude(limits__not_isnull=True)
        else:
            query = query.annotate(limits_count=Count('limits')).order_by('-limits_count')
        return query.filter(**kwargs)

    class Meta:
        table_description = "Payment methods - Currencies"
        unique_together = (("pm", "cur"),)


class Pmex(Model):  # existence pm in ex with no cur tie
    pm: fields.ForeignKeyRelation[Pm] = fields.ForeignKeyField("models.Pm", 'pmexs')
    pm_id: int
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex", 'pmexs')
    ex_id: int | None
    exid: int | None = fields.SmallIntField(null=True)

    def repr(self):
        return f"{self.pm.name}-{self.ex.name}"

    class Meta:
        table_description = "Payment methods - Currencies"
        unique_together = (("ex", "exid"),)


class Pmcurex(Model):  # existence pm in ex for exact cur, with "blocked" flag
    pmcur: fields.ForeignKeyRelation[Pmcur] = fields.ForeignKeyField("models.Pmcur")
    pmcur_id: int
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex")
    ex_id: int
    blocked: bool = fields.BooleanField(default=False)

    def repr(self, caller: type[Model] = None):
        return ('[X] ' if self.blocked else '') + super().repr()

    class Meta:
        table_description = "Payment methods - Currencies"


class Fiat(Model):
    pmcur: fields.ForeignKeyRelation[Pmcur] = fields.ForeignKeyField("models.Pmcur")
    pmcur_id: int
    country: fields.ForeignKeyRelation[Country] = fields.ForeignKeyField("models.Country", related_name="fiats")
    country_id: int
    detail: str = fields.CharField(127)
    client: fields.ForeignKeyRelation[Client] = fields.ForeignKeyField("models.Client", "fiats")
    client_id: int
    amount: float | None = fields.FloatField(default=None, null=True)
    target: float | None = fields.FloatField(default=None, null=True)

    orders: fields.ReverseRelation["Order"]

    _icon = 'cash'

    def repr(self):
        return f"{self.id}: {self.pmcur.repr()} ({self.client.name})"

    class Meta:
        table_description = "Currency accounts balance"


class Limit(Model):
    pmcur: fields.ForeignKeyRelation[Pmcur] = fields.ForeignKeyField("models.Pmcur")
    pmcur_id: int
    amount: int = fields.IntField(null=True)  # '$' if unit >= 0 else 'transactions count'
    unit: int = fields.IntField(default=30)  # positive: $/days, 0: $/transaction, negative: transactions count / days
    level: float | None = fields.IntField(default=0, null=True)  # 0 - same group, 1 - to parent group, 2 - to grandparent  # only for output trans, on input = None
    income: bool = fields.BooleanField(default=False)
    added_by: fields.ForeignKeyRelation["Client"] = fields.ForeignKeyField("models.Client", related_name="limits")
    added_by_id: int

    _icon = 'frame'

    def repr(self):
        return f"{self.pmcur.repr()}[{'<-' if self.income else '->'}]"

    class Meta:
        table_description = "Currency accounts balance"


class Asset(Model):
    coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField("models.Coin", related_name="assets")
    coin_id: int
    agent: fields.ForeignKeyRelation[Agent] = fields.ForeignKeyField("models.Agent", "assets")
    agent_id: int
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex", "assets")
    ex_id: int
    type: AssetType = fields.IntEnumField(AssetType)
    free: float = fields.FloatField()
    freeze: float | None = fields.FloatField(default=0)
    lock: float | None = fields.FloatField(default=0)
    target: float | None = fields.FloatField(default=0, null=True)

    _icon = 'currency-bitcoin'

    def repr(self):
        return f'{self.coin.ticker} {self.free:.3g}/{self.freeze:.3g} user:{self.agent.repr()}'

    class Meta:
        table_description = "Coin balance"
        unique_together = (("coin", "agent", "ex", "type"),)


class Order(TsModel):
    id: int = fields.BigIntField(pk=True)
    ad: fields.ForeignKeyRelation[Ad] = fields.ForeignKeyField("models.Ad", related_name="ads")
    ad_id: int
    amount: float = fields.FloatField()
    fiat: fields.ForeignKeyRelation[Fiat] = fields.ForeignKeyField("models.Fiat", related_name="orders", null=True)
    fiat_id: int | None
    pm: fields.ForeignKeyRelation[Pm] = fields.ForeignKeyField("models.Pm", related_name="orders", null=True)
    pm_id: int | None
    taker: fields.ForeignKeyRelation[Agent] = fields.ForeignKeyField("models.Agent", "orders")
    taker_id: int
    status: OrderStatus = fields.IntEnumField(OrderStatus)
    notify_pay_at: datetime | None = DatetimeSecField(null=True)
    confirm_pay_at: datetime | None = DatetimeSecField(null=True)

    _icon = 'file-check'

    def repr(self):
        return f'{self.taker.repr()}: {self.amount:.3g} pm:{self.pm.name}/{self.fiat_id} {self.status.name}'

    class Meta:
        table_description = "P2P Orders"


class Dep(TsModel):
    pid: str = fields.CharField(31)  # product_id
    apr: float = fields.FloatField()
    fee: float | None = fields.FloatField(null=True)
    apr_is_fixed: bool = fields.BooleanField(default=False)
    duration: int | None = fields.SmallIntField(null=True)
    early_redeem: bool | None = fields.BooleanField(null=True)
    type: DepType = fields.IntEnumField(DepType)
    # mb: renewable?
    min_limit: float = fields.FloatField()
    max_limit: float | None = fields.FloatField(null=True)
    is_active: bool = fields.BooleanField(default=True)

    coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField("models.Coin", related_name="deps")
    coin_id: int
    reward_coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField("models.Coin", related_name="deps_reward",
                                                                          null=True)
    reward_coin_id: int | None = None
    bonus_coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField("models.Coin", related_name="deps_bonus",
                                                                         null=True)
    bonus_coin_id: int | None = None
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex", related_name="deps")
    ex_id: int
    investments: fields.ReverseRelation["Investment"]

    _icon = 'seeding'
    _name = 'pid'

    def repr(self, caller: Model.__class__ = None):
        return f'{self.coin.ticker}:{self.apr * 100:.3g}% {f"{self.duration}d" if self.duration and self.duration > 0 else "flex"}'

    class Meta:
        table_description = "Investment products"
        unique_together = (("pid", "type", "ex"),)


class Investment(TsModel):
    dep: fields.ForeignKeyRelation[Dep] = fields.ForeignKeyField("models.Dep", related_name="investments")
    dep_id: int
    amount: float = fields.FloatField()
    is_active: bool = fields.BooleanField(default=True)

    _icon = 'trending-up'

    def repr(self):
        return f'{self.amount:.3g} {self.dep.repr()}'

    class Meta:
        table_description = "Investments"


class TestEx(TsModel):
    ex: fields.OneToOneRelation[Ex] = fields.OneToOneField("models.Ex", related_name="test")
    ex_id: int
    ads: bool = fields.BooleanField(default=False, description='Got Ads, post/upd')
    pms: bool = fields.BooleanField(default=False, description='Got Pms in this Ex')
    coins: bool = fields.BooleanField(default=False, description='Coins for p2p in this Ex')
    curs: bool = fields.BooleanField(default=False, description='Currencies available in this Ex')
    pmcurs: bool = fields.BooleanField(default=False, description='Got Pmcurs, save in db')
    fiats: bool = fields.BooleanField(default=False, description='Fiat creds for this Ex')
    deps: bool | None = fields.BooleanField(default=False, null=True, description='Deposits in this Ex')
    _icon = 'test-pipe'

    def repr(self):
        return self.ex.name

    class Meta:
        table_description = "Test Exs"


class Vpn(Model):
    client: fields.OneToOneRelation[Client] = fields.OneToOneField("models.Client", related_name="vpn")
    client_id: int
    priv: str = fields.CharField(63, unique=True)
    pub: str = fields.CharField(63, unique=True)
    created_at: datetime|None = DatetimeSecField(auto_now_add=True)
    _icon = 'vpn'

    def repr(self):
        return self.client.name

    class Meta:
        table_description = "Test Exs"
