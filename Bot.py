import random,os,json,asyncio
from telebot.async_telebot import AsyncTeleBot,types  
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait ,BadRequest ,NotAcceptable,Unauthorized,SessionPasswordNeeded, PhoneCodeInvalid, PasswordHashInvalid
from pyrogram import Client


# coinfig class
class Coinfig:
    API_KEY = "6383407760:AAEIXIc5wf9SRJkRaUfM0CFb7yaD81Vn34o"

# chack json file sessions 
if os.path.exists(r"data/Sessions.json") == False:
    os.mkdir('data')
    with open('data/Sessions.json' ,'w') as JSObj:
        json.dump({'sessions':{}}, JSObj)


# Start Bot telebot
bot = AsyncTeleBot(Coinfig.API_KEY)

# lists and value 
temp_handler = {}

Status = {'get_message':False}

add_acconet_stat = {
    'API_HASH_STATE':False,
    'API_ID_STATE':False,
    'CODE_STATE':False,
    'PHONE_STATE':False,
    'PASSORD_STATE':False
}

reaction_list = ['🔥','🔥','🔥']
ADMINE_STATE = {'add_acconet':False,'add_username':False,'session_id':'session_1'}


# inline keyboards 
def HOME_KEYBOARD():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("• المطور •", callback_data='not'))
    keyboard.add(InlineKeyboardButton("╰ اެضِفِ حِسُاެبُ  ╯", callback_data='add_acconet'), InlineKeyboardButton("╰ اެݪحِسُاެبُاެتِ  ╯", callback_data="show_acconet"))
    keyboard.add(InlineKeyboardButton("• - @viptrt - •", callback_data='not'))
    keyboard.add(InlineKeyboardButton("اެࢪسُاެݪ ࢪسُاެݪهَ ", callback_data='t_send_message'),
    InlineKeyboardButton("اެنِضِمِاެمِ ݪقِنِاެهَ ", callback_data='t_join_chanl'))
    keyboard.add(InlineKeyboardButton(" ࢪشِقِ تِصِۅيُتِ ❤️", callback_data='t_reaction'))
    return keyboard

def BACK_HOME_KEYBOARD():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("•ࢪجَۅعٰ ⌫", callback_data='back_home'))
    return keyboard

def SHOW_ALL_SESSION():
    sessions = session_data.READ_SESSIONS()
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton("𝙄𝘿", callback_data="NOT"),
        InlineKeyboardButton("𝙉𝘼𝙈𝙀", callback_data="NOT"),
        InlineKeyboardButton("𝘿𝙀𝙇𝙀𝙏", callback_data="NOT"))

    if len(sessions['sessions']) != 0:
        for i in sessions['sessions']:
            session = sessions['sessions'][i]
            keyboard.add(
                InlineKeyboardButton(i.split('_')[1], callback_data="NOT"),
                InlineKeyboardButton(session['first_name'], url=f"t.me/{session['username']}"),
                InlineKeyboardButton('𝙳𝙴𝙻𝙴𝚃', callback_data=f"del_ses:{i}"))

        
    elif len(sessions['sessions']) == 0:
        keyboard.add(InlineKeyboardButton("𝙉𝙊 𝘼𝘾𝘾𝙊𝙉𝙀𝙏", callback_data="barck"))

    keyboard.add(InlineKeyboardButton("•BACK ⌫", callback_data="back_home"))
    return keyboard

# message 
MESSAGE_BOT = {'HOME':"Wlcome To The bot Telegram Acconet mange .",
   'SHOW_ACCONET':'The All acconet','SHOW_TOOLS':"Acconets Tools"}



