from amiyabot.database import MysqlConfig
from core.util import read_yaml

config = MysqlConfig(
    **read_yaml('config/database.yaml', _dict=True)
)
