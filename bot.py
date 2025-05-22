import asyncio
from os import environ
from pyrogram import Client, filters, idle
from pyrogram.errors import FloodWait
from subprocess import Popen

API_ID = int(environ.get("API_ID"))
API_HASH = environ.get("API_HASH")
BOT_TOKEN = environ.get("BOT_TOKEN")
SESSION = environ.get("SESSION")
TIME = int(environ.get("TIME"))
PORT = 8080
GROUPS = []
for grp in environ.get("GROUPS").split():
    GROUPS.append(int(grp))
ADMINS = []
for usr in environ.get("ADMINS").split():
    ADMINS.append(int(usr))

START_MSG = "<b>Hey!! {},\nI'm a private bot of @MM_Films to delete group messages after a specific time \nTo create your own bot contact @Lexi_Tvd</b>"


User = Client(name="user-account",
              session_string=SESSION,
              api_id=API_ID,
              api_hash=API_HASH,
              workers=300
              )


Bot = Client(name="auto-delete",
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=300
             )


@Bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(START_MSG.format(message.from_user.mention))

@User.on_message(filters.chat(GROUPS))
async def delete(user, message):
    try:
       if message.from_user.id in ADMINS:
          return
       else:
          await asyncio.sleep(TIME)
          await Bot.delete_messages(message.chat.id, message.id)
    except FloodWait as e:
        print(f"Rate limit hit. Sleeping for {e.x} seconds.")
        await asyncio.sleep(e.x) 
        await Bot.delete_messages(message.chat.id, message.id)
    except Exception as e:
       print(e)
Popen(f"gunicorn utils.server:app --bind 0.0.0.0:{PORT}", shell=True)      
User.start()
print("User Started!")
Bot.start()
print("Bot Started!")

idle()

User.stop()
print("User Stopped!")
Bot.stop()
print("Bot Stopped!")
