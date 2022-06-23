from core import bot, Message, Chain


@bot.on_message(keywords=['功能', '帮助', '说明', 'help'], allow_direct=True)
async def _(data: Message):
    return Chain(data).html('template/function/function.html', render_time=1000)
