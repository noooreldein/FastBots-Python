from storage import SimpleStorage
import requests
import json
import os
import re
import time
import random
import subprocess
import base64
import sys
from pprint import pprint
from urllib.parse import urlparse, urlencode, quote, unquote
from td import FastBots

# ------------------------------------------------------------------
# Redis Connection
# ------------------------------------------------------------------
Redis = SimpleStorage()

def r_get(key):
    return Redis.get(key)

def r_smembers(key):
    members = Redis.smembers(key)
    return list(members)

def r_sismember(key, value):
    return bool(Redis.sismember(key, value))

# ------------------------------------------------------------------
# Interactive Setup Flow
# ------------------------------------------------------------------
SshId = subprocess.getoutput("echo $SSH_CLIENT | awk '{ print $1}'").strip()

if not os.path.exists("./Information.py"):
    token_key = f"{SshId}Info:Redis:Token"
    token_user_key = f"{SshId}Info:Redis:Token:User"
    user_key = f"{SshId}Info:Redis:User"
    user_id_key = f"{SshId}Info:Redis:User:ID"

    if not Redis.get(token_key):
        sys.stdout.write("\033[1;31mارسل لي توكن البوت الان \nSend Me a Bot Token Now ↡\n\033[0;39;49m")
        sys.stdout.flush()
        TokenBot = input().strip()
        match = re.match(r'(\d+):(.*)', TokenBot)
        if match:
            try:
                res = requests.get(f"https://api.telegram.org/bot{TokenBot}/getMe")
                if res.status_code == 200:
                    Json_Info = res.json()
                    if Json_Info.get("ok"):
                        sys.stdout.write("\033[1;34mتم حفظ التوكن بنجاح \nThe token been saved successfully \n\033[0;39;49m\n")
                        TheTokenBot = match.group(1)
                        subprocess.run(f"rm -fr .CallBack-Bot/{TheTokenBot}", shell=True)
                        Redis.set(token_key, TokenBot)
                        Redis.set(token_user_key, Json_Info["result"]["username"])
                    else:
                        print("\033[1;34mعذرا توكن البوت خطأ تحقق منه وارسله مره اخره \nBot Token is Wrong\n")
                else:
                    print("\033[1;34mعذرا توكن البوت خطأ تحقق منه وارسله مره اخره \nBot Token is Wrong\n")
            except Exception:
                print("\033[1;34mعذرا توكن البوت خطأ تحقق منه وارسله مره اخره \nBot Token is Wrong\n")
        else:
            print("\033[1;34mلم يتم حفظ التوكن جرب مره اخره \nToken not saved, try again")
        os.execv(sys.executable, [sys.executable] + sys.argv)

    if not Redis.get(user_key):
        sys.stdout.write("\033[1;31mارسل معرف المطور الاساسي الان \nDeveloper UserName saved ↡\n\033[0;39;49m")
        sys.stdout.flush()
        UserSudo = input().replace('@', '').strip()
        if UserSudo != '':
            sys.stdout.write("\n\033[1;34mتم حفظ معرف المطور \nDeveloper UserName saved \n\n\033[0;39;49m\n")
            Redis.set(user_key, UserSudo)
        else:
            print("\n\033[1;34mلم يتم حفظ معرف المطور الاساسي \nDeveloper UserName not saved\n")
        os.execv(sys.executable, [sys.executable] + sys.argv)

    if not Redis.get(user_id_key):
        sys.stdout.write("\033[1;31mارسل ايدي المطور الاساسي الان \nDeveloper ID saved ↡\n\033[0;39;49m")
        sys.stdout.flush()
        UserId = input().strip()
        match_id = re.match(r'(\d+)', UserId)
        if match_id:
            sys.stdout.write("\n\033[1;34mتم حفظ ايدي المطور \nDeveloper ID saved \n\n\033[0;39;49m\n")
            Redis.set(user_id_key, UserId)
        else:
            print("\n\033[1;34mلم يتم حفظ ايدي المطور الاساسي \nDeveloper ID not saved\n")
        os.execv(sys.executable, [sys.executable] + sys.argv)

    tok_str = r_get(token_key)
    ubot_str = r_get(token_user_key)
    usudo_str = r_get(user_key)
    sudoid_str = r_get(user_id_key)

    with open("Information.py", "w", encoding="utf-8") as f:
        f.write(f'Token = "{tok_str}"\nUserBot = "{ubot_str}"\nUserSudo = "{usudo_str}"\nSudoId = {sudoid_str}\n')

    with open("start", "w", encoding="utf-8") as f:
        f.write("cd $(cd $(dirname $0); pwd)\npython3 Fast.py\n")

    Redis.delete(user_id_key)
    Redis.delete(user_key)
    Redis.delete(token_user_key)
    Redis.delete(token_key)

    subprocess.run("chmod +x start", shell=True)
    subprocess.run([sys.executable] + sys.argv)
    sys.exit(0)

# ------------------------------------------------------------------
# Import Configuration
# ------------------------------------------------------------------
import Information

Sudo_Id = Information.SudoId
UserSudo = Information.UserSudo
Token = Information.Token
UserBot = Information.UserBot
Fast = Token.split(":")[0]

mongodb_list = [
    "mongodb+srv://NANA:NANA@cluster0.nwbxug1.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://bshwaty:bshwaty@cluster0.1htwdrk.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://amroO0O:amroO0O@cluster0.wpuzjc3.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://UOUOP:UOUOP@cluster0.mrtnl9h.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://bnatyt:bnatyt@cluster0.smhzfv0.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://sohbya:sohbya@cluster0.wbvjaup.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://JAKOZA:JAKOZA@cluster0.d5ddv1n.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://MEDOZ:MEDOZ@cluster0.dy7mnbo.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://Anubarlo:Anubarlo@cluster0.ioiefbq.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://kofor98990:kofor98990@cluster0.chpnoxi.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://zazaqzaza:zazaqzaza@cluster0.2cbxhfr.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://banzima:banzima@cluster0.xmaorqt.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://Yayatrue:Yayatrue@cluster0.bxsqkzf.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://UoUpl:UoUpl@cluster0.sufxjc1.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://sevet:sevet@cluster0.jdhl1jf.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://amoropyrh:amoropyrh@cluster0.gr6wdvv.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://jokhabn:jokhabn@cluster0.bor53ye.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://Kazanova:Kazanova@cluster0.cnj97ya.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://hsbnsbs:hsbnsbs@cluster0.8h1mmtr.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://adamsbarlo:adamsbarlo@cluster0.ey30t4t.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://HznsssM:HznsssM@cluster0.u8lzlkt.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://Amrooo0:Amrooo0@cluster0.epa8l8e.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://Jokaye:Jokaye@cluster0.xf7zgfo.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://Gaklpq008:Gaklpq008@cluster0.bfbyk4t.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://janha:janha@cluster0.8sivfcv.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://kazablnka:kazablnka@cluster0.kk5tnaq.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://Hjllqna:Hjllqna@cluster0.nm4mv2i.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://Bsbbbzs:Bsbbbzs@cluster0.tfg8lxa.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://Nznnnsnz:Nznnnsnz@cluster0.woopdba.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://Naopqmz778:Naopqmz778@cluster0.ed97t5o.mongodb.net/?retryWrites=true&w=majority"
]


