import os, logging, asyncio

from telegraph import upload_file

from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
ankit = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token) 

moment_worker = []


#start
@ankit.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("^_^ Hey, Welcome To TAG Help Bot's Menu\nI can tag 15,000 Members in Group and 300 Members In Channel.\nNeed Help /help ",
                    buttons=(
                      [
                         Button.url('⭕Developer⭕', 'https://github.com/ANKIT-OS'), 
                         Button.url('🔰©ANKIT-OS™🔰', 'https://github.com/ANKIT-OS'), 
                      ], 
                      [
                        Button.url('💫Repo💫', 'https://github.com/ANKIT-OS/TAGGERBOT'),   
                      ]
                   ),
                    link_preview=False
                   )

#help
@ankit.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Tag Help Bot's Help Menu**\n\nCommand: /all \n You can use this command with text you want to tell others. \n`Example: /all Legend's Say's To ©ANKIT-OS™!` \nYou can use this command as an answer. any message Bot will tag users to replied message"
  await event.reply(helptext,
                    buttons=(
                      [
                         Button.url('⭕Developer⭕', 'https://github.com/ANKIT-OS'), 
                         Button.url('🔰©ANKIT-OS™🔰', 'https://github.com/ANKIT-OS'), 
                      ], 
                      [
                        Button.url('💫Repo💫', 'https://github.com/ANKIT-OS/TAGGERBOT'),   
                      ]
                   ), 
                    link_preview=False
                   )

#Wah bhaiya full ignorebazzi
#Credit dedena ©ANKIT-OS™

#tag
@ankit.on(events.NewMessage(pattern="^/tagall|/call|/tall|/all|#all|@all?(.*)"))
async def mentionall(event):
  global moment_worker
  if event.is_private:
    return await event.respond("Use This In Channel or Group!")
  
  admins = []
  async for admin in ankitbot.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("Only Admin can use it.")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("I can't Mention Members for Old Post!")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("Give me can an Argument. Ex: `/tag Hey, Where are you`")
  else:
    return await event.respond("Reply to Message or Give Some Text To Mention!")
    
  if mode == "text_on_cmd":
    moment_worker.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in ankitbot.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in moment_worker:
        await event.respond("Stopped!")
        return
      if usrnum == 5:
        await ankit.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    moment_worker.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in ankit.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in moment_worker:
        await event.respond("Stopped")
        return
      if usrnum == 5:
        await ankit.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


# Cancel

@ankit.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('__There is no proccess on going...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('**__Stoped__**\n\n**__Powered By:__ https://github.com/ANKIT-OS **')





print("Started Successfully Follow Me On Github")
print("¯\_(ツ)_/¯ Need Help https://github.com/ANKIT-OS")
ankit.run_until_disconnected()
