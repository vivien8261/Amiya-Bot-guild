import re
import copy

from core import bot, GroupConfig, Message, Chain
from core.util import find_similar_list, any_match, get_index_from_text
from core.resource.arknightsGameData import ArknightsGameData, ArknightsGameDataResource

from .operatorInfo import OperatorInfo
from .operatorData import OperatorData
from .initData import OperatorSearchInfo, InitData

bot.set_group_config(GroupConfig('operator', allow_direct=True))


class LoopBreak(Exception):
    def __init__(self, index, name='', value=''):
        self.index = index
        self.value = value
        self.name = name

    def __str__(self):
        return self.index, self.name


def search_info(words: list, source_keys: list = None, text: str = ''):
    info_source = {
        'name': [OperatorInfo.operator_map, OperatorInfo.operator_list],
        'level': [InitData.skill_level_list],
        'skill': [OperatorInfo.skill_map],
        'skill_index': [InitData.skill_index_list],
        'skin_key': [OperatorInfo.skins_keywords],
        'voice_key': [InitData.voices],
        'story_key': [OperatorInfo.stories_title]
    }

    info = OperatorSearchInfo()
    info_key = list(info_source.keys()) if not source_keys else source_keys

    words = [n.lower() for n in copy.deepcopy(words)]

    if 'name' in info_key and text:
        for name in OperatorInfo.operator_one_char_list:
            if name in text:
                info.name = name

    while True:
        try:
            if len(words) == 0:
                break
            for index, item in enumerate(words):
                for name in copy.deepcopy(info_key):
                    for source in info_source[name]:

                        if name == 'skill':
                            res, rate = find_similar_list(item, source.keys(), _random=True)
                            if res:
                                setattr(info, name, source[res])
                                raise LoopBreak(index, name, source[res])

                        elif item in source:
                            value = source[item] if type(source) is dict else item

                            setattr(info, name, value)
                            raise LoopBreak(index, name, value)

                if index == len(words) - 1:
                    raise LoopBreak('done')
        except LoopBreak as e:
            if e.index == 'done':
                break

            words.pop(e.index)

            if e.name == 'name' and e.value == '?????????':
                continue
            else:
                info_key.remove(e.name)

    if info.name == '?????????':
        for item in ['?????????', 'amiya']:
            t = text.lower()
            if t.startswith(item) and t.count(item) == 1:
                info.name = ''

    if info.name and info.skill and OperatorInfo.skill_operator[info.skill] != info.name:
        info.skill = ''

    return info


async def level_up(data: Message):
    info = search_info(data.text_words, source_keys=['name', 'level', 'skill_index'], text=data.text)

    condition = any_match(data.text, ['??????', '??????'])
    condition2 = info.name and '??????' in data.text

    return bool(condition or condition2), (3 if condition2 else 2)


async def operator(data: Message):
    info = search_info(data.text_words, source_keys=['name'], text=data.text)
    return bool(info.name), 2 if info.name != '?????????' else 0


@bot.on_message(group_id='operator', keywords=['??????', '??????'], level=2)
async def _(data: Message):
    info = search_info(data.text_words, source_keys=['skin_key', 'name'], text=data.text)

    if not info.name:
        wait = await data.wait(Chain(data).text('??????????????????????????????????????????'))
        if not wait or not wait.text:
            return None
        info.name = wait.text

    operators = ArknightsGameData().operators

    if info.name not in operators:
        return Chain(data).text(f'???????????????????????????"{info.name}"')

    opt = operators[info.name]
    skins = opt.skins()
    index = get_index_from_text(data.text, skins)

    if index is None:
        text = f'?????????????????????{info.name}???????????????\n\n'
        for index, item in enumerate(skins):
            text += f'[{index + 1}] %s\n' % item['skin_name']
        text += '\n?????????????????????????????????????????????'

        wait = await data.wait(Chain(data).text(text))
        if wait:
            index = get_index_from_text(wait.text_digits, skins)

    if index is not None:
        skin_item = skins[index]
        skin_data = {
            'name': info.name,
            'data': skin_item,
            'path': await ArknightsGameDataResource.get_skin_file(opt, skin_item)
        }

        return Chain(data).html('template/operator/operatorSkin.html', skin_data)


