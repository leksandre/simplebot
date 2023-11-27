import json

from pytgbot import Bot
from pytgbot.api_types import as_array
from pytgbot.api_types.sendable.reply_markup import ForceReply, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from pytgbot.api_types.receivable.updates import Message
from pytgbot.api_types.receivable.media import PhotoSize
from some import API_KEY
photo_cache = {}  # stores the images.
bot = Bot(API_KEY)

def main():
    my_info=bot.get_me()
    print("Information about myself: {info}".format(info=my_info))
    last_update_id = -1
    while True:
        for update in bot.get_updates(limit=1, offset=last_update_id+1):
            last_update_id = update.update_id
            print(update)
            
            if update.callback_query:
                  # callback_query.message is the original message the bot sent
                    peer_id, current_image, do_submit = update.callback_query.data.split(";")
                    peer_id, current_image = int(peer_id), int(current_image)  # str -> int
                    do_submit = do_submit == "True"  # str -> bool
                    photos = cache_peer_images(peer_id)
                    result_image, markup = generate_page(current_image, peer_id, photos)
                    assert isinstance(result_image, PhotoSize)
                    if do_submit:
                        bot.answer_callback_query(update.callback_query.id, text="Sending photo...")
                        bot.send_message(update.message.chat.id, "отправьте фото пожалуйста")
                        
                        # result = bot.send_photo(chat_id=update.callback_query.message.chat.id, photo=result_image.file_id)
                        
                    else:
                        bot.answer_callback_query(update.callback_query.id, text="Sending query...")
                        bot.send_message(update.message.chat.id, "ваш вопрос будет отпарвлен нашему менеджеру")
                        
                        # result = bot.edit_message_text(
                        #     "Profile pic {num}\n{w}x{h}, {size}B".format(
                        #         num=current_image, w=result_image.width, h=result_image.height, size=result_image.file_size
                        #     ),
                        #     chat_id=update.callback_query.message.chat.id,
                        #     message_id=update.callback_query.message.message_id,
                        #     disable_web_page_preview=False,
                        #     reply_markup=markup
                        # )
                        
                        
                    # end if
                    print(result)
                # end if
                
            if not update.message or not update.message.entities:
                continue
            
            
            for entity in update.message.entities:
                
                origin, peer_id = get_sender_infos(update.message)
                current_image = 0
                photos = cache_peer_images(peer_id, force=True)
                
                # MessageEntity
                print('-------')
                print('entity.type',entity.type)
                print('-------')
                
                
                if entity.type == "bot_command":
                    command = update.message.text[entity.offset:entity.offset+entity.length]
                    print('command:',command)
                    if command == "отправить фото" or command == "/1":
                        bot.send_message(update.message.chat.id, "отправьте фото пожалуйста")
                    elif command == "задать вопрос" or command == "/2":
                        bot.send_message(update.message.chat.id, "ваш вопрос будет отпарвлен нашему менеджеру")
                    elif  command == "/unkey":
                        hide_keyboard(update.message.chat.id)
                    elif command == "/start":
                        do_keyboard(update.message.chat.id)
                


                        buttons = [[],[]]  # 2 rows
                        buttons[0].append(InlineKeyboardButton(
                            "отправить фото", callback_data="{peer_id};{curr_pos};True".format(peer_id=peer_id, curr_pos=current_image)
                            # "/1 отправить фото", callback_data="/1 отправить_фото"
                        ))
                        buttons[1].append(InlineKeyboardButton(
                            "задать вопрос", callback_data="{peer_id};{curr_pos};False".format(peer_id=peer_id, curr_pos=current_image)
                            # "/2 задать вопрос", callback_data="/2 задать_вопрос"
                        ))
                        markup = InlineKeyboardMarkup(buttons)
            
                        print(bot.send_msg(update.message.chat.id, "что вам необходимо сделать?", reply_markup=markup))
                



                # # MessageEntity
                # if entity.type == "bot_command":
                #     command = update.message.text[entity.offset:entity.offset+entity.length]
                #     if command == "/key":
                #         do_keyboard(update.message.chat.id)
                #     elif command == "/unkey":
                #         hide_keyboard(update.message.chat.id)
                #     # end if



            # end for
        # end for update
    # end while forever
# end def main

# noinspection PyTypeChecker
def generate_page(current_image, peer_id, photos):
    buttons = [[], []]  # 2 rows
    # first button row
    if current_image > 0:
        buttons[0].append(InlineKeyboardButton(
            "<<", callback_data="{peer_id};{next_pos};False".format(peer_id=peer_id, next_pos=current_image-1)
        ))
    # end if
    if current_image < len(photos)-1:
        buttons[0].append(InlineKeyboardButton(
            ">>", callback_data="{peer_id};{next_pos};False".format(peer_id=peer_id, next_pos=current_image + 1)
        ))
    # end if
    # second button row
    buttons[1].append(InlineKeyboardButton(
        "send", callback_data="{peer_id};{curr_pos};True".format(peer_id=peer_id, curr_pos=current_image)
    ))
    markup = InlineKeyboardMarkup(buttons)
    result_image = photo_cache[peer_id][current_image]
    return result_image, markup

def cache_peer_images(peer_id, force=False):
    if not force and peer_id in photo_cache:
        return photo_cache[peer_id]
    photos = bot.get_user_profile_photos(peer_id).photos
    photo_cache[peer_id] = []
    for photo in photos:
        photo_cache[peer_id].append(
            max(photo, key=lambda p: p.file_size)  # get the biggest image.
        )
    return photos
# end def


def get_sender_infos(message):
    assert isinstance(message, Message)
    peer_id = message.from_peer.id
    origin = message.chat.id if message.chat else message.from_peer.id
    return origin, peer_id


def do_keyboard(chat_id):
    buttons = [
        ["/1 отправить фото", "/2 задать вопрос"],
      #  ["/key", "/unkey"],
      #  [KeyboardButton("Contact?", request_contact=True), KeyboardButton("Location?", request_location=True)],
    ]
    markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    print(bot.send_msg(chat_id, "добро пожаловать, ", reply_markup=markup))


def hide_keyboard(chat_id):
    print(bot.send_msg(chat_id, "okey, keyboard hidden.", reply_markup=ReplyKeyboardRemove()))
main()
