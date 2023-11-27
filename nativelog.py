from luckydonaldUtils.logger import logging
from pytgbot import Bot
from pytgbot.api_types.receivable import Result
from pytgbot.api_types.receivable.updates import Update


from some import API_KEY 

logger = logging.getLogger(__name__)


def main():
    logging.add_colored_handler(level=logging.DEBUG)
    # get you bot instance.
    bot = Bot(API_KEY, return_python_objects=True)
    print(bot.get_me())

    # do the update loop.
    last_update_id = 0
    while True:  # loop forever.
        updates = bot.get_updates(limit=100, offset=last_update_id + 1)
        for update in updates:  # for every new update
            last_update_id = update.update_id
            print(update)
            result = update.to_array()
            assert isinstance(result, dict)
            print(result)
        # end for
    # end while
# end def


if __name__ == '__main__':
    main()