# session databesas 
class Session_databesas:

    def __init__(self):
        self.PAT =   r'data/Sessions.json'

    def ADD_SESSION(self ,api_hash: str ,api_id: str ,phone: str ,seesion_string: str 
        ,first_name: str ,accont_id: str ,username : str ,):
        # open session databesas file 
        with open(self.PAT ,'r') as JSObjRead:
            JSObj = json.load(JSObjRead)
        # session id
        session_id = len(JSObj['sessions'])+1
        # add data
        JSObj['sessions'].update({f'session_{str(session_id)}':{"id":session_id,"api_hash":api_hash ,"api_id":api_id,"phone":phone,'session':seesion_string,'first_name':first_name,'username':username,'accont_id':accont_id}})

        # update Json File
        with open(self.PAT ,'w') as JSObjWireat:
            json.dump(JSObj , JSObjWireat,indent=3)

    def READ_SESSIONS(self ,):
        with open(self.PAT ,'r') as JSObjRead:
            JSObj = json.load(JSObjRead)
        return JSObj

    # get sessions count 
    def GET_SESSION_COUNT(self ,):
            # open session databesas file 
        with open(self.PAT ,'r') as JSObjRead:
            JSObj = json.load(JSObjRead)
        # session id
        session_count = len(JSObj['sessions'])

        return session_count

    def DELET_SESSION(self, session_id: str ,):
        sessions = self.READ_SESSIONS()
        sessions['sessions'].pop(session_id)
        with open(self.PAT ,'w') as JSObjWireat:
            json.dump(sessions , JSObjWireat,indent=3)
    
    def CHACHK_SESSION(self ,API_HASH : str ,API_ID : int ,PHONE : str ,):
        RETUERE = True
        sessions = self.READ_SESSIONS()
        for i in sessions['sessions']:
            if PHONE in sessions['sessions'][i]['phone'] or API_ID == sessions['sessions'][i]['api_id'] or API_HASH ==  sessions['sessions'][i]['api_hash']:
                RETUERE = False
            else : 
                RETUERE = True
        return RETUERE

session_data = Session_databesas() 