@bot.on_message(group_id='operator', keywords=['??????'], level=2)
async def _(data: Message):
    info = search_info(data.text_words, source_keys=['name'], text=data.text)

    if not info.name:
        wait = await data.wait(Chain(data).text('??????????????????????????????????????????'))
        if not wait or not wait.text:
            return None
        info.name = wait.text

    if info.name not in ArknightsGameData().operators:
        return Chain(data).text(f'???????????????????????????"{info.name}"')

    is_story = '??????' in data.text
    result = OperatorData.find_operator_module(info, is_story)

    if not result:
        return Chain(data).text(f'???????????????{info.name}??????????????????')
    if is_story:
        return Chain(data).text_image(result)
    else:
        return Chain(data).html('template/operator/operatorModule.html', result)


@bot.on_message(group_id='operator', keywords=['??????'], level=2)
async def _(data: Message):
    return Chain(data).text(f'?????????????????????????????????????????????')


@bot.on_message(group_id='operator', keywords=['??????', '??????'], level=2)
async def _(data: Message):
    info = search_info(data.text_words, source_keys=['story_key', 'name'], text=data.text)

    if not info.name:
        wait = await data.wait(Chain(data).text('??????????????????????????????????????????'))
        if not wait or not wait.text:
            return None
        info.name = wait.text

    operators = ArknightsGameData().operators

    if info.name not in operators:
        return Chain(data).text(f'???????????????????????????"{info.name}"')

    opt = operators[info.name]
    stories = opt.stories()
    stories_map = {item['story_title']: item['story_text'] for item in stories}
    index = get_index_from_text(data.text, stories)

    if not info.story_key and index is None:
        text = f'?????????????????????{opt.name}???????????????\n\n'
        for index, item in enumerate(stories):
            text += f'[{index + 1}] %s\n' % item['story_title']
        text += '\n?????????????????????????????????????????????'

        wait = await data.wait(Chain(data).text(text))
        if wait:
            index = get_index_from_text(wait.text_digits, stories)

    if index is not None:
        info.story_key = stories[index]['story_title']

    if not info.story_key:
        return None

    if info.story_key in stories_map:
        return Chain(data).text(f'?????????????????????{info.name}???{info.story_key}????????????\n\n{stories_map[info.story_key]}')
    else:
        return Chain(data).text(f'???????????????????????????{info.name}???{info.story_key}????????????')


@bot.on_message(group_id='operator', verify=level_up)
async def _(data: Message):
    info = search_info(data.text_words, source_keys=['level', 'skill_index', 'name'], text=data.text)

    if not info.name:
        wait = await data.wait(Chain(data).text('??????????????????????????????????????????'))
        if not wait or not wait.text:
            return None
        info.name = wait.text

    if '??????' in data.text:
        result = await OperatorData.get_level_up_cost(info)
        template = 'template/operator/operatorCost.html'
    else:
        result = await OperatorData.get_skills_detail(info)
        template = 'template/operator/skillsDetail.html'

    if not result:
        return Chain(data).text('????????????????????????????????????????????????')

    return Chain(data).html(template, result)


@bot.on_message(group_id='operator', verify=operator)
async def _(data: Message):
    info = search_info(data.text_words, source_keys=['name'], text=data.text)

    if '??????' in data.text:
        result = await OperatorData.get_skills_detail(info)
        template = 'template/operator/skillsDetail.html'
    else:
        result = await OperatorData.get_operator_detail(info)
        template = 'template/operator/operatorInfo.html'

    if not result:
        return Chain(data).text('????????????????????????????????????????????????')

    return Chain(data).html(template, result)
