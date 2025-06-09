import json
import psycopg2
from pytgbot import Bot
from pytgbot.api_types import as_array
from pytgbot.api_types.sendable.reply_markup import ForceReply, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from pytgbot.api_types.receivable.updates import Message
from pytgbot.api_types.receivable.media import PhotoSize
from some import API_KEY, pgdb, pguser, pgpswd, pghost, pgport, pgschema, url_e, url_c, log_e, pass_e, managers_chats_id, service_chats_id
import requests
import timeit
import uuid
from io import BytesIO
import os
import sys
import cv2
import pprint
photo_cache = {}  # stores the images.
bot = Bot(API_KEY)
from base64 import b64encode
import time

import string
import random

from DictObject import DictObject
import datetime

from luckydonaldUtils.encoding import to_binary as b, to_native as n
from luckydonaldUtils.exceptions import assert_type_or_raise

pp = pprint.PrettyPrinter(indent=4)
pp0 = pprint.PrettyPrinter(width=41, compact=True)
AppId = 14
#посмотри стаусы в аппке
dafStatus = 34
tenant = 'domotel'
domen = 'https://'+tenant+'-admin.mobsted.ru'

errorRegistration = '''ваш аккаунт не зарегиcтрирован в нашей системе, напишите сюда, пожалуйста, следующие данные:
- номер вашй машины в формате а123ааХХ
- номер вашей карты мойки (написан на карте Пит Стоп)
- ваш номер мобильного телефона
- ваше имя
- ваш email 

или пройдите регистрацию у нашего менеджера в оффисе по адресу г. Тюмень, ул. Хохрякова 44, оффис ДомОтель'''

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
                    limit = 1
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
                    limit = 1
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



           
def selCommentsFromBase():
    limit = 100
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
                    # limit = 100 #, \"\", \"\", \"\", \"\", \"\", \"\"
                    sql = " select comments.\"id\",\"CommentText\", \"ActionName\", \"chat_id\" from comments LEFT JOIN backend ON comments.\"LinkId\" = backend.id   LEFT JOIN objects ON objects.id = backend.\"ObjectId\" where  \"Delivered\" is null and \"chat_id\" is not null order by comments.id asc limit "+str(limit)  # coock_str is not null and
                    # params={"name":name}
                    # curpg.execute(sql,params)
                    curpg.execute(sql)
                    res1 = curpg.fetchall()
                    return res1
        return False
    except psycopg2.DatabaseError as e:
        print('Error %s' % e)




           
def updateCommentsFromBase(id):
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
                if True:             
                    sql = " update comments set \"DeliveredDate\" =  now() , \"Delivered\" = 1 where  \"id\" = %(tagnick)s   "
                    params={"tagnick":id}
                    curpg.execute(sql,params)
                    conpg.commit()
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
                    sql = " select "+str(field)+" as str from objects where  \"Enabled\" = 1 and \"chat_id\" = '"+str(name)+"'  limit "+str(limit)  # coock_str is not null and
                    # params={"name":name}
                    # curpg.execute(sql,params)
                    curpg.execute(sql)
                    res1 = curpg.fetchall()
                    return res1
        return False
    except psycopg2.DatabaseError as e:
        print('Error %s' % e)



         
def insertFile(Name,FileName,LinkId,ObjectId,Url,FileSize,Height,Width,Extension):
        
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
                    sql = " insert into files (\"Name\", \"FileName\",\"LinkId\", \"ObjectId\", \"Url\", \"FileSize\", \"Height\", \"Width\", \"Extension\",\"LinksToTable\",\"Backendname\") \
                            values (%(Name)s,%(FileName)s,%(LinkId)s,%(ObjectId)s,%(Url)s,%(FileSize)s,%(Height)s,%(Width)s,%(Extension)s,'Backend','Chat')"
                    params={"Name":Name,"FileName":FileName,"LinkId":LinkId,"ObjectId":ObjectId,"Url":Url,"FileSize":FileSize,"Height":Height,"Width":Width,"Extension":Extension}
                    curpg.execute(sql,params)
                    conpg.commit()
                    print('fixed')
                    return True
                    
    except psycopg2.DatabaseError as e:
        print('Error %s' % e)




