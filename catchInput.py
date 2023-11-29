import json
import psycopg2
from pytgbot import Bot
from pytgbot.api_types import as_array
from pytgbot.api_types.sendable.reply_markup import ForceReply, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from pytgbot.api_types.receivable.updates import Message
from pytgbot.api_types.receivable.media import PhotoSize
from some import API_KEY, pgdb, pguser, pgpswd, pghost, pgport, pgschema, url_e, url_c, log_e, pass_e
import requests
import timeit
import uuid



photo_cache = {}  # stores the images.
bot = Bot(API_KEY)




AppId = 14

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
                    
                    if True:             
                        sql = " update objects set \"chat_id\" = %(tagnick)s , \"PIN\" = null where  \"PIN\" = '"+str(name)+"' and  \"chat_id\" is null and  \"PIN\" <> '' and  \"PIN\" is not null  "
                        params={"name":name,"tagnick":tagnick}
                        curpg.execute(sql,params)
                        conpg.commit()
                        
                        # sql = " update targets set \"status\" = %(tagnick)s where   \"PIN\" = '"+str(name)+"' and  \"chat_id\" is null and  \"PIN\" <> '' and  \"PIN\" is not null  "
                        # params={"name":name,"tagnick":tagnick}
                        # curpg.execute(sql,params)
                        # conpg.commit()
                    
                    print('fixed')
                    
                    return res1
        return False
    except psycopg2.DatabaseError as e:
        print('Error %s' % e)



           
def selByChatIdFromBase(name, field):
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
                    limit = 1
                    sql = " select '"+str(field)+"' as str from objects where  \"Enabled\" = 1 and \"chat_id\" = '"+str(name)+"'  limit "+str(limit)  # coock_str is not null and
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
                ObjectId = 0
                #get chat and text
                chat_id = False
                text_message = False
                print(update)
                if(update.callback_query)and(update.callback_query.message)and(update.callback_query.message.chat)and(update.callback_query.message.chat.id):
                    print('update.callback_query.message.chat.id', update.callback_query.message.chat.id)
                    text_message = update.callback_query.message.text
                    chat_id = update.callback_query.message.chat.id
                if(update.message)and(update.message.chat)and(update.message.chat.id):
                    print('update update.message.chat.id', update.message.chat.id)
                    text_message = update.message.text
                    chat_id = update.message.chat.id
                    
                #check user
                fio = selByChatIdFromBase(chat_id, 'fio')
                if not fio:
                    #проверить телефон или пин
                    if text_message:
                        fio = selByPinFromBase(text_message,chat_id)
                        if fio:
                            bot.send_message(chat_id, "добро пожаловать в систему для получения бонусов Дом Отель, "+str(fio[0]))
                            ObjectId = selByChatIdFromBase(chat_id, 'id')
                        else:
                            #отказать    
                            bot.send_message(chat_id, "ваш аккаунт не зарегиcтрирован в нашей системе, получите регистрационный код у нашего менеджера")
                            continue
                
                #if it inline button reaction 
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
                            result = bot.send_message(chat_id, "отправьте ваше фото пожалуйста, принимаются только фотографии сделанные в текуще месяце")
                            
                            # result = bot.send_photo(chat_id=chat_id, photo=result_image.file_id)
                            
                        else:
                            bot.answer_callback_query(update.callback_query.id, text="Sending query...")
                            result = bot.send_message(chat_id, "напишите ваш вопрос, он будет передан нашему менеджеру, который свяжется с вам для разъяснения ситуации")
                            
                            # result = bot.edit_message_text(
                            #     "Profile pic {num}\n{w}x{h}, {size}B".format(
                            #         num=current_image, w=result_image.width, h=result_image.height, size=result_image.file_size
                            #     ),
                            #     chat_id=chat_id,
                            #     message_id=update.callback_query.message.message_id,
                            #     disable_web_page_preview=False,
                            #     reply_markup=markup
                            # )
                            
                            
                        # end if
                        print(result)
                        continue
                    # end if

                    
                # get other information for our interaction
                if update.message:
                    origin, peer_id = get_sender_infos(update.message)
                    current_image = 0
                    photos = cache_peer_images(peer_id, force=True)
                    
                    
                # if it same command
                if not update.message or not update.message.entities:
                    pass
                else:
                    for entity in update.message.entities:
                        
                        # MessageEntity
                        print('-------')
                        print('entity.type',entity.type)
                        print('-------')
                        
                        if entity.type == "bot_command":
                            command = text_message[entity.offset:entity.offset+entity.length]
                            print('command:',command)
                            if command == "отправить фото" or command == "/1":
                                bot.send_message(chat_id, "отправьте фото пожалуйста")
                                continue
                            elif command == "задать вопрос" or command == "/2":
                                bot.send_message(chat_id, "ваш вопрос будет отпарвлен нашему менеджеру")
                                continue
                            elif  command == "/unkey":
                                hide_keyboard(chat_id)
                            elif command == "/start":
                                do_keyboard(chat_id)
                        

                #send inline buttons
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
                print(bot.send_msg(chat_id, "что вам необходимо сделать?", reply_markup=markup))
                    

                createEvent(text_message, ObjectId)

                    # # MessageEntity
                    # if entity.type == "bot_command":
                    #     command = text_message[entity.offset:entity.offset+entity.length]
                    #     if command == "/key":
                    #         do_keyboard(chat_id)
                    #     elif command == "/unkey":
                    #         hide_keyboard(chat_id)
                    #     # end if

        except KeyError as e:
            print(' over KeyError  ' + str(e))

            # end for
        # end for update
    # end while forever
# end def main



def createEvent(textm,objid):
    PARAMS = {'login':log_e,'password':pass_e}
    r = requests.get(url = url_e, params = PARAMS)
    data = r.json()

    access_token = data['access_token']
    refresh_token = data['refresh_token']
    print(data,access_token,refresh_token)
    
    if(objid>0):
        PARAMS = {'ApplicationId':AppId,
                    'Value':'{"test":"test"}',
                    'ObjectId':objid,
                    'ActionName':'Chat',
                    'StatusId':1}
        r = requests.post(url = url_c, params = PARAMS)
        data = r.json()




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