# add acconet hndler class
class ADD_SESSION_HANDLER:

    def __init__(self ,call : types.CallbackQuery):
        self.chat_id = call.message.chat.id
        self.message_id = call.message.id
        # states 
        # self.API_HASH_STATE  = False
        # add_acconet_stat['API_ID_STATE']    = False
        # add_acconet_stat['PHONE_STATE']     = False
        # add_acconet_stat['CODE_STATE']      = False
        # add_acconet_stat['PASSORD_STATE']      = False
        # data dict

        self.user_dict = {
            'API_HASH':None,
            'API_ID':None,
            'PHONE_NUMBER':None,
            'CODE_HASH':None,
            'CODE':None,
            'PASSURD':None
            }
     



    # START HANLDER 
    async def START(self, ):
        await bot.edit_message_text(text="ارسل الايبي هاش عزيزي ❤️" ,chat_id=self.chat_id ,
         message_id=self.message_id,reply_markup=BACK_HOME_KEYBOARD())
        add_acconet_stat['API_HASH_STATE'] = True
        await self.API_HASH_HANDLER()
        
    async def API_HASH_HANDLER(self, ): # api_hash hanler
        @bot.message_handler(func=lambda hndler: add_acconet_stat['API_HASH_STATE'] == True and ADMINE_STATE['add_acconet']  == True)
        async def API_HASH_HAND(message):
            self.user_dict['API_HASH'] = message.text
            add_acconet_stat['API_HASH_STATE'] = False
            add_acconet_stat['API_ID_STATE'] = True
            await bot.send_message(text='ارسل الايبي ايدي عزيزي ❤️',chat_id=self.chat_id,reply_markup=BACK_HOME_KEYBOARD())
            await self.API_ID_HANDLER()

    async def API_ID_HANDLER(self, ): # api_id handler
        @bot.message_handler(func=lambda hndler: add_acconet_stat['API_ID_STATE'] == True and ADMINE_STATE['add_acconet']  == True)
        async def API_ID_HAND(message):
            self.user_dict['API_ID'] = message.text
            add_acconet_stat['API_ID_STATE'] = False
            add_acconet_stat['PHONE_STATE'] = True
            await bot.send_message(text='𝙿𝚕𝚎𝚊𝚜𝚎 𝚂𝚎𝚗𝚍 𝙿𝚑𝚘𝚗𝚎 𝙽𝚞𝚖𝚋𝚎𝚛 .',chat_id=self.chat_id,reply_markup=BACK_HOME_KEYBOARD())
            await self.PHONE_NUMBER()

    async def PHONE_NUMBER(self, ): # phone_number 
        @bot.message_handler(func=lambda hndler: add_acconet_stat['PHONE_STATE'] == True and ADMINE_STATE['add_acconet']  == True)
        async def PHONE_NUMBER_HAND(message):
            self.user_dict['PHONE_NUMBER'] = message.text
            message_edit = await bot.send_message(text='𝙿𝚕𝚎𝚊𝚜𝚎 𝚆𝚒𝚝𝚎 𝙲𝚑𝚊𝚌𝚔 𝙸𝚗𝚏𝚘 .',chat_id=self.chat_id)
            try:
                if session_data.CHACHK_SESSION(self.user_dict['API_HASH'],self.user_dict['API_ID'],
                self.user_dict['PHONE_NUMBER']) == True:
                    # chack info from session 
                    self.client = Client('session' ,api_hash=self.user_dict["API_HASH"] ,
                    api_id=self.user_dict['API_ID'] ,in_memory=True) # start client pyrogram
                    # connect client 
                    await self.client.connect()
                    # send code from phone number
                    code_coinfig = await self.client.send_code(self.user_dict['PHONE_NUMBER'])
                    # get code hash 
                    self.user_dict['CODE_HASH'] = code_coinfig.phone_code_hash
                    # edit STATE
                    add_acconet_stat['PHONE_STATE'] = False
                    add_acconet_stat['CODE_STATE'] = True
                    await bot.edit_message_text(text="𝙿𝚕𝚎𝚊𝚜𝚎 𝚂𝚎𝚗𝚍 𝚟𝚎𝚛𝚒𝚏𝚒𝚌𝚊𝚝𝚒𝚘𝚗 𝚌𝚘𝚍𝚎 ,𝚂𝚎𝚗𝚍 𝙵𝚛𝚘𝚖 𝙿𝚑𝚘𝚗𝚎 𝙽𝚞𝚖𝚋𝚎𝚛 .", chat_id=self.chat_id ,message_id=
                        message_edit.message_id,reply_markup=BACK_HOME_KEYBOARD())
                    # get coinfig code start
                    await self.COINFIG_CODE()
                else: 
                    await bot.edit_message_text(text="𝚃𝚑𝚎 𝚊𝚌𝚌𝚘𝚞𝚗𝚝 𝚑𝚊𝚜 𝚊𝚕𝚛𝚎𝚊𝚍𝚢 𝚋𝚎𝚎𝚗 𝚊𝚍𝚍𝚎𝚍 .", chat_id=self.chat_id ,message_id=
                        message_edit.message_id,reply_markup=BACK_HOME_KEYBOARD())
                    add_acconet_stat['PHONE_STATE'] = False
                    
            # FloodWait error : 420
            except FloodWait as Err:
                await bot.edit_message_text(text=f"𝙱𝙻𝙾𝙲𝙺 𝙰𝚌𝚌𝚘𝚗𝚎𝚝 𝚏𝚛𝚘𝚖 𝚂𝚒𝚐𝚗 𝚒𝚜  ❲ {Err.value} ❳ 𝚜𝚎𝚌𝚞𝚒𝚗𝚎𝚍 .", chat_id=self.chat_id ,message_id=
                    message_edit.message_id,reply_markup=BACK_HOME_KEYBOARD())
                add_acconet_stat['PHONE_STATE'] = False
            # BadRequest error : 400
            except BadRequest as Err:
                # api_id/api_hash not faund
                if Err.ID == 'API_ID_INVALID':
                    await bot.edit_message_text(text="𝙴𝚛𝚛𝚘𝚛 𝙰𝙿𝙸_𝙷𝙰𝚂𝙷/𝙰𝙿𝙸_𝙸𝙳 𝙽𝚘𝚝 𝙵𝚊𝚞𝚗𝚎𝚍 .", chat_id=self.chat_id ,message_id=
                        message_edit.message_id,reply_markup=BACK_HOME_KEYBOARD())
                    add_acconet_stat['PHONE_STATE'] = False
                # Phone Not Faunde
                elif Err.ID == 'PHONE_NUMBER_INVALID':
                    await bot.edit_message_text(text="𝙴𝚛𝚛𝚘𝚛 𝙿𝙷𝙾𝙽𝙴 𝙽𝚄𝙼𝙱𝙴𝚁 𝙽𝙾𝚃 𝙵𝙰𝚄𝙽𝙴𝙳 ,𝙿𝚕𝚎𝚊𝚜𝚎 𝚂𝚎𝚗𝚍 𝙿𝚑𝚘𝚗𝚎 .", chat_id=self.chat_id ,message_id=
                        message_edit.message_id,reply_markup=BACK_HOME_KEYBOARD())
                else:
                    await bot.send_message(text=Err,chat_id=self.chat_id,reply_markup=BACK_HOME_KEYBOARD())
            except NotAcceptable as Err:
                if Err.ID == 'PHONE_NUMBER_INVALID':
                    await bot.edit_message_text(text="𝙴𝚛𝚛𝚘𝚛 𝙿𝙷𝙾𝙽𝙴 𝙽𝚄𝙼𝙱𝙴𝚁 𝙽𝙾𝚃 𝙵𝙰𝚄𝙽𝙴𝙳 ,𝙿𝚕𝚎𝚊𝚜𝚎 𝚂𝚎𝚗𝚍 𝙿𝚑𝚘𝚗𝚎 .", chat_id=self.chat_id ,message_id=
                    message_edit.message_id,reply_markup=BACK_HOME_KEYBOARD())
                else:
                    await bot.send_message(text=Err,chat_id=self.chat_id,reply_markup=BACK_HOME_KEYBOARD())
    
    async def COINFIG_CODE(self, ): # get coinfig code 
        @bot.message_handler(func=lambda hndler: add_acconet_stat['CODE_STATE']== True and ADMINE_STATE['add_acconet']  == True)
        async def COINFIG_CODE_HAND(message):
            self.user_dict['CODE'] = message.text
      
            message_edit_wite = await bot.send_message(message.chat.id ,
                text='𝚆𝚒𝚝𝚑 𝚂𝚒𝚐𝚗 𝙰𝚌𝚌𝚘𝚗𝚎𝚝 .' )
            try:
                # singe acconet
                await self.client.sign_in(phone_number=self.user_dict['PHONE_NUMBER'] 
                ,phone_code_hash=self.user_dict['CODE_HASH'] ,phone_code=self.user_dict['CODE'])
                await self.ADD_SESSION(message_edit_wite)

            except SessionPasswordNeeded:
                await bot.edit_message_text(text="𝙸𝚏 𝚢𝚘𝚞𝚛 𝚊𝚌𝚌𝚘𝚞𝚗𝚝 𝚒𝚜 𝚕𝚘𝚌𝚔𝚎𝚍, 𝚋𝚞𝚝 𝚢𝚘𝚞 𝚑𝚊𝚟𝚎 𝚎𝚗𝚝𝚎𝚛𝚎𝚍 𝚊 𝚙𝚊𝚜𝚜𝚠𝚘𝚛𝚍, 𝚙𝚕𝚎𝚊𝚜𝚎 𝚜𝚎𝚗𝚍 𝚝𝚑𝚎 𝚙𝚊𝚜𝚜𝚠𝚘𝚛𝚍 .", chat_id=self.chat_id ,message_id=
                    message_edit_wite.message_id,reply_markup=BACK_HOME_KEYBOARD())
                add_acconet_stat['CODE_STATE'] = False
                add_acconet_stat['PASSORD_STATE'] = True
                await self.PASSURD_CACK()

            except PhoneCodeInvalid:
                await bot.edit_message_text(text="𝚃𝚑𝚎 𝚟𝚎𝚛𝚒𝚏𝚒𝚌𝚊𝚝𝚒𝚘𝚗 𝚌𝚘𝚍𝚎 𝚒𝚜 𝚒𝚗𝚌𝚘𝚛𝚛𝚎𝚌𝚝. 𝙿𝚕𝚎𝚊𝚜𝚎 𝚜𝚎𝚗𝚍 𝚊 𝚟𝚊𝚕𝚒𝚍 𝚌𝚘𝚍𝚎 .", chat_id=self.chat_id ,message_id=
                    message_edit_wite.message_id,reply_markup=BACK_HOME_KEYBOARD())


    
     
    async def PASSURD_CACK(self, ): # get coinfig code 
        @bot.message_handler(func=lambda hndler: add_acconet_stat['PASSORD_STATE'] == True and ADMINE_STATE['add_acconet']  == True)
        async def PASSURD_HAND(message):
            PASSURD = message.text
            self.user_dict['PASSURD'] = PASSURD
            message_edit_wite = await bot.send_message(message.chat.id ,
                    text='𝚆𝚒𝚝𝚑 Cahck passurd' )
            try:
                await self.client.check_password(PASSURD)
                add_acconet_stat['PASSORD_STATE'] = False
                await self.ADD_SESSION(message_edit_wite)

            except PasswordHashInvalid:
                await bot.edit_message_text(text="ارسل الباسورد الخاص بلحساب الصحيح مطور البوت ( @viptrt )  ", chat_id=self.chat_id ,message_id=
                    message_edit_wite.message_id,reply_markup=BACK_HOME_KEYBOARD())

        
    async def ADD_SESSION(self, message_edit_wite):
        # export session_string
        self.session_string = await self.client.export_session_string()
        # send message from acconet
        await self.client.send_message('me', 'done sessions')
        ACCONET_INFO = await self.client.get_me()
        # edit state 
        add_acconet_stat['CODE_STATE'] = False
        # add session data
        session_data.ADD_SESSION(self.user_dict['API_HASH'],self.user_dict['API_ID'],
            self.user_dict['PHONE_NUMBER'],
            self.session_string,ACCONET_INFO.first_name ,ACCONET_INFO.id,ACCONET_INFO.username)
        # edit message 
        await bot.edit_message_text(text="𝙳𝚘𝚗𝚎 𝙰𝚍𝚍 𝙰𝚌𝚘𝚗𝚎𝚝", chat_id=self.chat_id ,message_id=
            message_edit_wite.message_id,reply_markup=BACK_HOME_KEYBOARD())