bot = FastBots()
bot = bot.set_config(
    api_id=1846213,
    api_hash='c545c613b78f18a30744970910124d53',
    session_name=Fast,
    token=Token
)

# ------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------
def var(value):
    pprint(value)

def download(url, name=None):
    if not name:
        name = url.split('/')[-1]
    if url.startswith('https://') or url.startswith('http://'):
        try:
            res = requests.get(url)
            if res.status_code != 200:
                return f'check url , error code : {res.status_code}'
            with open(name, 'wb') as f:
                f.write(res.content)
            return f'./{name}'
        except Exception as e:
            return f'check url , error code : {e}'
    else:
        return 'The link format is incorrect.'

def sleep(n):
    time.sleep(n)

def Dev(msg):
    dev_list = [str(Sudo_Id), '5675627801', '5041044821', '5512718660']
    if isinstance(msg, dict):
        sender = msg.get('sender_id', {})
        if isinstance(sender, dict):
            sender_user_id = str(sender.get('user_id', 0))
            # Check hardcoded list
            if sender_user_id in dev_list:
                return True
            # Check Redis dev set (added via "رفع مطور <id>")
            try:
                if r_sismember(f"{Fast}Dev", sender_user_id):
                    return True
            except Exception:
                pass
    return False

def scandirfile(directory):
    try:
        return os.listdir(directory)
    except Exception:
        return []

def exi_filesx(cpath):
    return scandirfile(cpath)

def checkfile(name, cpath):
    for v in exi_filesx(cpath):
        if name in v:
            return True
    return False

def ChannelJoin(id_user):
    JoinChannel = True
    chh = r_get(f"{Fast}chfalse")
    if chh:
        try:
            res = requests.get(f"https://api.telegram.org/bot{Token}/getchatmember?chat_id={chh}&user_id={id_user}")
            if res.status_code == 200:
                data_json = res.json()
                status = data_json.get('result', {}).get('status')
                if status in ['left', 'kicked']:
                    JoinChannel = False
        except Exception:
            pass
    return JoinChannel

def send(chat, rep=0, text="", parse=None, dis=None, clear=None, disn=None, back=None, markup=None):
    return bot.sendText(chat, rep, text, parse, dis, clear, disn, back, markup)

def Reply_Status(UserId, TextMsg):
    try:
        UserInfo = bot.getUser(UserId)
        Name_User = UserInfo.get('first_name') if isinstance(UserInfo, dict) else getattr(UserInfo, 'first_name', None)
    except Exception:
        Name_User = None
    if Name_User:
        UserInfousername = f'[{Name_User}](tg://user?id={UserId})'
    else:
        UserInfousername = str(UserId)
    Textdata = globals().get('Textdata', '')
    return {
        'Lock': f'\n*✨ بواسطه ← *{UserInfousername}\n*{Textdata}\n✨خاصيه المسح *',
        'unLock': f'\n*✨ بواسطه ← *{UserInfousername}\n{TextMsg}',
        'lockKtm': f'\n*✨ بواسطه ← *{UserInfousername}\n*{Textdata}\n✨خاصيه الكتم *',
        'lockKid': f'\n*✨ بواسطه ← *{UserInfousername}\n*{Textdata}\n✨خاصيه التقييد *',
        'lockKick': f'\n*✨ بواسطه ← *{UserInfousername}\n*{Textdata}\n✨خاصيه الطرد *',
        'Reply': f'\n*✨ المستخدم ← *{UserInfousername}\n*{TextMsg}*'
    }