def get_file(file_url, filePath, as_png=True):
    r = requests.get(file_url)
    if r.status_code != 200:
        logger.error("Download returned: {}".format(r.content))
        return None
    # end if
    
    with open(filePath, mode="wb") as file:
        file.write(r.content)
    
    fake_input = BytesIO(r.content)
    if not as_png:
        return fake_input
    # end if
    from PIL import Image  # pip install Pillow
    im = Image.open(fake_input)
    del fake_input
    fake_output = BytesIO()
    im.save(fake_output, "PNG")
    del im
    fake_output.seek(0)
    return fake_output
# end def

def iterm_show_file(filename, data=None, inline=True, width="auto", height="auto", preserve_aspect_ratio=True):
    """

    https://iterm2.com/documentation-images.html
    
    :param filename: 
    :param data: 
    :param inline: 
    :param width:  
    :param height: 
    :param preserve_aspect_ratio: 
    
    Size:
        - N   (Number only): N character cells.
        - Npx (Number + px): N pixels.
        - N%  (Number + %):  N percent of the session's width or height.
        - auto:              The image's inherent size will be used to determine an appropriate dimension.
    :return: 
    """
    width = str(width) if width is not None else "auto"
    height = str(height) if height is not None else "auto"
    if data is None:
        data = read_file_to_buffer(filename)
    # end if
    data_bytes = data.getvalue()
    output = "\033]1337;File=" \
             "name={filename};size={size};inline={inline};" \
             "preserveAspectRatio={preserve};width={width};height={height}:{data}\a\n".format(
        filename=n(b64encode(b(filename))), size=len(data_bytes), inline=1 if inline else 0,
        width=width, height=height, preserve=1 if preserve_aspect_ratio else 0,
        data=n(b64encode(data_bytes)),
    )
    #sys.stdout.write(output)
    return output
# end if


def process_file( file, caption, pathsFiles, file_type="file", as_png=False, inline=True, height=None):
    file_object = bot.get_file(file.file_id)
    file_url = bot.get_download_url(file_object)
    print('file_url',file_url)
    
    N = 12
    tmpName = ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))
    file_ext0 = file_url.split(".")[-1]
    tmpName = tmpName+'.'+file_ext0
    time = datetime.datetime.now()
    str_time=time.strftime("/%Y/%m/%d/")
    filePath = '/home/per_server/tenants/www/tenants/'+tenant+'/uploads'+str_time

    try:
        os.makedirs(filePath, exist_ok=True)
    except KeyError as e:
        print(' over KeyError 42 ' + str(e))
        return False
        
    filePath += tmpName
    
    file_content = get_file(file_url, filePath=filePath, as_png=as_png)
    
    print('filePath ',filePath)
    pathsFiles.append(filePath)
    
    file_name = file_url.split("/")[-1]
    if as_png:
        file_name = file_name + ".png"
    # end if
    save_file_name = str(file.file_id) + "__" + file_name
    return "[{type} {file_id}]\n{image}\n{caption}\n{file_name}".format(
        file_id=file.file_id, caption=(" " + caption if caption else ""),
        image=iterm_show_file(save_file_name, data=file_content, inline=inline, height=height),
        type=file_type, file_name=save_file_name
    )
# end def

