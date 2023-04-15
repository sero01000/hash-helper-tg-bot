import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from settings import API_TOKEN
from funcs import *

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start', 'help'])
@dp.throttled(rate=2)
async def send_welcome(message: types.Message):
    await message.reply("This bot detect hashes.\n\
Commands:/h, /hash.\n\
Usage example: /hash a6105c0a611b41b08f1209506350279e\n\
hash a6105c0a611b41b08f1209506350279e\nOr send me hash in private message or by inline.")


@dp.message_handler(commands=['hash', 'h'])
@dp.throttled(rate=2)
async def hash_detect(message: types.Message):
    words = prepare_text(message.get_args())
    words_to_check = prepare_words(words)
    answer = prepare_detect(words_to_check)

    if answer == "":
        await message.reply("Cant detect hash")
    else:
        await message.reply(answer)


@dp.message_handler(chat_type=[types.ChatType.PRIVATE])
@dp.throttled(rate=3)
async def group_handler(message: types.Message):
    words = prepare_text(message.text)
    words_to_check = prepare_words(words)
    answer = prepare_detect(words_to_check)

    if answer == "":
        await message.reply("Cant detect hash...")
    else:
        await message.reply(answer)


@dp.message_handler(regexp='hash |хэш | hash| хэш', chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
@dp.throttled(rate=3)
async def tt_download2(message: types.Message):
    words = prepare_text(message.text)
    words_to_check = prepare_words(words)
    answer = prepare_detect(words_to_check)

    if answer == "":
        await message.reply("I hear 'hash' word, but cant find hash.")
    else:
        await message.reply(answer)


@dp.throttled(rate=3)
@dp.inline_handler()
async def inline_echo(inline_query: types.InlineQuery):

    text = inline_query.query or None
    if text != None:
        words = prepare_text(text)
        words_to_check = prepare_words(words)
        answer = prepare_detect(words_to_check)
        if answer == "":
            img = "https://cdn-icons-png.flaticon.com/512/5253/5253543.png"
            result = prepare_querry("Not found", "Cant find hash", img)
        else:
            img = "https://cdn-icons-png.flaticon.com/512/5253/5253963.png"
            result = prepare_querry("Found", answer, img)
        # , cache_time=1
        await bot.answer_inline_query(inline_query.id, results=[result])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