# ------------------------------------------------------------------
# Main Logic: Run(msg, data)
# ------------------------------------------------------------------
def Run(msg, data):
    text = ""
    content = data.get('content', {}) if isinstance(data, dict) else {}
    if isinstance(content, dict) and 'text' in content:
        text_obj = content.get('text', {})
        if isinstance(text_obj, dict):
            text = text_obj.get('text', '').strip() if text_obj.get('text') else ''
        elif isinstance(text_obj, str):
            text = text_obj.strip()

    sender_id_obj = data.get('sender_id', {}) if isinstance(data, dict) else {}
    sender_id = sender_id_obj.get('user_id', 0) if isinstance(sender_id_obj, dict) else 0

    if str(sender_id) == str(Fast):
        return False

    chsource = r_get(f"{Fast}chsource") or "SOURCEVEGA"

    chat_id = data.get('chat_id')
    msg_id = data.get('id', 0)

    # --------------------------------------------------------------
    # SUDO Commands
    # --------------------------------------------------------------
    if Dev(msg):
        if text in ["تحديث", "اعاده التشغيل ✨"]:
            bot.sendText(chat_id, 0, "✨ تمت اعاده تشغيل الملفات بنجاح ✅")
            os.execv(sys.executable, [sys.executable] + sys.argv)
            return False

        if text == "✨ تنظيف الملفات":
            import shutil
            cleaned = 0
            for root, dirs, files in os.walk("./source"):
                for d in list(dirs):
                    if d == "__pycache__":
                        shutil.rmtree(os.path.join(root, d), ignore_errors=True)
                        cleaned += 1
                for fn in list(files):
                    if fn.endswith(".pyc") or fn.endswith(".bak") or fn == "0":
                        try:
                            os.remove(os.path.join(root, fn))
                            cleaned += 1
                        except:
                            pass
            if os.path.exists("./update"):
                shutil.rmtree("./update", ignore_errors=True)
                cleaned += 1
            send(chat_id, msg_id, f"✨ تم تنظيف {cleaned} ملف/مجلد من الملفات المؤقتة\n✨ تم مسح الكاش والملفات القديمة", "md", True)
            return False

        reply_to_msg_id = data.get('reply_to_message_id', 0)
        if reply_to_msg_id != 0:
            Message_Get = bot.getMessage(chat_id, reply_to_msg_id)
            if isinstance(Message_Get, dict) and Message_Get.get('forward_info'):
                date_key = Message_Get['forward_info'].get('date')
                Info_User = r_get(f"{Fast}Twasl:UserId{date_key}") or 46899864
                if text == 'حظر':
                    Redis.sadd(f"{Fast}BaN:In:Tuasl", Info_User)
                    return send(chat_id, msg_id, Reply_Status(Info_User, '✨ تم حظره من الصانع')['Reply'], "md", True)
                if text in ['الغاء الحظر', 'الغاء حظر']:
                    Redis.srem(f"{Fast}BaN:In:Tuasl", Info_User)
                    return send(chat_id, msg_id, Reply_Status(Info_User, '✨ تم الغاء حظره من الصانع ')['Reply'], "md", True)

        if text == "✨ الغاء الامر":
            Redis.delete(f"{Fast}{sender_id}bottoken")
            Redis.delete(f"{Fast}{sender_id}botuser")
            Redis.delete(f"{Fast}{sender_id}dev:user")
            Redis.delete(f"{Fast}{sender_id}dev:id")
            Redis.delete(f"{Fast}{sender_id}app:id")
            Redis.delete(f"{Fast}{sender_id}api:hash")
            Redis.delete(f"{Fast}{sender_id}session")
            Redis.delete(f"{Fast}{sender_id}helper")
            Redis.delete(f"{Fast}{sender_id}ch:7oda")
            Redis.delete(f"{Fast}{sender_id}make:bot")
            Redis.delete(f"{Fast}{sender_id}gp:id")
            Redis.delete(f"{Fast}{sender_id}gp:user")
            return send(chat_id, msg_id, "✨ تم الغاء الامر بنجاح")

        if text == "/start":
            Redis.delete(f"{Fast}{sender_id}bottoken")
            Redis.delete(f"{Fast}{sender_id}botuser")
            Redis.delete(f"{Fast}{sender_id}make:bot")

            reply_markup = bot.replyMarkup({
                'type': 'keyboard',
                'resize': True,
                'is_personal': True,
                'data': [
                    [
                        {'text': '✨ صنع بوت', 'type': 'text', 'style': 'success', 'icon_custom_emoji_id': 5319101633550896862},
                        {'text': '✨ حذف بوت', 'type': 'text', 'style': 'danger', 'icon_custom_emoji_id': 5307659638810877853}
                    ],
                    [
                        {'text': '✨ تفعيل الاشتراك الاجباري', 'type': 'text', 'style': 'success', 'icon_custom_emoji_id': 5888622809625661717},
                        {'text': '✨ تعطيل الاشتراك الاجباري', 'type': 'text', 'style': 'danger', 'icon_custom_emoji_id': 5204200890331835565}
                    ],
                    [
                        {'text': '✨ تفعيل الوضع المجاني', 'type': 'text', 'style': 'success', 'icon_custom_emoji_id': 5458611822116485224},
                        {'text': '✨ تعطيل الوضع المجاني', 'type': 'text', 'style': 'danger', 'icon_custom_emoji_id': 5837029841399975415}
                    ],
                    [
                        {'text': '✨ تحديث المصنوعات', 'type': 'text', 'style': 'primary', 'icon_custom_emoji_id': 5433878454078556670},
                        {'text': '✨ تنظيف الملفات', 'type': 'text', 'style': 'danger', 'icon_custom_emoji_id': 5307659638810877853}
                    ],
                    [
                        {'text': '✨ عدد البوتات', 'type': 'text', 'style': 'primary', 'icon_custom_emoji_id': 6269451181735546806}
                    ],
                    [
                        {'text': '✨ الاحصائيات', 'type': 'text', 'style': 'primary', 'icon_custom_emoji_id': 5449730014431959418},
                        {'text': '✨ الاسكرينات المفتوحه', 'type': 'text', 'style': 'primary', 'icon_custom_emoji_id': 5783089682136964715}
                    ],
                    [
                        {'text': '✨ تفعيل التواصل', 'type': 'text', 'style': 'success', 'icon_custom_emoji_id': 5458611822116485224},
                        {'text': '✨ تعطيل التواصل', 'type': 'text', 'style': 'danger', 'icon_custom_emoji_id': 5837029841399975415}
                    ],
                    [
                        {'text': '✨ اذاعه', 'type': 'text', 'style': 'primary', 'icon_custom_emoji_id': 6165579510805696230},
                        {'text': '✨ اذاعه بالتوجيه', 'type': 'text', 'style': 'primary', 'icon_custom_emoji_id': 6165579510805696230}
                    ],
                    [
                        {'text': 'اعاده التشغيل ✨', 'type': 'text', 'style': 'primary', 'icon_custom_emoji_id': 5220021677244559322}
                    ],
                    [
                        {'text': '✨ الغاء الامر', 'type': 'text', 'style': 'danger', 'icon_custom_emoji_id': 5974342591552952895}
                    ]
                ]
            })
            send(chat_id, msg_id, "✨ اهلا بك عزيزي المطور الاساسي \n", "md", True, False, False, True, reply_markup)
            return False

        if text:
            m_ref = re.match(r"^رفع مطور (\d+)$", text)
            if m_ref:
                Redis.sadd(f"{Fast}Dev", m_ref.group(1))
                send(chat_id, msg_id, '✨ تم رفع العضو مطور ف الصانع بنجاح ', "md", True)
                return False

            m_tanz = re.match(r"^تنزيل مطور (\d+)$", text)
            if m_tanz:
                Redis.srem(f"{Fast}Dev", m_tanz.group(1))
                send(chat_id, msg_id, '✨ تم تنزيل العضو مطور من الصانع بنجاح ', "md", True)
                return False

        if text == "✨ تفعيل الوضع المجاني":
            Redis.delete(f"{Fast}free:bot")
            send(chat_id, msg_id, '✨ تم تفعيل الوضع المجاني ', "md", True)

        if text == "✨ تعطيل الوضع المجاني":
            Redis.set(f"{Fast}free:bot", "true")
            send(chat_id, msg_id, '✨ تم تعطيل الوضع المجاني ', "md", True)

        # Forced subscription check
        if r_get(f"{Fast}ch:addd{sender_id}") == "on":
            Redis.set(f"{Fast}ch:addd{sender_id}", "off")
            try:
                m_res = requests.get(f"http://api.telegram.org/bot{Token}/getchat?chat_id={text}")
                da = m_res.json() if m_res.status_code == 200 else {}
            except Exception:
                da = {}
            if da.get('result', {}).get('invite_link'):
                ch = da['result']['id']
                send(chat_id, msg_id, '✨ تم حفظ القناه ', "md", True)
                Redis.delete(f"{Fast}chfalse")
                Redis.set(f"{Fast}chfalse", ch)
                Redis.delete(f"{Fast}ch:admin")
                Redis.set(f"{Fast}ch:admin", da['result']['invite_link'])
            else:
                send(chat_id, msg_id, '✨ المعرف خطأ او البوت ليس مشرف في القناه ', "md", True)

        if text == "✨ تفعيل الاشتراك الاجباري":
            Redis.set(f"{Fast}ch:addd{sender_id}", "on")
            send(chat_id, msg_id, '✨ ارسل الان معرف القناه ', "md", True)

        if text == "✨ تعطيل الاشتراك الاجباري":
            Redis.delete(f"{Fast}ch:admin")
            Redis.delete(f"{Fast}chfalse")
            send(chat_id, msg_id, '✨ تم حذف القناه ', "md", True)

        # Sudo bot creation flow steps
        if text and re.match(r"^@(.*)", text) and r_get(f"{Fast}{sender_id}ch:7oda"):
            user = re.match(r"^@(.*)", text).group(1)
            get = bot.searchPublicChat(user)
            if isinstance(get, dict) and get.get('type', {}).get('supergroup_id'):
                Redis.set(f"{Fast}{sender_id}gp:user", user)
                Redis.set(f"{Fast}{sender_id}gp:id", f"-100{get['type']['supergroup_id']}")
                token_val = r_get(f"{Fast}{sender_id}bottoken")
                userbot_val = r_get(f"{Fast}{sender_id}botuser")
                dev_user_val = r_get(f"{Fast}{sender_id}dev:user")
                dev_id_val = r_get(f"{Fast}{sender_id}dev:id")
                session_val = r_get(f"{Fast}{sender_id}session")
                gp_id_val = r_get(f"{Fast}{sender_id}gp:id") or dev_id_val

                with open("./source/.env", "w", encoding="utf-8") as env_file:
                    env_file.write(f"API_ID=10823881\nAPI_HASH=339886e2109eb67203ce12022b32e035\nBOT_TOKEN={token_val}\nMONGO_DB_URI={random.choice(mongodb_list)}\nLOG_GROUP_ID={gp_id_val}\nMUSIC_BOT_NAME={userbot_val}\nSTRING_SESSION={session_val}\nOWNER_ID={dev_id_val}")
                time.sleep(3)
                send(chat_id, 0, "✨ تم حفظ بيانات البوت جاري التشغيل يرجي الانتظار ...", "md", True)
                subprocess.run("find ./source -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; find ./source -name *.pyc -delete 2>/dev/null; find ./source -name *.bak -delete 2>/dev/null", shell=True)
                subprocess.run(f"cp -a ./source/. ./@{userbot_val}", shell=True)
                time.sleep(1)
                subprocess.run(f"cd @{userbot_val} && pip3 install -r requirements.txt 2>&1 | tail -5", shell=True, timeout=300)
                subprocess.run(f"screen -m -d -S {userbot_val} bash -c 'cd {os.getcwd()}/@{userbot_val} && bash start.sh {Token} {Sudo_Id}'", shell=True)
                time.sleep(5)

                Redis.delete(f"{Fast}{sender_id}bottoken")
                Redis.delete(f"{Fast}{sender_id}botuser")
                Redis.delete(f"{Fast}{sender_id}dev:user")
                Redis.delete(f"{Fast}{sender_id}dev:id")
                Redis.delete(f"{Fast}{sender_id}app:id")
                Redis.delete(f"{Fast}{sender_id}api:hash")
                Redis.delete(f"{Fast}{sender_id}session")
                Redis.delete(f"{Fast}{sender_id}helper")
                Redis.delete(f"{Fast}{sender_id}ch:7oda")
                Redis.delete(f"{Fast}{sender_id}make:bot")
                Redis.delete(f"{Fast}{sender_id}gp:id")
                Redis.delete(f"{Fast}{sender_id}gp:user")
                Redis.delete(f"{Fast}{sender_id}mongoDB")

                Redis.sadd(f"{Fast}bots", f"@{userbot_val} » @{dev_user_val}")
                send(chat_id, msg_id, "✨ تم تشغيل البوت بنجاح \n✨ في حاله لم يعمل البوت هذا يعني وجود خطأ في احدى البيانات اللتي ارسلتها", "md", True)
                return send(chat_id, msg_id, "✨ تم حفظ جروب الدعم بنجاح \n✨ جاري التشغيل", "md", True)
            else:
                return send(chat_id, msg_id, "✨ المعرف ليس لمجموعه خارقه تأكد منه")

        if text and r_get(f"{Fast}{sender_id}make:bot") == "devid":
            m_devid = re.match(r"^(\d+)$", text)
            if m_devid:
                DevId = m_devid.group(1)
                Redis.set(f"{Fast}{sender_id}dev:id", DevId)
                Redis.set(f"{Fast}{sender_id}make:bot", "session")
                return send(chat_id, msg_id, "✨ تم حفظ مطور البوت \n✨ ارسل الان جلسه البايروجرام \n✨ احصل عليه من هنا @s_stbot")
            send(chat_id, msg_id, "✨ ارسل ايدي المطور بشكل صحيح (ارقام فقط) ", "md", True)
            return False

        if text and r_get(f"{Fast}{sender_id}make:bot") == "devuser":
            m_devusr = re.match(r"^@(.+)$", text.strip())
            if m_devusr:
                UserName = m_devusr.group(1)
                if re.search(r'(\S+)[Bb][Oo][Tt]', UserName):
                    send(chat_id, msg_id, "✨ عذرا يجب ان تستخدم معرف لحساب شخصي فقط ", "md", True)
                    return False
                Redis.set(f"{Fast}{sender_id}dev:user", UserName)
                Redis.set(f"{Fast}{sender_id}make:bot", "devid")
                return send(chat_id, msg_id, "✨ تم حفظ معرف المطور \n✨ ارسل الان ايدي المطور (رقمي) \n✨ احصل عليه من @userinfobot")
            send(chat_id, msg_id, "✨ اليوزر ليس لحساب شخصي تأكد منه\n✨ ارسل المعرف بشكل صحيح مثال: @username", "md", True)
            return False

        if text and r_get(f"{Fast}{sender_id}make:bot") == "session":
            if text:
                Redis.set(f"{Fast}{sender_id}session", text)
                Redis.set(f"{Fast}{sender_id}make:bot", "helper")
                return send(chat_id, msg_id, "✨ تم حفظ جلسه البايروجرام \n✨ ارسل الان ايدي الحساب المساعد")
            return False

        if text and r_get(f"{Fast}{sender_id}make:bot") == "helper":
            m_helper = re.match(r"^(\d+)$", text)
            if m_helper:
                Redis.set(f"{Fast}{sender_id}helper", text)
                Redis.set(f"{Fast}{sender_id}make:bot", "channel")
                return send(chat_id, msg_id, "✨ تم حفظ ايدي الحساب المساعد \n✨ ارسل الان معرف قناة الاشتراك الاجباري")
            send(chat_id, msg_id, "✨ ارسل ايدي الحساب المساعد بشكل صحيح ", "md", True)
            return False

        if text and r_get(f"{Fast}{sender_id}make:bot") == "channel":
            m_chan = re.match(r"^@(.*)$", text)
            if m_chan:
                ChanUser = m_chan.group(1)
                Redis.set(f"{Fast}{sender_id}ch:7oda", ChanUser)
                Redis.set(f"{Fast}{sender_id}make:bot", "group")
                return send(chat_id, msg_id, "✨ تم حفظ قناه الاشتراك الاجباري \n✨ ارسل الان معرف جروب الدعم \n✨ تأكد ان البوت مشرف بالجروب")
            send(chat_id, msg_id, "✨ ارسل معرف القناة بشكل صحيح (مثل @channel) ", "md", True)
            return False

        if text and r_get(f"{Fast}{sender_id}make:bot") == "group":
            m_grp = re.match(r"^@(.*)$", text)
            if m_grp:
                GrpUser = m_grp.group(1)
                get = bot.searchPublicChat(GrpUser)
                if isinstance(get, dict) and get.get('type', {}).get('supergroup_id'):
                    Redis.set(f"{Fast}{sender_id}gp:user", GrpUser)
                    Redis.set(f"{Fast}{sender_id}gp:id", f"-100{get['type']['supergroup_id']}")
                    # All data collected - create the bot
                    token_val = r_get(f"{Fast}{sender_id}bottoken")
                    userbot_val = r_get(f"{Fast}{sender_id}botuser")
                    dev_user_val = r_get(f"{Fast}{sender_id}dev:user")
                    dev_id_val = r_get(f"{Fast}{sender_id}dev:id")
                    session_val = r_get(f"{Fast}{sender_id}session")
                    gp_id_val = r_get(f"{Fast}{sender_id}gp:id") or dev_id_val

                    with open("./source/.env", "w", encoding="utf-8") as env_file:
                        env_file.write(f"API_ID=10823881\nAPI_HASH=339886e2109eb67203ce12022b32e035\nBOT_TOKEN={token_val}\nMONGO_DB_URI={random.choice(mongodb_list)}\nLOG_GROUP_ID={gp_id_val}\nMUSIC_BOT_NAME={userbot_val}\nSTRING_SESSION={session_val}\nOWNER_ID={dev_id_val}")
                    time.sleep(3)
                    send(chat_id, 0, "✨ تم حفظ بيانات البوت جاري التشغيل يرجي الانتظار ...", "md", True)
                    subprocess.run("find ./source -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; find ./source -name *.pyc -delete 2>/dev/null; find ./source -name *.bak -delete 2>/dev/null", shell=True)
                    subprocess.run("find ./source -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; find ./source -name *.pyc -delete 2>/dev/null; find ./source -name *.bak -delete 2>/dev/null", shell=True)
                    subprocess.run(f"cp -a ./source/. ./@{userbot_val}", shell=True)
                    time.sleep(1)
                    subprocess.run(f"cd @{userbot_val} && pip3 install -r requirements.txt 2>&1 | tail -5", shell=True, timeout=300)
                    subprocess.run(f"screen -m -d -S {userbot_val} bash -c 'cd {os.getcwd()}/@{userbot_val} && bash start.sh {Token} {Sudo_Id}'", shell=True)
                    time.sleep(5)

                    # Cleanup
                    for k in ['bottoken', 'dev:user', 'dev:id', 'app:id', 'api:hash', 'session', 'helper', 'ch:7oda', 'make:bot', 'gp:id', 'gp:user', 'mongoDB']:
                        Redis.delete(f"{Fast}{sender_id}{k}")

                    send(Sudo_Id, 0, f"✨ تم تنصيب بوت جديد \n✨ توكن البوت `{token_val}`\n✨ معرف المطور [@{dev_user_val}]", "md", True)
                    Redis.sadd(f"{Fast}bots", f"@{userbot_val} » @{dev_user_val}")
                    send(chat_id, msg_id, "✨ تم تشغيل البوت بنجاح \n✨ في حاله لم يعمل البوت هذا يعني وجود خطأ في احدى البيانات اللتي ارسلتها", "md", True)
                    return send(chat_id, msg_id, "✨ تم حفظ جروب الدعم بنجاح \n✨ جاري التشغيل", "md", True)
                else:
                    return send(chat_id, msg_id, "✨ المعرف ليس لمجموعه خارقه تأكد منه")
            send(chat_id, msg_id, "✨ ارسل معرف الجروب بشكل صحيح (مثل @group) ", "md", True)
            return False

        if text and r_get(f"{Fast}{sender_id}make:bot") == "token":
            m_tok = re.match(r"(\d+):(.*)", text)
            if m_tok:
                try:
                    res = requests.get(f"http://api.telegram.org/bot{text}/getme")
                    json_data = res.json() if res.status_code == 200 else {}
                except Exception:
                    json_data = {}
                if json_data.get('ok') is True:
                    botuser = json_data['result']['username']
                    if r_sismember(f"{Fast}userbots", botuser):
                        send(chat_id, msg_id, "\n✨ عذرا هذا البوت مصنوع بالفعل", "md", True)
                        return False
                    Redis.set(f"{Fast}{sender_id}botuser", botuser)
                    Redis.set(f"{Fast}{sender_id}bottoken", text)
                    Redis.set(f"{Fast}{sender_id}make:bot", "devuser")
                    send(chat_id, msg_id, "\n✨ ارسل الان معرف المطور الاساسي (مثل @username)")
                    return False
                send(chat_id, msg_id, "\n✨ التوكن الذي ارسلته غير صحيح ")
                return False
            send(chat_id, msg_id, "\n✨ من فضلك ارسل التوكن بشكل صحيح ")

        if text == "✨ صنع بوت":
            Redis.set(f"{Fast}{sender_id}make:bot", "token")
            send(chat_id, msg_id, "\n✨ ارسل توكن البوت الان", "md", True)
            return False

        if text == "✨ تحديث المصنوعات":
            r = 0
            try:
                folders = os.listdir('.')
            except Exception:
                folders = []
            for folder in folders:
                if re.match(r'@[a-zA-Z0-9_]', folder) and os.path.isdir(folder):
                    screen_name = folder.replace('@', '')
                    subprocess.run(f"cp -a ./update/. ./{folder} 2>/dev/null || true; cd {folder} && chmod +x * && screen -X -S {screen_name} quit 2>/dev/null || true; screen -d -m -S {screen_name} sh -c 'cd . && python3 -m YukkiMusic'", shell=True)
                    r += 1
            subprocess.run("rm -fr ./source/*", shell=True)
            subprocess.run("cp -a ./update/. ./source 2>/dev/null || true", shell=True)
            send(msg.get('chat_id', chat_id), msg.get('id', msg_id), f"تم تحديث {r} بوت", "html", True)

        if text == "✨ عدد البوتات":
            list_bots = r_smembers(f"{Fast}bots")
            if len(list_bots) > 0:
                txx = "===== قائمه بوتاتك ======\n"
                for v in list_bots:
                    txx += f"{v}\n"
            else:
                txx = "• لا توجد بوتات مصنوعه"
            send(msg.get('chat_id', chat_id), msg.get('id', msg_id), txx)

        if text and text.startswith("✨ log "):
            bot_name = text.replace("✨ log ", "").strip().lstrip("@")
            log_file = f"/tmp/{bot_name}_bot.log"
            try:
                with open(log_file, "r") as lf:
                    log_content = lf.read()
                if log_content.strip():
                    # Send last 4000 chars
                    if len(log_content) > 4000:
                        log_content = "..." + log_content[-4000:]
                    send(chat_id, msg_id, "```" + log_content + "```", "md", True)
                else:
                    send(chat_id, msg_id, "✨ ملف اللوج فارغ - البوت لسه مشتغلش أو مشيقع", "md", True)
            except FileNotFoundError:
                send(chat_id, msg_id, f"✨ مفيش ملف log للبوت @{bot_name}\n✨ تأكد إنك كتبت اسم البوت صح", "md", True)
            except Exception as e:
                send(chat_id, msg_id, f"✨ خطأ: {e}", "md", True)
            return False

        if text == "✨ الاسكرينات المفتوحه":
            rqm = 0
            message = ' ✨ السكرينات الموجوده بالسيرفر \n\n'
            try:
                proc = subprocess.Popen('ls /var/run/screen/S-root', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                out, _ = proc.communicate()
                screen_lines = [l.strip() for l in out.splitlines() if l.strip()]
            except Exception:
                screen_lines = []
            for screnName in screen_lines:
                rqm += 1
                message += f"{rqm}-  {{ `{screnName}` }}\n"
            send(chat_id, msg_id, message + f'\n حاليا عندك `{rqm}` اسكرين مفتوح ...\n', "md", True)
            return False

        if text and r_get(f"{Fast}{sender_id}make:bot") == "del":
            if text in ["الغاء", "✨ الغاء الامر"]:
                Redis.delete(f"{Fast}{sender_id}make:bot")
                send(chat_id, msg_id, "\n✨ تم الغاء حذف البوت", "md", True)
                return False
            list_bots = r_smembers(f"{Fast}bots")
            if len(list_bots) > 0:
                for v in list_bots:
                    if text in v:
                        Redis.srem(f"{Fast}bots", v)
            subprocess.run(f"rm -fr {text}", shell=True)
            screen_name = text.replace('@', '')
            subprocess.run(f"screen -X -S {screen_name} quit 2>/dev/null || true", shell=True)
            send(chat_id, msg_id, "\n✨ تم حذف البوت بنجاح", "md", True)
            Redis.delete(f"{Fast}{sender_id}make:bot")
            return False

        if text == "✨ حذف بوت":
            Redis.set(f"{Fast}{sender_id}make:bot", "del")
            send(chat_id, msg_id, "\n✨ ارسل معرف البوت الان", "md", True)
            return False

        if text == "✨ تفعيل التواصل":
            Redis.delete(f"{Fast}twsl")
            send(chat_id, msg_id, "✨ تم تفعيل التواصل")
            return False

        if text == "✨ تعطيل التواصل":
            Redis.set(f"{Fast}twsl", "true")
            send(chat_id, msg_id, "✨ تم تعطيل التواصل")
            return False

        if text == "✨ الاحصائيات":
            list_total = r_smembers(f"{Fast}total")
            send(chat_id, msg_id, f"✨ عدد مشتركين بوتك {len(list_total)} مشترك")
            return False

        # Broadcast
        if r_get(f"{Fast}{sender_id}brodcast"):
            if text in ["الغاء", "✨ الغاء الامر"]:
                Redis.delete(f"{Fast}{sender_id}brodcast")
                send(chat_id, msg_id, "\n✨ تم الغاء الاذاعه", "md", True)
                return False
            list_total = r_smembers(f"{Fast}total")
            if content.get('video_note'):
                vn_id = content['video_note']['video']['remote']['id']
                for v in list_total:
                    bot.sendVideoNote(v, 0, vn_id)
            elif content.get('photo'):
                sizes = content['photo'].get('sizes', [])
                idPhoto = None
                if len(sizes) > 0 and sizes[0].get('photo', {}).get('remote', {}).get('id'):
                    idPhoto = sizes[0]['photo']['remote']['id']
                elif len(sizes) > 1 and sizes[1].get('photo', {}).get('remote', {}).get('id'):
                    idPhoto = sizes[1]['photo']['remote']['id']
                elif len(sizes) > 2 and sizes[2].get('photo', {}).get('remote', {}).get('id'):
                    idPhoto = sizes[2]['photo']['remote']['id']
                if idPhoto:
                    for v in list_total:
                        bot.sendPhoto(v, 0, idPhoto, '')
            elif content.get('sticker'):
                stk_id = content['sticker']['sticker']['remote']['id']
                for v in list_total:
                    bot.sendSticker(v, 0, stk_id)
            elif content.get('voice_note'):
                vc_id = content['voice_note']['voice']['remote']['id']
                for v in list_total:
                    bot.sendVoiceNote(v, 0, vc_id, '', 'md')
            elif content.get('video'):
                vid_id = content['video']['video']['remote']['id']
                for v in list_total:
                    bot.sendVideo(v, 0, vid_id, '', 'md')
            elif content.get('animation'):
                anim_id = content['animation']['animation']['remote']['id']
                for v in list_total:
                    bot.sendAnimation(v, 0, anim_id, '', 'md')
            elif content.get('document'):
                doc_id = content['document']['document']['remote']['id']
                for v in list_total:
                    bot.sendDocument(v, 0, doc_id, '', 'md')
            elif content.get('audio'):
                aud_id = content['audio']['audio']['remote']['id']
                for v in list_total:
                    bot.sendAudio(v, 0, aud_id, '', 'md')
            elif text:
                for v in list_total:
                    send(v, 0, text, "md", True)
            send(chat_id, msg_id, f"✨ تمت الاذاعه الى *- {len(list_total)} * عضو في البوت ", "md", True)
            Redis.delete(f"{Fast}{sender_id}brodcast")
            return False

        if text == "✨ اذاعه":
            Redis.set(f"{Fast}{sender_id}brodcast", "true")
            send(chat_id, msg_id, "✨ ارسل الاذاعه الان")
            return False

        # Forward Broadcast
        if r_get(f"{Fast}{sender_id}brodcast:fwd"):
            if text in ["الغاء", "✨ الغاء الامر"]:
                Redis.delete(f"{Fast}{sender_id}brodcast:fwd")
                send(chat_id, msg_id, "\n✨ تم الغاء الاذاعه بالتوجيه", "md", True)
                return False
            if data.get('forward_info'):
                list_total = r_smembers(f"{Fast}total")
                send(chat_id, msg_id, f"✨ تم التوجيه الى *- {len(list_total)} * مشترك ف البوت ", "md", True)
                for v in list_total:
                    bot.forwardMessages(v, chat_id, msg_id, 0, 0, True, False, False)
                Redis.delete(f"{Fast}{sender_id}brodcast:fwd")
            return False

        if text == "✨ اذاعه بالتوجيه":
            Redis.set(f"{Fast}{sender_id}brodcast:fwd", "true")
            send(chat_id, msg_id, "✨ ارسل التوجيه الان")
            return False

    # --------------------------------------------------------------
    # Non-SUDO / Regular User Commands
    # --------------------------------------------------------------
    if not Dev(data):
        if text and ChannelJoin(sender_id) is False:
            chinfo = r_get(f"{Fast}ch:admin") or ""
            send(chat_id, msg_id, f'\n✨ عليك الاشتراك في قناة البوت لاستخذام الاوامر\n\n{chinfo}')
            return False

        if not r_get(f"{Fast}twsl"):
            if str(sender_id) != str(Fast):
                if r_sismember(f"{Fast}BaN:In:Tuasl", sender_id):
                    return False
                if msg_id:
                    Redis.setex(f"{Fast}Twasl:UserId{data.get('date')}", 172800, sender_id)
                    bot.forwardMessages(Sudo_Id, chat_id, msg_id, 0, 0, True, False, False)

        if r_sismember(f"{Fast}BaN:In:Tuasl", sender_id):
            return False

        if text and r_get(f"{Fast}free:bot"):
            return send(chat_id, msg_id, "✨ الوضع المجاني معطل من قبل مطور الصانع")

        if text == "✨ الغاء":
            Redis.delete(f"{Fast}{sender_id}bottoken")
            Redis.delete(f"{Fast}{sender_id}dev:user")
            Redis.delete(f"{Fast}{sender_id}dev:id")
            Redis.delete(f"{Fast}{sender_id}app:id")
            Redis.delete(f"{Fast}{sender_id}api:hash")
            Redis.delete(f"{Fast}{sender_id}session")
            Redis.delete(f"{Fast}{sender_id}helper")
            Redis.delete(f"{Fast}{sender_id}ch:7oda")
            Redis.delete(f"{Fast}{sender_id}make:bot")
            Redis.delete(f"{Fast}{sender_id}gp:id")
            Redis.delete(f"{Fast}{sender_id}gp:user")
            Redis.delete(f"{Fast}{sender_id}mongoDB")
            send(chat_id, msg_id, "\n✨ تم الغاء الامر بنجاح ")
            return False

        if text == "/start":
            if not r_sismember(f"{Fast}total", sender_id):
                Redis.sadd(f"{Fast}total", sender_id)
            Redis.delete(f"{Fast}{sender_id}bottoken")
            Redis.delete(f"{Fast}{sender_id}dev:user")
            Redis.delete(f"{Fast}{sender_id}dev:id")
            Redis.delete(f"{Fast}{sender_id}app:id")
            Redis.delete(f"{Fast}{sender_id}api:hash")
            Redis.delete(f"{Fast}{sender_id}session")
            Redis.delete(f"{Fast}{sender_id}helper")
            Redis.delete(f"{Fast}{sender_id}ch:7oda")
            Redis.delete(f"{Fast}{sender_id}make:bot")
            Redis.delete(f"{Fast}{sender_id}gp:id")
            Redis.delete(f"{Fast}{sender_id}gp:user")
            Redis.delete(f"{Fast}{sender_id}mongoDB")

            reply_markup = bot.replyMarkup({
                'type': 'keyboard',
                'resize': True,
                'is_personal': True,
                'data': [
                    [
                        {'text': '✨ صنع بوت', 'type': 'text', 'style': 'success', 'icon_custom_emoji_id': 5319101633550896862},
                        {'text': '✨ حذف البوت', 'type': 'text', 'style': 'danger', 'icon_custom_emoji_id': 5307659638810877853}
                    ],
                    [
                        {'text': '✨ الغاء', 'type': 'text', 'style': 'danger', 'icon_custom_emoji_id': 5974342591552952895}
                    ]
                ]
            })
            send(chat_id, msg_id, "✨ اهــــــلــا بــــــك فــــــي صــــــانــــــع مــيوزك ســــــورس ثريثون\n✨ مــــطــــورين ســــورس ثريثون CCYFC.t.me", "html", True, False, False, True, reply_markup)
            return False

        # Regular user bot creation steps

        if text and r_get(f"{Fast}{sender_id}make:bot") == "devid":
            m_devid = re.match(r"^(\d+)$", text)
            if m_devid:
                DevId = m_devid.group(1)
                Redis.set(f"{Fast}{sender_id}dev:id", DevId)
                Redis.set(f"{Fast}{sender_id}make:bot", "session")
                return send(chat_id, msg_id, "✨ تم حفظ مطور البوت \n✨ ارسل الان جلسه البايروجرام \n✨ احصل عليه من هنا @s_stbot")
            send(chat_id, msg_id, "✨ ارسل ايدي المطور بشكل صحيح (ارقام فقط) ", "md", True)
            return False

        if text and r_get(f"{Fast}{sender_id}make:bot") == "devuser":
            m_devusr = re.match(r"^@(.+)$", text.strip())
            if m_devusr:
                UserName = m_devusr.group(1)
                if re.search(r'(\S+)[Bb][Oo][Tt]', UserName):
                    send(chat_id, msg_id, "✨ عذرا يجب ان تستخدم معرف لحساب شخصي فقط ", "md", True)
                    return False
                Redis.set(f"{Fast}{sender_id}dev:user", UserName)
                Redis.set(f"{Fast}{sender_id}make:bot", "devid")
                return send(chat_id, msg_id, "✨ تم حفظ معرف المطور \n✨ ارسل الان ايدي المطور (رقمي) \n✨ احصل عليه من @userinfobot")
            send(chat_id, msg_id, "✨ اليوزر ليس لحساب شخصي تأكد منه\n✨ ارسل المعرف بشكل صحيح مثال: @username", "md", True)
            return False

        if text and r_get(f"{Fast}{sender_id}make:bot") == "session":
            if text:
                Redis.set(f"{Fast}{sender_id}session", text)
                Redis.set(f"{Fast}{sender_id}make:bot", "helper")
                return send(chat_id, msg_id, "✨ تم حفظ جلسه البايروجرام \n✨ ارسل الان ايدي الحساب المساعد")
            return False

        if text and r_get(f"{Fast}{sender_id}make:bot") == "helper":
            m_helper = re.match(r"^(\d+)$", text)
            if m_helper:
                Redis.set(f"{Fast}{sender_id}helper", text)
                Redis.set(f"{Fast}{sender_id}make:bot", "channel")
                return send(chat_id, msg_id, "✨ تم حفظ ايدي الحساب المساعد \n✨ ارسل الان معرف قناة الاشتراك الاجباري")
            send(chat_id, msg_id, "✨ ارسل ايدي الحساب المساعد بشكل صحيح ", "md", True)
            return False

        if text and r_get(f"{Fast}{sender_id}make:bot") == "channel":
            m_chan = re.match(r"^@(.*)$", text)
            if m_chan:
                ChanUser = m_chan.group(1)
                Redis.set(f"{Fast}{sender_id}ch:7oda", ChanUser)
                Redis.set(f"{Fast}{sender_id}make:bot", "group")
                return send(chat_id, msg_id, "✨ تم حفظ قناه الاشتراك الاجباري \n✨ ارسل الان معرف جروب الدعم \n✨ تأكد ان البوت مشرف بالجروب")
            send(chat_id, msg_id, "✨ ارسل معرف القناة بشكل صحيح (مثل @channel) ", "md", True)
            return False

        if text and r_get(f"{Fast}{sender_id}make:bot") == "group":
            m_grp = re.match(r"^@(.*)$", text)
            if m_grp:
                GrpUser = m_grp.group(1)
                get = bot.searchPublicChat(GrpUser)
                if isinstance(get, dict) and get.get('type', {}).get('supergroup_id'):
                    Redis.set(f"{Fast}{sender_id}gp:user", GrpUser)
                    Redis.set(f"{Fast}{sender_id}gp:id", f"-100{get['type']['supergroup_id']}")
                    # All data collected - create the bot
                    token_val = r_get(f"{Fast}{sender_id}bottoken")
                    userbot_val = r_get(f"{Fast}{sender_id}botuser")
                    dev_user_val = r_get(f"{Fast}{sender_id}dev:user")
                    dev_id_val = r_get(f"{Fast}{sender_id}dev:id")
                    session_val = r_get(f"{Fast}{sender_id}session")
                    gp_id_val = r_get(f"{Fast}{sender_id}gp:id") or dev_id_val

                    with open("./source/.env", "w", encoding="utf-8") as env_file:
                        env_file.write(f"API_ID=10823881\nAPI_HASH=339886e2109eb67203ce12022b32e035\nBOT_TOKEN={token_val}\nMONGO_DB_URI={random.choice(mongodb_list)}\nLOG_GROUP_ID={gp_id_val}\nMUSIC_BOT_NAME={userbot_val}\nSTRING_SESSION={session_val}\nOWNER_ID={dev_id_val}")
                    time.sleep(3)
                    send(chat_id, 0, "✨ تم حفظ بيانات البوت جاري التشغيل يرجي الانتظار ...", "md", True)
                    subprocess.run(f"cp -a ./source/. ./@{userbot_val}", shell=True)
                    time.sleep(1)
                    subprocess.run(f"cd @{userbot_val} && pip3 install -r requirements.txt 2>&1 | tail -5", shell=True, timeout=300)
                    subprocess.run(f"screen -m -d -S {userbot_val} bash -c 'cd {os.getcwd()}/@{userbot_val} && bash start.sh {Token} {Sudo_Id}'", shell=True)
                    time.sleep(5)

                    # Cleanup
                    for k in ['bottoken', 'dev:user', 'dev:id', 'app:id', 'api:hash', 'session', 'helper', 'ch:7oda', 'make:bot', 'gp:id', 'gp:user', 'mongoDB']:
                        Redis.delete(f"{Fast}{sender_id}{k}")

                    send(Sudo_Id, 0, f"✨ تم تنصيب بوت جديد \n✨ توكن البوت `{token_val}`\n✨ معرف المطور [@{dev_user_val}]", "md", True)
                    Redis.sadd(f"{Fast}bots", f"@{userbot_val} » @{dev_user_val}")
                    send(chat_id, msg_id, "✨ تم تشغيل البوت بنجاح \n✨ في حاله لم يعمل البوت هذا يعني وجود خطأ في احدى البيانات اللتي ارسلتها", "md", True)
                    return send(chat_id, msg_id, "✨ تم حفظ جروب الدعم بنجاح \n✨ جاري التشغيل", "md", True)
                else:
                    return send(chat_id, msg_id, "✨ المعرف ليس لمجموعه خارقه تأكد منه")
            send(chat_id, msg_id, "✨ ارسل معرف الجروب بشكل صحيح (مثل @group) ", "md", True)
            return False

        if text and r_get(f"{Fast}{sender_id}make:bot") == "token":
            m_tok = re.match(r"(\d+):(.*)", text)
            if m_tok:
                try:
                    res = requests.get(f"http://api.telegram.org/bot{text}/getme")
                    json_data = res.json() if res.status_code == 200 else {}
                except Exception:
                    json_data = {}
                if json_data.get('ok') is True:
                    botuser = json_data['result']['username']
                    if r_sismember(f"{Fast}userbots", botuser):
                        send(chat_id, msg_id, "\n✨ عذرا هذا البوت مصنوع بالفعل", "md", True)
                        return False
                    Redis.set(f"{Fast}{sender_id}botuser", botuser)
                    Redis.set(f"{Fast}{sender_id}bottoken", text)
                    Redis.set(f"{Fast}{sender_id}make:bot", "devuser")
                    send(chat_id, msg_id, "\n✨ ارسل الان معرف المطور الاساسي (مثل @username)")
                    return False
                send(chat_id, msg_id, "\n✨ التوكن الذي ارسلته غير صحيح ")
                return False
            send(chat_id, msg_id, "\n✨ من فضلك ارسل التوكن بشكل صحيح ")

        if text == "✨ صنع بوت":
            if r_get(f"{Fast}{sender_id}botuser"):
                return send(chat_id, msg_id, "\n✨ لديك بوت بالفعل")
            Redis.set(f"{Fast}{sender_id}make:bot", "token")
            send(chat_id, msg_id, "\n✨ ارسل توكن البوت الان", "md", True)
            return False

        if text == "✨ حذف البوت":
            if r_get(f"{Fast}{sender_id}botuser"):
                botuser = r_get(f"{Fast}{sender_id}botuser")
                try:
                    user_obj = bot.getUser(sender_id)
                    dev_user = user_obj.get('username', '') if isinstance(user_obj, dict) else (getattr(user_obj, 'username', '') or '')
                except Exception:
                    dev_user = ""
                userinfo = bot.searchPublicChat(botuser)
                list_bots = r_smembers(f"{Fast}bots")
                if len(list_bots) > 0:
                    for v in list_bots:
                        if botuser in v:
                            Redis.srem(f"{Fast}bots", v)
                subprocess.run(f"rm -fr @{botuser}", shell=True)
                subprocess.run(f"screen -X -S {botuser} quit 2>/dev/null || true", shell=True)
                Redis.delete(f"{Fast}{sender_id}botuser")
                send(chat_id, msg_id, "\n✨ تم حذف البوت بنجاح", "md", True)
            else:
                send(chat_id, msg_id, "\n✨ عفوا لم تصنع اي بوت من قبل", "md", True)

# ------------------------------------------------------------------
# Update Callback Routing
# ------------------------------------------------------------------
def callback(data):
    if not isinstance(data, dict):
        return
    update_type = data.get("Fastbots") or data.get("@type")

    if update_type == "updateNewMessage":
        msg = data.get("message", {})
        sender = msg.get("sender_id", {}) if isinstance(msg, dict) else {}
        sender_user_id = sender.get("user_id") if isinstance(sender, dict) else 0
        if str(sender_user_id) == str(Fast):
            return False
        Run(msg, msg)

    elif update_type == "updateMessageEdited":
        chat_id = data.get("chat_id")
        msg_id = data.get("message_id")
        Message_Edit = bot.getMessage(chat_id, msg_id)
        if isinstance(Message_Edit, dict):
            sender = Message_Edit.get("sender_id", {})
            sender_user_id = sender.get("user_id") if isinstance(sender, dict) else 0
            if str(sender_user_id) == str(Fast):
                return False
            Run(Message_Edit, Message_Edit)

    elif update_type == "updateNewCallbackQuery":
        try:
            payload_data = data.get("payload", {}).get("data", "")
            Text = base64.b64decode(payload_data).decode('utf-8')
        except Exception:
            Text = ""
        IdUser = data.get("sender_user_id")
        ChatId = data.get("chat_id")
        Msg_id = data.get("message_id")
        # Answer the callback query to remove loading state
        bot.answerCallbackQuery(data.get("id", ""), text="")
        # Route callback as a message to Run()
        if Text:
            fake_msg = {
                "id": Msg_id,
                "chat_id": ChatId,
                "sender_id": {"user_id": IdUser},
                "content": {"text": {"text": Text}},
                "text": Text,
                "reply_to_message_id": 0,
            }
            Run(fake_msg, fake_msg)

# Startup environment checks
_screen_check = subprocess.run("which screen", shell=True, capture_output=True, text=True)
if _screen_check.returncode != 0:
    print("⚠️  WARNING: 'screen' is not installed! Bots won't start.")
    print("   Install it: apt install screen -y")
else:
    print(f"✅ screen found: {_screen_check.stdout.strip()}")

_ffmpeg_check = subprocess.run("which ffmpeg", shell=True, capture_output=True, text=True)
if _ffmpeg_check.returncode != 0:
    print("⚠️  WARNING: 'ffmpeg' is not installed! Music bots won't work.")
    print("   Install it: apt install ffmpeg -y")
else:
    print(f"✅ ffmpeg found: {_ffmpeg_check.stdout.strip()}")



# ------------------------------------------------------------------
# Error Handler & Auto-Restart for Main Bot
# ------------------------------------------------------------------
def send_error_to_admin(error_text):
    """Send error message to admin via Telegram Bot API"""
    try:
        import urllib.parse as _urlparse
        safe_text = _urlparse.quote(str(error_text)[:4000])
        requests.get(
            f"https://api.telegram.org/bot{Token}/sendMessage",
            params={"chat_id": Sudo_Id, "text": str(error_text)[:4000]},
            timeout=10
        )
    except Exception:
        pass

def run_with_retry(max_retries=2):
    """Run the main bot with auto-retry on crash"""
    for attempt in range(1, max_retries + 2):
        try:
            print(f"🚀 FastBots starting (attempt {attempt}/{max_retries + 1})...")
            bot.run(callback)
        except KeyboardInterrupt:
            print("\n⛔ FastBots stopped by user.")
            break
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            error_msg = f"⚠️ FastBots crashed (attempt {attempt}/{max_retries + 1})\n\nError: {str(e)[:500]}\n\n{error_details[:1500]}"
            print(error_msg)
            send_error_to_admin(error_msg)

            if attempt <= max_retries:
                print(f"⏳ Retrying in 5 seconds...")
                time.sleep(5)
            else:
                final_msg = f"❌ FastBots فشل يشغل بعد {max_retries + 1} محاولات\n\nآخر خطأ:\n{str(e)[:500]}"
                print(final_msg)
                send_error_to_admin(final_msg)

if __name__ == "__main__":
    run_with_retry()
