from pytgbot import Bot
import logging
logger = logging.getLogger(__name__)

from some import API_KEY  
bot = Bot(API_KEY)


my_info=bot.get_me()
print("Information about myself: {info}".format(info=my_info))
last_update_id = 0

while True:
    # loop forever.
    for update in bot.get_updates(limit=100, offset=last_update_id+1):
        last_update_id = update.update_id
        print(update)
        if update.message and update.message.text:  # we have a text message.
            if update.message.chat:  # is a group chat
                sender = update.message.chat.id
            else:  # user chat
                sender = update.message.from_peer.id

