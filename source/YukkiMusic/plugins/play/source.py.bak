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
        photo=f"https://telegra.ph/file/1a3b073913ee104c8339b.jpg",
        caption=f"""╭━━━═[𝐓𝐇𝐑𝐄𝐄 𝐓𝐇𝐔𝐍](https://t.me/CCYFC)═━━━╮
➤[𝐀𝐒𝐊.𝐓𝐎 𝐌𝐄](https://t.me/TT_LLJ)
➤[𝗛َِ𝗮َِ𝗶َِ𝗱َِ𝗲َِ𝗿](https://t.me/TT_LLJ)
╰━━━═[𝐓𝐇𝐑𝐄𝐄 𝐓𝐇𝐔𝐍](https://t.me/CCYFC)═━━━╯""",
        reply_markup=InlineKeyboardMarkup(
             [
                 [
                 InlineKeyboardButton(
                        "˛ َِ𝗛َِ𝗮َِ𝗶َِ𝗱َِ𝗲َِ𝗿 .👑", url=f"https://t.me/TT_LLJ")
                 ],   
                 [    
                    InlineKeyboardButton(
                        "𝐓𝐇𝐑𝐄𝐄 𝐓𝐇𝐔𝐍", url=f"https://t.me/CCYFC")
                 ],   
                 [    
                    InlineKeyboardButton(
                        "اضف البوت ف جروبك ✨️", url=f"https://t.me/KiMY_X_bot?startgroup=true")
                 ],
             ]
            ),
    )
  
  
  
  
  
  
@app.on_message(
    command(["حيدر"])
    & filters.group
    & ~filters.edited
)
async def yas(client, message):
    usr = await client.get_chat("TT_LLJ")
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
