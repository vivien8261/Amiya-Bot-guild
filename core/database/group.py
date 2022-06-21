from amiyabot.database import *
from core.database import config
from typing import Union

db = connect_database('amiya_group', True, config)


class GroupBaseModel(ModelClass):
    class Meta:
        database = db


@table
class Group(GroupBaseModel):
    group_id: Union[CharField, str] = CharField(primary_key=True)
    group_name: str = CharField()
    permission: str = CharField()


@table
class GroupActive(GroupBaseModel):
    group_id: str = CharField(primary_key=True)
    active: int = IntegerField(default=1)
    sleep_time: int = BigIntegerField(default=0)


@table
class GroupSetting(GroupBaseModel):
    group_id: str = CharField(primary_key=True)
    send_notice: int = IntegerField(default=1, null=True)
    send_weibo: int = IntegerField(default=0, null=True)


@table
class GroupNotice(GroupBaseModel):
    content = CharField()
    send_time = BigIntegerField()
    send_user = CharField()
