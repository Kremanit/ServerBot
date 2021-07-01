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

@client.command()

async def pidors(ctx,member:discord.Member = None, guild: discord.Guild = None):
	await ctx.message.delete()

	emb = discord.Embed( title = 'ГЛАВНЫЕ ПИДОРАСЫ СЕРВЕРА', colour = discord.Color.purple() )

	emb.add_field( name = f'артем', value = '```ПИДОР```' )
	emb.add_field( name = f'пика', value = '```ПИДОР```' )
	emb.add_field( name = f'олег', value = '```ПИДОР```' )
	emb.add_field( name = f'эдик', value = '```ПИДОР```' )
	emb.add_field( name = f'артем', value = '```ПИДОР```' )
 	
	await ctx.send( embed = emb )

@client.command()
async def pizdec(ctx):
    await ctx.send('Реально пиздец')

#Command help
@client.command( pass_context = True )

async def help( ctx ):
	await ctx.channel.purge( limit = 1 )

	emb = discord.Embed( title = 'Навигация по командам', colour = discord.Color.orange() )

	emb.add_field( name = f'{prefix}clear', value = '```Очистить чат```' )
	emb.add_field( name = f'{prefix}kick', value = '```Выгнать участника```' )
	emb.add_field( name = f'{prefix}ban', value = '```Забанить участника```' )
	emb.add_field( name = f'{prefix}time', value = '```Посмотреть время```' )
	emb.add_field( name = f'{prefix}pidors', value = '```Узнать пидоров сервера```' )
	emb.add_field( name = f'{prefix}pizdec', value = '```Ещё чё то```' )

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
		    d = "🟢В сети"

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


@client.command()
@commands.has_permissions( administrator = True )
async def mtm(ctx):
    for channel in ctx.guild.voice_channels:
        for member in channel.members:
            await member.move_to(ctx.author.voice.channel)


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
