import asyncio
from pyrogram import Client, filters
from strings import get_command
from strings.filters import command
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from YukkiMusic import app
from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_USER = getenv("BOT_USER")

@app.on_message(
    command(["سورس مين","سورس","السورس","يا سورس"])
    & ~filters.edited
)
async def taiger(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://t.me/QA_Z1O/6",
        caption=f"""╭━━━═[𝐒𝐨𝐮𝐫𝐜𝐞 𝐓𝐰𝐢𝐧𝐬](https://t.me/SOURCE_TWINS1)═━━━╮
➤[𝐀𝐒𝐊.𝐓𝐎 𝐌𝐄](https://t.me/BE_MO4)
➤[SPIDER](https://t.me/BE_MO4)
╰━━━═[𝐓𝐇𝐑𝐄𝐄 𝐓𝐇𝐔𝐍](https://t.me/SOURCE_TWINS1)═━━━╯""",
        reply_markup=InlineKeyboardMarkup(
             [
                 [
                 InlineKeyboardButton(
                        "˛ َِspider .👑", url=f"https://t.me/BE_MO4")
                 ],   
                 [    
                    InlineKeyboardButton(
                        "𝐒𝐨𝐮𝐫𝐜𝐞 𝐓𝐰𝐢𝐧𝐬", url=f"https://t.me/SOURCE_TWINS1")
                 ],   
                 [    
                    InlineKeyboardButton(
                        "اضف البوت ف جروبك ✨️", url=f"https://t.me/TWINS_MISCBO?startgroup=true")
                 ],
             ]
            ),
    )
  
  
  
  
  
  
@app.on_message(
    command(["توينز"])
    & filters.group
    & ~filters.edited
)
async def yas(client, message):
    usr = await client.get_chat("BE_MO4")
    name = usr.first_name
    photo = await app.download_media(usr.photo.big_file_id)
    await message.reply_photo(photo,       caption=f"**🧞‍♂️ ¦𝙺𝙸𝙽𝙶 :{name}\n🎯 ¦𝚄𝚂𝙴𝚁 :@{usr.username}\n💣 ¦𝙸𝙳 :`{usr.id}`\n🚀 ¦𝙱𝙸𝙾 :{usr.bio}\n", 
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        name, url=f"https://t.me/{usr.username}")
                ],
            ]
        ),
    )