# start bot /start
@bot.message_handler(commands='start')
async def START_BOT(message):
    await bot.send_message(text=MESSAGE_BOT['HOME'] ,chat_id=message.chat.id, reply_markup=HOME_KEYBOARD())


# back Home call
@bot.callback_query_handler(func=lambda c: c.data == "back_home")
async def ADD_ACCONET(call :types.CallbackQuery):
    chat_id,message_id = call.message.chat.id, call.message.message_id 
    await bot.edit_message_text(text=MESSAGE_BOT['HOME'],chat_id=chat_id,message_id=message_id,reply_markup=HOME_KEYBOARD())
    ADMINE_STATE['add_acconet'] = False
    ADMINE_STATE['add_username'] = False
    add_acconet_stat['API_HASH_STATE'] = False
    add_acconet_stat['API_ID_STATE'] = False
    add_acconet_stat['CODE_STATE'] = False
    add_acconet_stat['PHONE_STATE'] = False
    add_acconet_stat['PASSORD_STATE'] = False


# add acconet call 
@bot.callback_query_handler(func=lambda c: c.data == "add_acconet")
async def ADD_ACCONET(call :types.CallbackQuery):
    chat_id,message_id = call.message.chat.id, call.message.message_id 
    ADMINE_STATE['add_acconet'] = True
    hand =  ADD_SESSION_HANDLER(call)
    await hand.START()

