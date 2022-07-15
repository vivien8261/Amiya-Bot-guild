import json

from amiyabot import log
from amiyabot.network.httpRequests import http_requests
from core.database.bot import PenguinData

api = 'https://penguin-stats.io/PenguinStats/api/v2/result/matrix'


async def save_penguin_data():
    async with log.catch('penguin data save error:'):
        res = await http_requests.get(api)
        res = json.loads(res)

        PenguinData.truncate_table()
        PenguinData.batch_insert(res['matrix'])

        log.info('save penguin data successful.')
