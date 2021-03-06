from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import Executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from src.filters import filters_setup
from src.settings import DEBUG, VK_TOKEN, REDIS_HOST, REDIS_PORT, REDIS_DB_FSM, TG_BOT_TOKEN, REDIS_PASSWORD
from src.middleware import middlewares_setup
from src.database.db import db_setup
from src.services.vk import get_vk_broadcaster
from src.utils.logging import logging_setup

bot = Bot(token=TG_BOT_TOKEN, parse_mode=types.ParseMode.HTML, validate_token=True)
storage = RedisStorage2(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB_FSM)
vk_scheduler = get_vk_broadcaster(f"redis://{REDIS_HOST}:{REDIS_PORT}", VK_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
runner = Executor(dp, skip_updates=True)


def run_bot():
    logging_setup()
    db_setup(runner)
    middlewares_setup(dp)
    filters_setup(dp)
    # noinspection PyUnresolvedReferences
    import src.handlers

    if DEBUG:
        runner.start_polling()
