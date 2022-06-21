from amiyabot.database import *
from core.database import config
from core.util import read_yaml
from typing import Union

db = connect_database('amiya_user', True, config)
game = read_yaml('config/game.yaml')


class UserBaseModel(ModelClass):
    class Meta:
        database = db


@table
class User(UserBaseModel):
    user_id: Union[CharField, str] = CharField(primary_key=True)
    nickname: str = CharField(null=True)
    message_num: int = IntegerField(default=0)
    black: int = IntegerField(default=0)


@table
class UserInfo(UserBaseModel):
    user_id: Union[ForeignKeyField, str] = ForeignKeyField(User, db_column='user_id', on_delete='CASCADE')
    user_feeling: int = IntegerField(default=0)
    user_mood: int = IntegerField(default=15)
    sign_in: int = IntegerField(default=0)
    sign_times: int = IntegerField(default=0)
    jade_point: int = IntegerField(default=0)
    jade_point_max: int = IntegerField(default=0)

    @classmethod
    def get_user(cls, user_id):
        User.get_or_create(user_id=user_id)
        return cls.get_or_create(user_id=user_id)[0]

    @classmethod
    def get_user_info(cls, user_id):
        user = model_to_dict(User.get_or_create(user_id=user_id)[0])
        user_info = model_to_dict(cls.get_or_create(user_id=user_id)[0])
        user_gacha_info = model_to_dict(UserGachaInfo.get_or_create(user_id=user_id)[0])
        operator_box = model_to_dict(OperatorBox.get_or_create(user_id=user_id)[0])

        return {
            'user': user,
            'user_info': user_info,
            'user_gacha_info': user_gacha_info,
            'operator_box': operator_box
        }

    @classmethod
    def add_jade_point(cls, user_id, point):
        user: UserInfo = cls.get_user(user_id)

        surplus = game.jade_point_max - user.jade_point_max
        if surplus <= 0:
            return None

        if point > surplus:
            point = surplus

        update = {
            'jade_point': UserInfo.jade_point + point,
            'jade_point_max': UserInfo.jade_point_max + point
        }
        cls.update(**update).where(UserInfo.user_id == user_id).execute()


@table
class UserGachaInfo(UserBaseModel):
    user_id: Union[ForeignKeyField, str] = ForeignKeyField(User, db_column='user_id', on_delete='CASCADE')
    coupon: int = IntegerField(default=50)
    gacha_break_even: int = IntegerField(default=0)
    gacha_pool: int = IntegerField(default=1)


@table
class OperatorBox(UserBaseModel):
    user_id: str = CharField()
    operator: str = TextField(default='')


@table
class Intellect(UserBaseModel):
    user_id: str = CharField(primary_key=True)
    belong_id: str = CharField(null=True)
    cur_num: int = IntegerField()
    full_num: int = IntegerField()
    full_time: int = IntegerField()
    message_type: str = CharField()
    group_id: str = CharField()
    in_time: int = IntegerField()
    status: int = IntegerField()
