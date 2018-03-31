import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import random
import datetime
import sqlite3

coinconn = sqlite3.connect('coinStorage.db')
c = coinconn.cursor()


Client = discord.Client()
client = commands.Bot(command_prefix = "?")

@client.event
async def on_ready():
  print("Management || Bot is Online and ready.")
  await client.change_presence(game=discord.Game(name="Fire Mania Management | ?help"))


invBlacklist = []

numOfMessages = 0

@client.event

async def on_message_delete(message):
  logschannel = client.get_channel("429372917839822858")
  emb = (discord.Embed(description=None, colour=0xFF0000))
  emb.add_field(name="Message Deletion",value="A message was deleted in <#%s>" % (message.channel.id),inline=False)
  emb.add_field(name="Message created by", value="%s" % (message.author), inline=False)
  emb.add_field(name="Message", value="%s" % (message.content), inline=False)
  await client.send_message(logschannel, embed=emb)

@client.event 

async def on_message_edit(before, after):
  logschannel = client.get_channel("429372917839822858")
  emb = (discord.Embed(description=None, colour=0xFF0000))
  emb.add_field(name="Edited Message",value="A message was edited in <#%s>" % (after.channel.id),inline=False)
  emb.add_field(name="Message edited by", value="%s" % (after.author), inline=False)
  emb.add_field(name="Original Message", value="%s" % (before.content), inline=False)
  emb.add_field(name="Edited Message", value="%s" % (after.content), inline=False)
  await client.send_message(logschannel, embed=emb)
 
@client.event