def printf(format, *args):
    sys.stdout.write(format % args)
    
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
                print(' ')
                print(' ')
                pp0.pprint(update)
                
                if(update.callback_query)and(update.callback_query.message)and(update.callback_query.message.chat)and(update.callback_query.message.chat.id):
                    # print('update.callback_query.message.chat.id', update.callback_query.message.chat.id)
                    text_message = update.callback_query.message.text
                    chat_id = update.callback_query.message.chat.id
                #
                #if it inline button reaction process intine button actions
                if update.callback_query:
                    # callback_query.message is the original message the bot sent
                        if(not chat_id):
                            continue
                        
                        peer_id, current_image, do_submit = update.callback_query.data.split(";")
                        peer_id, current_image = int(peer_id), int(current_image)  # str -> int
                        do_submit = do_submit == "True"  # str -> bool
                        photos = cache_peer_images(peer_id)
                        result_image, markup = generate_page(current_image, peer_id, photos)
                        assert isinstance(result_image, PhotoSize)
                        
                        try:
                            if do_submit:
                                #bot.answer_callback_query(update.callback_query.id, text="Sending photo...")#description='Bad Request: query is too old and response timeout expired or query ID is invalid
                                result = bot.send_message(chat_id, "отправьте ваше фото пожалуйста, принимаются только фотографии сделанные в текуще месяце")
                                
                                # result = bot.send_photo(chat_id=chat_id, photo=result_image.file_id)
                                
                            else:
                                #bot.answer_callback_query(update.callback_query.id, text="Sending query...")#description='Bad Request: query is too old and response timeout expired or query ID is invalid
                                result = bot.send_message(chat_id, "напишите ваш вопрос, он будет передан нашему менеджеру, который свяжется с вам для разъяснения ситуации")
                        except KeyError as e:
                            print(' over KeyError  ' + str(e))  
                             
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
                        print('результат отправки ответа на реакцию кнопки',result)
                        continue
                    # end if


                if not update.message:
                    continue
                
                msg = update.message
                
                if(msg)and(msg.chat)and(msg.chat.id):
                    # print('update msg.chat.id', msg.chat.id)
                    text_message = msg.text
                    chat_id = msg.chat.id
       
       
                #check user
                fio = selByChatIdFromBase(chat_id, 'fio')
                if not fio:
                    #проверить телефон или пин
                    if text_message:
                        fio = selByPinFromBase(text_message,chat_id)
                        if fio:
                            bot.send_message(chat_id, "добро пожаловать в систему для получения бонусов Дом Отель, "+str(fio[0]))
                        else:
                            #отказать    
                            bot.send_message(chat_id, errorRegistration)
                            for chat in service_chats_id: 
                                bot.send_message(chat, "--> !!!незарегистрированный пользователь ("+text_message+") написал '"+text_message+"'" )
                            continue

                if not fio:
                   print('!!!!!!!!!!!!-------------------- bad thing for chat:',chat_id)
                   continue 
               
                
                ObjectId = selByChatIdFromBase(chat_id, 'id')
                # print('user:',ObjectId,',',fio)
                fio = (fio[0][0])
                ObjectId = (ObjectId[0][0])
                print('!user:',ObjectId,',',fio)
                
                
                
                
                
                
                #
                #process media content
                pathsFiles = []
                if "photo" in msg:
                    print('------------photo', msg.chat.id)
                    photo = msg.photo[0]
                    for p in msg.photo[1:]:
                        if p.file_size > photo.file_size:
                            photo = p
                        # end if
                    # end for
                    result01 = process_file(photo, msg.caption, pathsFiles, file_type="photo", height="10")
                    if not result01:
                        return False
                    print('результат отправки ответа на картинку:',result01)
                    text_message = msg.caption
                if "sticker" in msg:
                    print('-------------sticker', msg.chat.id)
                    result0 = process_file(msg.sticker, msg.caption, pathsFiles, file_type="sticker", as_png=True, height="10")
                    if not result01:
                        return False
                    print('результат отправки ответа на стиккер:',result0)
                    text_message = msg.caption
                
                

                #
                # get other information for our interaction
                if update.message:
                    origin, peer_id = get_sender_infos(update.message)
                    current_image = 0
                    photos = cache_peer_images(peer_id, force=True)
                    
                    
                #
                # if it same command
                if not update.message or not update.message.entities:
                    pass
                else:
                    for entity in update.message.entities:
                        
                        # MessageEntity
                        print('-------')
                        print('тип сообщения - entity.type:',entity.type)
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
                    
                skipSendButtons = False
                
                if(text_message):
                  countWords = len(text_message.split())
                  if text_message[-1] =='?':
                    esult2 = bot.send_message(chat_id, "в ближайшее время наш сотруник с вами свяжется для ответа на ваш вопрос")
                    skipSendButtons = True
                  else:
                    if countWords>1:
                        result2 = bot.send_message(chat_id, "в ближайшее время мы обработаем ваше сообщение, дополните его, если это необходимо для прояснения ситуции")
                        skipSendButtons = True
                  
                        

                #
                #send inline buttons
                if not skipSendButtons:
                    if((len(pathsFiles)==0)):
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
                        result2 = bot.send_msg(chat_id, "что вам необходимо сделать?", reply_markup=markup)
                        
                        #print('результат отправки ответа на тектовое сообщение',result2)
                        
                    else:
                        result2 = bot.send_message(chat_id, "спасибо, в ближайщее время мы обработаем полученные данные, средства на карту зачисляются 1го и 15го числа месяца")
                
                
                eventcreated = False
                
                #
                #save event
                print('------- pathsFiles',pathsFiles)
                if(ObjectId>0 and (text_message or (len(pathsFiles)>0))):
                    eventcreated = createEvent(text_message, ObjectId, pathsFiles)
                
                #managers_chats_id, service_chats_id
                if True:
                  if eventcreated:
                    for chat in managers_chats_id:
                        if text_message:
                            messageformanager = "--> сообщение от " + str(fio) + ': ' + '\"'+text_message+'\"'
                            bot.send_message(chat, messageformanager)
                        if len(pathsFiles)>0:
                            messageformanager = "--> фото от "+str(fio)
                            bot.send_message(chat, messageformanager)

                            
                if not eventcreated:
                    bot.send_message(chat_id, "что-то не так, ваше сообщение недоставлено, повторите отправку через некоторое время или свяжитесь с нами по телефону указанному на сайте https://домотель.рф/#contacts")
                    #managers_chats_id, service_chats_id
                    for chat in service_chats_id: 
                        bot.send_message(chat, "--> !!!ошибка создания эвента!!!")
                        
                    # # MessageEntity
                    # if entity.type == "bot_command":
                    #     command = text_message[entity.offset:entity.offset+entity.length]
                    #     if command == "/key":
                    #         do_keyboard(chat_id)
                    #     elif command == "/unkey":
                    #         hide_keyboard(chat_id)
                    #     # end if


            time.sleep(0.2)
            comments = selCommentsFromBase()
            if comments:
              if len(comments)>0:
                for comment in comments:
                    print(comment)
                    chat_id = comment[3]
                    id_comment = comment[0]
                    text_comment = comment[1]
                    result9 = False
                    try:
                        result9 = bot.send_message(chat_id, text_comment)
                        print('результат отправки комментария',result9)
                    except KeyError as e:
                                print(' over KeyError  ' + str(e))
                    time.sleep(0.2)
                    if(result9):
                        updateCommentsFromBase(id_comment)
        
        except KeyError as e:
            print(' over KeyError  ' + str(e))

            # end for
        # end for update
    # end while forever
