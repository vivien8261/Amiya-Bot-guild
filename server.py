from fastapi import FastAPI
from amiyabot.database import query_to_list
from core.database.bot import Pool, PoolSpOperator, GachaConfig

app = FastAPI()


def response(data=None,
             code: int = 200,
             message: str = ''):
    return {
        'data': data,
        'code': code,
        'message': message
    }


@app.get('/pool/getGachaPool')
def get_pool():
    data = {
        'Pool': query_to_list(Pool.select()),
        'PoolSpOperator': query_to_list(PoolSpOperator.select()),
        'GachaConfig': query_to_list(GachaConfig.select())
    }

    for item in data['PoolSpOperator']:
        item['pool_id'] = item['pool_id']['id']

    return response(data=data)