async def on_message(message):
    numOfMessages +1
    if message.content.upper().startswith('?HELP'):
        emb = (discord.Embed(description=None, colour=0x3DF270))
        emb.add_field(name="Welcome to Fire Mania Management!",value="I am here to serve and protect this server. For version info, say `?version`. I am still being coded and I barely have commands, but that will change!",inline=False)
        print("%s ran the ?help command!" % (message.author.id))
        await client.send_message(message.channel, embed=emb)
    if message.content.upper().startswith('?VERSION') or message.content.upper().startswith('*VERSION') or message.content.upper().startswith('-VERSION') or message.content.upper().startswith('>VERSION'):
       emb = (discord.Embed(description=None, colour=0x3DF270))
       emb.add_field(name="Version", value="I am in Alpha stages. I am still being made and some features might not work.", inline=False)
       await client.send_message(message.channel, embed=emb)
       print("%s ran the ?version command!" % (message.author.id))
    if message.content.upper().startswith('?CHANNEL') or message.content.upper().startswith('*CHANNEL') or message.content.upper().startswith('-CHANNEL') or message.content.upper().startswith('>CHANNEL'):
          if "419904679124664321" in [role.id for role in message.author.roles]:
              await client.create_channel(message.server, "TEST", type=discord.ChannelType.text)
    if message.content.upper().startswith('?CREATE TEXT') or message.content.upper().startswith('*CREATE TEXT') or message.content.upper().startswith('-CREATE TEXT') or message.content.upper().startswith('>CREATE TEXT'):
        args = message.content.split(" ")
        if "419904679124664321" in [role.id for role in message.author.roles]:
                emb = (discord.Embed(description=None, colour=0x3DF270))
                emb.add_field(name="Successful Channel Creation", value="I created a text channel! Look for it on the side!", inline=False)
                await client.create_channel(message.server, " ".join(args[1:]), type=discord.ChannelType.text)
                await client.send_message(message.channel, embed=emb)
                print("%s ran the ?create text command!" % (message.author.id))
        else:
            emb = (discord.Embed(description=None, colour=0xff0000))
            emb.add_field(name="Failed Channel Creation", value="I failed to create a text channel! You do not have administrative previlages.", inline=False)
            await client.send_message(message.channel, embed=emb)
    if message.content.upper().startswith('?CREATE VOICE') or message.content.upper().startswith('*CREATE VOICE') or message.content.upper().startswith('-CREATE VOICE') or message.content.upper().startswith('>CREATE VOICE'):
        args = message.content.split(" ")
        if "419904679124664321" in [role.id for role in message.author.roles]:
                emb = (discord.Embed(description=None, colour=0x3DF270))
                emb.add_field(name="Successful Channel Creation", value="I created a voice channel! Look for it on the side!", inline=False)
                await client.create_channel(message.server, " ".join(args[1:]), type=discord.ChannelType.voice)
                await client.send_message(message.channel, embed=emb)
                print("%s ran the ?create voice command!" % (message.author.id))
        else:
            emb = (discord.Embed(description=None, colour=0xff0000))
            emb.add_field(name="Failed Channel Creation", value="I failed to create a voice channel! You do not have administrative previlages.", inline=False)
            await client.send_message(message.channel, embed=emb)
    if message.content.upper().startswith('?INVITE') or message.content.upper().startswith('*INVITE') or message.content.upper().startswith('-INVITE') or message.content.upper().startswith('>INVITE'):
       perms = True
       for item in invBlacklist:
         if item == message.author.id:
           perms = False
       if perms == True:
          invite = await client.create_invite(destination = message.channel, xkcd = True, max_uses = 1)
          await client.send_message(message.channel, ":white_check_mark: Invite your friend with this invite! Note that it can ONLY be used once. Here's the invite: %s" % (invite))
       elif perms == False:
          await client.send_message(message.channel, "<@%s> :x: You have been blacklisted from creating invites. If this is a mistake, please mention/message a Bot Administrator" % (message.author.id))
    if message.content.upper().startswith('?VIEWINVITE') or message.content.upper().startswith('*VIEWINVITE') or message.content.upper().startswith('-VIEWINVITE') or message.content.upper().startswith('?VIEWINVITE'):
       if "419904679124664321" in [role.id for role in message.author.roles]:
          args = message.content.split(" ")
          invite12 = await client.get_invite("http://discord.gg/%s" % " ".join(args[1:]))
          created = invite12.created_at
          emb = (discord.Embed(description=None, colour=0x3DF270))
          emb.add_field(name="Viewing invite information for %s" % (" ".join(args[1:])), value="%s" % (" ".join(args[1:])), inline=False)
          emb.add_field(name="Channel", value="#%s" % (invite12.channel), inline=False)
          emb.add_field(name="Uses", value="%s" % (invite12.uses), inline=False)
          await client.send_message(message.channel, embed=emb)
       else:
          await client.send_message(message.channel, "<@%s> :x: You are not an admin and cannot run this command!" % (message.author.id))
    if message.content.upper().startswith('?INVBLOCK') or message.content.upper().startswith('*INVBLOCK') or message.content.upper().startswith('-INVBLOCK') or message.content.upper().startswith('>INVBLOCK'):
       if "419904679124664321" in [role.id for role in message.author.roles]:
          perms = True
          for item in invBlacklist:
            if item == message.author.id:
               perms = False
          if perms == False:
             await client.send_message(message.channel, "<@%s> :x: That user is already blacklisted!" % (message.author.id))
          elif perms == True:
             args = message.content.split(" ")
             mentionID = message.mentions[0].id
             invBlacklist.append(mentionID)
             await client.send_message(message.channel, ":white_check_mark: <@%s> %s has been blacklisted from creating invites!" % (message.author.id, mentionID))
       else:
          await client.send_message(message.channel, "<@%s> :x: You are not an admin and cannot run this command!" % (message.author.id))
    if message.content.upper().startswith('?INVWHITELIST') or message.content.upper().startswith('*INVWHITELIST') or message.content.upper().startswith('-INVWHITELIST') or message.content.upper().startswith('>INVWHITELIST'):
       if "419904679124664321" in [role.id for role in message.author.roles]:
          perms = True
          for item in invBlacklist:
            if item == message.author.id:
               perms = False
          if perms == True:
             await client.send_message(message.channel, "<@%s> :x: That user is not blacklisted!" % (message.author.id))
          elif perms == False:
             args = message.content.split(" ")
             mentionID = message.mentions[0].id
             invBlacklist.remove(mentionID)
             await client.send_message(message.channel, ":white_check_mark: <@%s> %s has been whitelisted and can now create invites!" % (message.author.id, mentionID))
       else:
          await client.send_message(message.channel, "<@%s> :x: You are not an admin and cannot run this command!" % (message.author.id))
    if message.content.upper().startswith('?INVBLACKLIST') or message.content.upper().startswith('*INVBLACKLIST') or message.content.upper().startswith('-INVBLACKLIST') or message.content.upper().startswith('>INVBLACKLIST'):
       if "419904679124664321" in [role.id for role in message.author.roles]:
         await client.send_message(message.channel, ":white_check_mark: <@%s> The following people are blacklisted from creating invites: %s" % (message.author.id, ", ".join(invBlacklist)))
       else:
         await client.send_message(message.channel, "<@%s> :x: You are not an admin and cannot run this command!" % (message.author.id))
    if message.content.upper().startswith('?8BALL') or message.content.upper().startswith('*8BALL') or message.content.upper().startswith('-8BALL') or message.content.upper().startswith('>8BALL'):
        userID = message.author.id
        randnum = random.randint(1,11)
        if randnum == 1:
            await client.send_message(message.channel,"<@%s> :8ball: It is likely. :8ball:" % (userID))
        if randnum == 2:
            await client.send_message(message.channel, "<@%s> :8ball: I am afraid not. :8ball:" % (userID))
        if randnum == 3:
            await client.send_message(message.channel, "<@%s> :8ball: I do not see it in the future. :8ball:" % (userID))
        if randnum == 4:
            await client.send_message(message.channel, "<@%s> :8ball: Very possible. :8ball:" % (userID))
        if randnum == 5:
            await client.send_message(message.channel, "<@%s> :8ball: There is a very bad chance. :8ball:" % (userID))
        if randnum == 6:
            await client.send_message(message.channel, "<@%s> :8ball: I see it in the future. :8ball:" % (userID))
        if randnum == 7:
            await client.send_message(message.channel, "<@%s> :8ball: There is an great chance. :8ball:" % (userID))
        if randnum == 8:
            await client.send_message(message.channel, "<@%s> :8ball: I do not see this happening. :8ball:" % (userID))
        if randnum == 9:
            await client.send_message(message.channel, "<@%s> :8ball: I see something positive. :8ball:" % (userID))
        if randnum == 10:
            await client.send_message(message.channel, "<@%s> :8ball: I don't see it. You may as well walk away. :8ball:" % (userID))
    if message.content.upper().startswith('?COOKIE') or message.content.upper().startswith('*COOKIE') or message.content.upper().startswith('-COOKIE') or message.content.upper().startswith('>COOKIE'):
       userID = message.author.id
       mentionID = message.mentions[0].id
       if userID == mentionID:
         await client.send_message(message.channel, "<@%s> decided to take all the cookies! How dare they?!?!! :cookie:" % (userID))
       elif mentionID != "419904091607662592":
         await client.send_message(message.channel, "<@%s> gave <@%s> a cookie! How *sweet*! :cookie:" % (userID, mentionID))
       elif mentionID == "419904091607662592":
         await client.send_message(message.channel, "<@%s> gave me a cookie! ME? ME!? ME?!? What did I do to deserve this? :cookie:" % (userID))
         await client.add_reaction(message, "\U0001F1F9")
         await client.add_reaction(message, "\U0001F1ED")
         await client.add_reaction(message, "\U0001F1FD")
    if message.content.upper().startswith('?HUG') or message.content.upper().startswith('*HUG') or message.content.upper().startswith('-HUG') or message.content.upper().startswith('>HUG'):
       userID = message.author.id
       mentionID = message.mentions[0].id
       if userID == mentionID:
         await client.send_message(message.channel, "<@%s>, you have more friends than that! Right? Right? Right?!?! :revolving_hearts:" % (userID))
       elif mentionID != "419904091607662592":
         await client.send_message(message.channel, "<@%s> gave <@%s> a hug! How thoughtful?! :revolving_hearts:" % (userID, mentionID))
       elif mentionID == "419904091607662592":
         await client.send_message(message.channel, "<@%s>, are you being serious? I LOVE HUGS!!!!!!!!! :revolving_hearts:" % (userID))
         await client.add_reaction(message, "\u2665")
    if message.content.upper().startswith('?PUNCH') or message.content.upper().startswith('*PUNCH') or message.content.upper().startswith('-PUNCH') or message.content.upper().startswith('>PUNCH'):
       userID = message.author.id
       mentionID = message.mentions[0].id
       if userID == mentionID:
         await client.send_message(message.channel, "<@%s>, you have punched yourself. Niceeeeeeeeeeeeeeeeeee choice. :face_palm:" % (userID))
       elif mentionID != "419904091607662592":
         await client.send_message(message.channel, "<@%s> punched <@%s>! I honestly don't care but be warned that this could turn into a war. :face_palm:" % (userID, mentionID))
       elif mentionID == "419904091607662592":
         await client.send_message(message.channel, "<@%s>, NO NO NO NO NO NO NO NO NO. Don't do it. :face_palm:" % (userID))
         await client.add_reaction(message, "\U0001F1F3")
         await client.add_reaction(message, "\U0001F1F4")
    if message.content.upper().startswith('?SLAP') or message.content.upper().startswith('*SLAP') or message.content.upper().startswith('-SLAP') or message.content.upper().startswith('>SLAP'):
       userID = message.author.id
       mentionID = message.mentions[0].id
       if userID == mentionID:
         await client.send_message(message.channel, "<@%s>, you have slapped yourself. Do you think you're dreaming or something? :cloud_lightning:" % (userID))
       elif mentionID != "419904091607662592":
         await client.send_message(message.channel, "<@%s> punched <@%s>! Better knock some sense into him/her! :cloud_lightning:" % (userID, mentionID))
       elif mentionID == "419904091607662592":
         await client.send_message(message.channel, "<@%s>, what did I do to deserve this?? I am just programmed to do stuff OKAY?!?! :cloud_lightning:" % (userID))
         await client.add_reaction(message, "\U0001F620")
    if message.content.upper().startswith('?SUBSCRIBE') or message.content.upper().startswith('*SUBSCRIBE') or message.content.upper().startswith('-SUBSCRIBE') or message.content.upper().startswith('>SUBSCRIBE'):
      if "427167017917743114" in [role.id for role in message.author.roles]:
         await client.send_message(message.channel, "<@%s> :x: You are already a subscriber!" % (message.author.id))
      else:
         sub = discord.utils.get(message.server.roles, name="Subscriber")
         await client.add_roles(message.author, sub)
         await client.send_message(message.channel, "<@%s> :white_check_mark: You are now a subscriber and will be pinged when there is an announcement!" % (message.author.id))
    if message.content.upper().startswith('?UNSUBSCRIBE'):
            if "427167017917743114" in [role.id for role in message.author.roles]:
              sub = discord.utils.get(message.server.roles, name="Subscriber")
              await client.remove_roles(message.author, sub)
              await client.send_message(message.channel, "<@%s> :white_check_mark: You are no longer a subscriber and will not be pinged when there is an announcement." % (message.author.id))
            else:
              await client.send_message(message.channel, "<@%s> :x: You aren't a subscriber! Run `?subscribe` to be subscribed to #announcements!" % (message.author.id))
    if message.content.upper().startswith('?KICK'):
          if "419904679124664321" in [role.id for role in message.author.roles]:
            await client.send_message(message.channel, "<@%s> :white_check_mark: You have kicked <@%s> successfully." % (message.author.id, message.mentions[0].id))
            await client.kick(message.mentions[0])
          else:
            await client.send_message(message.channel, "<@%s> :x: You are not an admin and cannot run this command!" % (message.author.id))
    if message.content.upper().startswith('?BAN'):
          if "419904679124664321" in [role.id for role in message.author.roles]:
            await client.send_message(message.channel, "<@%s> :white_check_mark: You have banned <@%s> successfully." % (message.author.id, message.mentions[0].id))
            await client.ban(message.mentions[0], delete_message_days=7)
          else:
            await client.send_message(message.channel, "<@%s> :x: You are not an admin and cannot run this command!" % (message.author.id))
    if message.content.upper().startswith('?MUTE'):
      if "419904679124664321" in [role.id for role in message.author.roles]:
         muted = discord.utils.get(message.server.roles, name="Muted")
         await client.add_roles(message.mentions[0], muted)
         await client.send_message(message.channel, "<@%s> :white_check_mark: You have muted <@%s>! Run `?unmute @user` to unmute this user!" % (message.author.id, message.mentions[0].id))
      else:
         await client.send_message(message.channel, "<@%s> :x: You are not an admin and cannot run that command!" % (message.author.id))
    if message.content.upper().startswith('?UNBAN'):
          args = message.content.split(" ")
          if "419904679124664321" in [role.id for role in message.author.roles]:
            uid = " ".join(args[1:])
            await client.send_message(message.channel, "<@%s> :white_check_mark: You have unbanned %s successfully." % (message.author.id, uid))
            await client.unban(message.server, client.get_user_info(uid))
          else:
            await client.send_message(message.channel, "<@%s> :x: You are not an admin and cannot run this command!" % (message.author.id))
    if message.content.upper().startswith('?UNMUTE'):
      if "419904679124664321" in [role.id for role in message.author.roles]:
         muted = discord.utils.get(message.server.roles, name="Muted")
         await client.remove_roles(message.mentions[0], muted)
         await client.send_message(message.channel, "<@%s> :white_check_mark: You have unmuted <@%s>! Made a mistake? Use `?mute @user`" % (message.author.id, message.mentions[0].id))
      else:
         await client.send_message(message.channel, "<@%s> :x: You are not an admin and cannot run that command!" % (message.author.id))
    if message.content.upper().startswith('?ANNOUNCE'):
      if "419904679124664321" in [role.id for role in message.author.roles]:
         args = message.content.split(" ")
         announcechannel = client.get_channel("419590200805687296")
         emb = (discord.Embed(description=None, colour=0xFFA500))
         emb.add_field(name="Announcement by %s" % (message.author), value="%s" % (" ".join(args[1:])), inline=False)
         await client.send_message(announcechannel, "<@&427167017917743114>")
         await client.send_message(announcechannel, embed=emb)
      else:
         await client.send_message(message.channel, "<@%s> :x: You are not an admin and cannot run that command!" % (message.author.id))
    if message.content.upper().startswith('?PIN'):
      if "419904679124664321" in [role.id for role in message.author.roles]:
        args = message.content.split(" ")
        msg = await client.get_message(message.channel, " ".join(args[1:]))
        await client.pin_message(msg)
        emb = (discord.Embed(description=None, colour=0x3DF270))
        emb.add_field(name="Success", value="You have pinned the message id `%s`." % (" ".join(args[1:])), inline=False)
        await client.send_message(message.channel, embed=emb)
      else:
        emb = (discord.Embed(description=None, colour=0xFF0000))
        emb.add_field(name="Task Failure", value="You are not an admin and cannot do this!", inline=False)
        await client.send_message(message.channel, embed=emb)
    if message.content.upper().startswith('?SET'):
       c.execute("CREATE TABLE IF NOT EXISTS coinStorage(user TEXT, coins INTEGER)")
       emb = (discord.Embed(description=None, colour=0x3DF270))
       emb.add_field(name="Success", value="You have added a table to the Coin Storage Database!", inline=False)
       await client.send_message(message.channel, embed=emb)
    if message.content.upper().startswith('?REGISTER'):
       user = str(message.author)
       val = int(1000)
       c.execute("INSERT INTO coinStorage VALUES (?, ?)",
          (user, val))
       coinconn.commit()
       emb = (discord.Embed(description=None, colour=0x3DF270))
       emb.add_field(name="Success", value="You have registered yourself to the Coin Storage Database! User: `%s` | Coins: `1000`" % (message.author), inline=False)
       await client.send_message(message.channel, embed=emb)
    if message.content.upper().startswith('?COINS'):
           c.execute('SELECT * FROM coinStorage')
           data = c.fetchall()
           for row in data:
              if row[0] == str(message.author):
                 emb = (discord.Embed(description=None, colour=0x3DF270))
                 emb.add_field(name="Coins", value="You have %s coins!" % (row[1]), inline=False)
                 await client.send_message(message.channel, embed=emb)

client.run("NDE5OTA0MDkxNjA3NjYyNTky.DX27wA.zctI11rIHCQlRQVGYOXGqDSLhNs")