# end def main



def createEvent(textm,objid, pathsFiles = []):
    if(not(objid>0)):
        return False
    
    PARAMS = {'login':log_e,'password':pass_e}
    r = requests.get(url = url_e, params = PARAMS)
    
    if r.status_code != 200:
        return False
    
    data = r.json()
    
    if not 'access_token' in data:
        return False
    
    try:
        access_token = data['access_token']
        refresh_token = data['refresh_token']
        # print(data,access_token,refresh_token)
    except KeyError as e:
        print(' over KeyError 43 ' + str(e))
        return False

    
    Headers = { 'Authorization' : "Bearer "+str(access_token) }
    PARAMS = {'ApplicationId':AppId,
                # 'Value':'{"source":"Telegram"' + ((',"text":"'+str(textm)+'"') if textm else '') + '}', #,"type":"text"
                'Value':'{' + (('"&nbsp;":"'+str(textm)+'"') if textm else '"&nbsp;":"_фото_"') + '}', #,"type":"text"
                'ObjectId':objid,
                'ActionName':'Chat',
                'StatusId':dafStatus}
    # print('PARAMS',PARAMS)
    r = requests.post(url = url_c, json = PARAMS, data = PARAMS, headers=Headers)
    if r.status_code != 200:
        return False
    data = r.json()

    if not 'meta' in data:
        return False
    if not 'data' in data:
        return False
    
    try:
        eventId = data['data'][0]['id']
    except KeyError as e:
        print(' over KeyError 45  ' + str(e))
        return False

    if len(pathsFiles)>0:
        for x in pathsFiles:
            try:
                file_size = os.path.getsize(x)
                print(f"File Size in Bytes is {file_size}")
            except FileNotFoundError:
                print("File not found.1",x)
                return False
            except OSError:
                print("OS error occurred.")
                return False
            except Exception as e:
                print('read file exception 0 - ',e)
                return False
                
            try:
                im = cv2.imread(x)
                h, w, c = im.shape
                print('width:  ', w)
                print('height: ', h)
                print('channel:', c)
            except FileNotFoundError:
                print("File not found.0",x)
                return False
            except Exception as e:
                print('read file exception 1 - ',e)
                return False
                
            Name = (x.replace("/home/per_server/tenants/www",""))
            FileName = x.split("/")[-1]
            LinkId = eventId
            ObjectId = objid
            Url = domen + Name
            print('Url',Url)
            FileSize = file_size
            Height = w
            Width = h
            Extension = x.split(".")[-1]
  
            res = insertFile(Name=Name,FileName=FileName,LinkId=LinkId,ObjectId=ObjectId,Url=Url,FileSize=FileSize,Height=Height,Width=Width,Extension=Extension)
            if not res:
                return False
            
    #if all process good
    return True

    #start adding file



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