# show acconet call
@bot.callback_query_handler(func=lambda c: c.data == "show_acconet")
async def ADD_ACCONET(call :types.CallbackQuery):
    chat_id,message_id = call.message.chat.id, call.message.message_id 
    await bot.edit_message_text(text=MESSAGE_BOT['SHOW_ACCONET'],chat_id=chat_id,message_id=message_id,reply_markup=SHOW_ALL_SESSION())

# Tools calls
async def SENND_MESSAGE_ALL_ACCONETS(username : str ,message : str):
    sessions = session_data.READ_SESSIONS()['sessions']
    DONE = 0
    ERRO = 0
    for session in sessions:
        try :
            async with Client(session ,session_string=sessions[session]['session']) as app:
                await app.send_message(username, message)
                DONE+=1
        except:
            ERRO+=1
    return DONE

async def JOIN_HANLL_ALL_ACCONETS(username : str):
    sessions = session_data.READ_SESSIONS()['sessions']
    DONE = 0
    ERRO = 0
    for session in sessions:
        try:
            async with Client(session ,session_string=sessions[session]['session']) as app:
                await app.join_chat(username)
                DONE+=1

        except:
            ERRO+=1
    return DONE

async def SEND_REC_ALL_ACCONETS(url_message):
    sessions = session_data.READ_SESSIONS()['sessions']
    DONE = 0
    ERRO = 0
    url_split = url_message.split('/')
    for session in sessions:
        
        async with Client(session ,session_string=sessions[session]['session']) as app:
            await app.send_reaction(url_split[-2], int(url_split[-1]), random.choice(reaction_list))
            DONE+=1
     
    return DONE
