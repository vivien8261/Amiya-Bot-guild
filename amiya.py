import asyncio
import functions

from core import bot, init_task

if __name__ == '__main__':
    try:
        asyncio.run(
            asyncio.wait(
                [
                    asyncio.wait(init_task),
                    bot.start(enable_chromium=True)
                ]
            )
        )
    except KeyboardInterrupt:
        pass
