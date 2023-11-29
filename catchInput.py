import json
import psycopg2
from pytgbot import Bot
from pytgbot.api_types import as_array
from pytgbot.api_types.sendable.reply_markup import ForceReply, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from pytgbot.api_types.receivable.updates import Message
from pytgbot.api_types.receivable.media import PhotoSize
from some import API_KEY, pgdb, pguser, pgpswd, pghost, pgport, pgschema

import timeit
import uuid



photo_cache = {}  # stores the images.
bot = Bot(API_KEY)





           
def selByPhoneFromBase(name):
    limit = 1
    try:
        for x in range(0, 9999):
            try:
                    conpg = psycopg2.connect(database=pgdb, user=pguser, password=pgpswd,
                            host=pghost,port=pgport) # , options=f'-c search_path={pgschema}')
            except Exception as e:
                print('pgbouncer exception 1 - ',e)
                time.sleep(0.2)
                pass
            finally:
                break
        
        if 'conpg' not in locals():
            return False

        if conpg:
         with conpg:
             with conpg.cursor() as curpg:
                sql = " Set search_path =%(pgdb)s "
                params={"pgdb":pgdb}
                curpg.execute(sql,params)
                conpg.commit()

        if conpg:
         with conpg:
             with conpg.cursor() as curpg:
                    limit = 7
                    sql = " select fio as str from objects where  \"Phone\" = '"+str(name)+"'  limit "+str(limit)  # coock_str is not null and
                    # params={"name":name}
                    # curpg.execute(sql,params)
                    curpg.execute(sql)
                    res1 = curpg.fetchall()
                    return res1
        return False
    except psycopg2.DatabaseError as e:
        print('Error %s' % e)


           
def selByPinFromBase(name,tagnick):
    name = name.strip()
    limit = 1
    try:
        for x in range(0, 9999):
            try:
                    conpg = psycopg2.connect(database=pgdb, user=pguser, password=pgpswd,
                            host=pghost,port=pgport) # , options=f'-c search_path={pgschema}')
            except Exception as e:
                print('pgbouncer exception 1 - ',e)
                time.sleep(0.2)
                pass
            finally:
                break
        
        if 'conpg' not in locals():
            return False

        if conpg:
         with conpg:
             with conpg.cursor() as curpg:
                sql = " Set search_path =%(pgdb)s "
                params={"pgdb":pgdb}
                curpg.execute(sql,params)
                conpg.commit()

        if conpg:
         with conpg:
             with conpg.cursor() as curpg:
                    limit = 7
                    sql = " select fio as str from objects where  \"PIN\" = '"+str(name)+"' and  \"chat_id\" is null and  \"PIN\" <> '' and  \"PIN\" is not null  limit "+str(limit)  # coock_str is not null and
                    # params={"name":name}
                    # curpg.execute(sql,params)
                    curpg.execute(sql)
                    res1 = curpg.fetchone()
                    
                    
                    # sql = " update objects set \"chat_id\" = %(tagnick)s , \"PIN\" = null where  \"PIN\" = '"+str(name)+"' and  \"chat_id\" is null and  \"PIN\" <> '' and  \"PIN\" is not null  "
                    # params={"name":name,"tagnick":tagnick}
                    # curpg.execute(sql,params)
                    # conpg.commit()
                    
                    # sql = " update targets set \"status\" = %(tagnick)s where   \"PIN\" = '"+str(name)+"' and  \"chat_id\" is null and  \"PIN\" <> '' and  \"PIN\" is not null  "
                    # params={"name":name,"tagnick":tagnick}
                    # curpg.execute(sql,params)
                    # conpg.commit()
                    
                    print('fixed')
                    
                    return res1
        return False
    except psycopg2.DatabaseError as e:
        print('Error %s' % e)



           
def selByChatIdFromBase(name):
    limit = 1
    try:
        for x in range(0, 9999):
            try:
                    conpg = psycopg2.connect(database=pgdb, user=pguser, password=pgpswd,
                            host=pghost,port=pgport) # , options=f'-c search_path={pgschema}')
            except Exception as e:
                print('pgbouncer exception 1 - ',e)
                time.sleep(0.2)
                pass
            finally:
                break
        
        if 'conpg' not in locals():
            return False

        if conpg:
         with conpg:
             with conpg.cursor() as curpg:
                sql = " Set search_path =%(pgdb)s "
                params={"pgdb":pgdb}
                curpg.execute(sql,params)
                conpg.commit()

        if conpg:
         with conpg:
             with conpg.cursor() as curpg:
                    limit = 7
                    sql = " select fio as str from objects where  \"chat_id\" = '"+str(name)+"'  limit "+str(limit)  # coock_str is not null and
                    # params={"name":name}
                    # curpg.execute(sql,params)
                    curpg.execute(sql)
                    res1 = curpg.fetchall()
                    return res1
        return False
    except psycopg2.DatabaseError as e:
        print('Error %s' % e)


def main():
    my_info=bot.get_me()
    print("Information about myself: {info}".format(info=my_info))
    last_update_id = -1
    while True:
        try:
            for update in bot.get_updates(limit=1, offset=last_update_id+1):
                last_update_id = update.update_id
                origin, peer_id = get_sender_infos(update.message)
                current_image = 0
                photos = cache_peer_images(peer_id, force=True)
                        
                print(update)
                print('update update.message.chat.id', update.message.chat.id)
                fio = selByChatIdFromBase(update.message.chat.id)
                if not fio:
                    #проверить телефон или пин
                    if update.message.text:
                        fio = selByPinFromBase(update.message.text,update.message.chat.id)
                        if fio:
                            bot.send_message(update.message.chat.id, "добро пожаловать в систему для получения бонусов Дом Отель, "+str(fio[0]))
                        else:
                            #отказать    
                            bot.send_message(update.message.chat.id, "ваш аккаунт не зарегиcтрирован в нашей системе, получите регистрационный код у нашего менеджера")
                            continue
                
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
                            result = bot.send_message(update.callback_query.message.chat.id, "отправьте фото пожалуйста")
                            
                            # result = bot.send_photo(chat_id=update.callback_query.message.chat.id, photo=result_image.file_id)
                            
                        else:
                            bot.answer_callback_query(update.callback_query.id, text="Sending query...")
                            result = bot.send_message(update.callback_query.message.chat.id, "ваш вопрос будет отпарвлен нашему менеджеру")
                            
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
                    pass
                else:
                    for entity in update.message.entities:
                        
                        
                      
                        
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

        except KeyError as e:
            print(' over KeyError  ' + str(e))

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