# send_message
@bot.callback_query_handler(func=lambda c: c.data == "t_send_message")
async def SEND_MESSAGE(call :types.CallbackQuery):
    chat_id,message_id = call.message.chat.id, call.message.message_id 
    await bot.edit_message_text(text="send username ",chat_id=chat_id,message_id=message_id,reply_markup=BACK_HOME_KEYBOARD())
    Status['get_message'] = True
    stat_get = {'stat':'username'}
    # start hanlder
    @bot.message_handler(content_types=['text'],func=lambda me:Status['get_message']  == True)
    async def GET_MESSAGE(message):
        if stat_get['stat'] == 'username':
            stat_get['username'] = message.text 
            stat_get['stat'] = 'message'
            await bot.send_message(text='send message',chat_id=message.chat.id)
        elif stat_get['stat'] == 'message':
            stat_get['stat'] = 'none'
            Status['get_message'] = False
            DONE_SEND  = await SENND_MESSAGE_ALL_ACCONETS(stat_get['username'], message.text)
            await bot.send_message(text=f'DOEN SEND MESSAGE FROM @{stat_get["username"]} Aconets ({str(DONE_SEND)}) ',chat_id=message.chat.id)


           

# join channl       
@bot.callback_query_handler(func=lambda c: c.data == "t_join_chanl")
async def JOIN_CHANNL(call :types.CallbackQuery):
    chat_id,message_id = call.message.chat.id, call.message.message_id 
    await bot.edit_message_text(text="ارسل يوزر القناه بدون @  مطور البوت ( @viptrt )   ",chat_id=chat_id,message_id=message_id,reply_markup=BACK_HOME_KEYBOARD())
    Status['get_message'] = True
    # start hanlder
    @bot.message_handler(content_types=['text'],func=lambda me:Status['get_message']  == True)
    async def GET_MESSAGE(message):
        Status['get_message'] = False
        DONE_JOIN = await  JOIN_HANLL_ALL_ACCONETS(message.text)
        await bot.send_message(text=f'DOEN JOIN FROM @{message.text} Aconets ({str(DONE_JOIN)}) ',chat_id=message.chat.id,reply_markup=BACK_HOME_KEYBOARD())
        
# send recet
@bot.callback_query_handler(func=lambda c: c.data == "t_reaction")
async def reaction(call :types.CallbackQuery):
    chat_id,message_id = call.message.chat.id, call.message.message_id 
    await bot.edit_message_text(text="ارسل رابط المنشور  مطور البوت ( @viptrt )  ",chat_id=chat_id,message_id=message_id,reply_markup=BACK_HOME_KEYBOARD())
    Status['get_message'] = True
    # start hanlder
    @bot.message_handler(content_types=['text'],func=lambda me:Status['get_message']  == True)
    async def GET_MESSAGE(message):
        Status['get_message'] = False
        DONE_REACTION = await SEND_REC_ALL_ACCONETS(message.text)
        await bot.send_message(text=f'Doen Send Reaction : ({str(DONE_REACTION)}) ',reply_markup=BACK_HOME_KEYBOARD(),chat_id=message.chat.id)
        

        
 
asyncio.run(bot.polling())





