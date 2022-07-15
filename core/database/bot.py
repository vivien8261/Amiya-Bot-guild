from amiyabot.database import *
from core.database import config
from typing import Union

db = connect_database('amiya_bot', True, config)


class BotBaseModel(ModelClass):
    class Meta:
        database = db


@table
class GachaConfig(BotBaseModel):
    operator_name: str = CharField()
    operator_type: int = IntegerField()


@table
class Pool(BotBaseModel):
    pool_name: str = CharField(unique=True)
    pickup_6: str = CharField(null=True)
    pickup_5: str = CharField(null=True)
    pickup_4: str = CharField(null=True)
    pickup_s: str = CharField(null=True)
    limit_pool: int = IntegerField()


@table
class PoolSpOperator(BotBaseModel):
    pool_id: Union[ForeignKeyField, int] = ForeignKeyField(Pool, db_column='pool_id', on_delete='CASCADE')
    operator_name: str = CharField()
    rarity: int = IntegerField()
    classes: str = CharField()
    image: str = CharField()


@table
class TextReplace(BotBaseModel):
    user_id: str = CharField()
    group_id: str = CharField()
    origin: str = TextField()
    replace: str = TextField()
    in_time: int = BigIntegerField()
    is_global: int = IntegerField(default=0)
    is_active: int = IntegerField(default=1)


@table
class TextReplaceSetting(BotBaseModel):
    text: str = CharField()
    status: int = IntegerField()


@table
class PenguinData(BotBaseModel):
    stageId: str = CharField(null=True)
    itemId: str = CharField(null=True)
    times: int = IntegerField(null=True)
    quantity: int = IntegerField(null=True)
    stdDev: float = FloatField(null=True)
    start: int = BigIntegerField(null=True)
    end: int = BigIntegerField(null=True)
