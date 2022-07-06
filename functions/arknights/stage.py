import jieba

from core import log, bot, Message, Chain, exec_before_init
from core.util import any_match
from core.resource.arknightsGameData import ArknightsGameData


class Stage:
    @staticmethod
    @exec_before_init
    async def init_enemies():
        log.info('building stages keywords dict...')

        stages = list(ArknightsGameData().stages_map.keys())

        with open('resource/stages.txt', mode='w', encoding='utf-8') as file:
            file.write('\n'.join([f'{name} 500 n' for name in stages]))

        jieba.load_userdict('resource/stages.txt')


@bot.on_message(keywords=['地图', '关卡'], allow_direct=True)
async def _(data: Message):
    words = jieba.lcut(
        data.text_initial.upper().replace(' ', '')
    )
    level = ''
    if any_match(data.text, ['突袭']):
        level = '_hard'
    if any_match(data.text, ['简单', '剧情']):
        level = '_easy'
    if any_match(data.text, ['困难', '磨难']):
        level = '_tough'

    stage_id = None
    stages_map = ArknightsGameData().stages_map

    for item in words:
        stage_key = item + level
        if stage_key in stages_map:
            stage_id = stages_map[stage_key]

    if stage_id:
        return Chain(data).html('template/stage/stage.html', ArknightsGameData().stages[stage_id])
    else:
        return Chain(data).text('抱歉博士，没有查询到相关地图信息')
