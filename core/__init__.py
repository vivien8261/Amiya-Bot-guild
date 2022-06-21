import traceback

from amiyabot import MultipleAccounts, AmiyaBot, BotInstance, Message, Chain, log
from core.lib.timedTask import TasksControl
from core.util import read_yaml

__setting = read_yaml('config/qqbot.yaml', _dict=True)

bot = MultipleAccounts(
    [
        AmiyaBot(**item) for item in __setting['accounts']
    ]
)
tasks_control = TasksControl()
init_task = [
    tasks_control.run_tasks()
]

bot.prefix_keywords = read_yaml('config/talking.yaml').call.positive


def exec_before_init(coro):
    init_task.append(coro())
    return coro


@bot.on_exception()
async def _(err: Exception, instance: BotInstance):
    async with instance.send_message(channel_id='7126590') as chain:
        chain.text_image(traceback.format_exc())
