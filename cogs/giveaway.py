import discord
import asyncio
import random

from discord.ext import commands

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

class Giveaway(commands.Cog):
    """Создание розыгрышей/конкурсов"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['giveaway', 'розыгрыш'])
    @commands.has_permissions(administrator = True)
    async def giveaway_command(self, ctx, winners = None, giveaway_time = None, *, text):
        counter = 0
        time_rotation = {
            's': '1',
            'm': '60',
            'h': '3600',
            'd': '86400',
            'w': '604800'
        }
        winners_text = 'Победители'
        top_places = ''
        alternative_time = ''
        if int(winners) > 0 and giveaway_time != None and text != None: # Если победителей > 0, есть время и есть текст
            for s in giveaway_time: # Раскладываем переменную giveaway_time на буквы
                if s.lower() in time_rotation: # Проверяем есть ли в переменной giveaway_time буква совпадающающая со словарём time_rotation
                    intermediate_time = time_rotation[s.lower()] # Если такая буква есть, заносим её в новую переменную
                else:
                    alternative_time += f'{s}'
            if int(alternative_time) <= 0:
                alternative_time = 1
            final_time = int(alternative_time) * int(intermediate_time)
            end_time_str = display_time(final_time, 5)
            emb = discord.Embed(title = "🎉Розыгрыш начался🎉", description = f"**Внимание розыгрыш!\n\n{text}\n\nНажмите на реакцию ниже, чтобы принять участие**\nСпасибо <@{ctx.message.author.id}> за розыгрыш")
            emb.set_footer(text = f"{winners_text}: {winners} | Конец через {end_time_str}")
            message = await ctx.send(embed = emb)
            await message.add_reaction('🎫') # Добавляем емодзи
            await asyncio.sleep(final_time) # Асинхронное ожидание в секундах
            mess = await ctx.channel.fetch_message(message.id)
            winner_array = []
            for reaction in mess.reactions:
                if reaction.emoji == '🎫':
                    users = await reaction.users().flatten()
            if len(users) > 1:
                users.pop(0)
            while len(winner_array) < int(winners):
                winner = random.choice(users)
                if len(winner_array) >= len(users):
                    winner_array.append('Не удалось найти участника')
                elif winner in winner_array:
                    winner = random.choice(users)
                else:
                    winner_array.append(winner)
            while counter < int(winners):
                top_places += f'{counter + 1}) {winner_array[counter]}\n'
                counter += 1
            emb_final = discord.Embed(title = "🎉Розыгрыш закончился🎉", description = f"**Внимание розыгрыш закончился!\n\n{text}\n\nПобедители:\n{top_places}**\nСпасибо <@{ctx.message.author.id}> за розыгрыш")
            emb_final.set_footer(text = f"{winners_text}: {winners} | Закончился")

            await message.edit(embed = emb_final)

    @giveaway_command.error
    async def giveaway_command_error(self, ctx, error):
        if isinstance (error, commands.MissingRequiredArgument): # Если нехватает аргументов
            emb = discord.Embed(title = 'Помощник - Розыгрыши', color = 0x30DD30)
            emb.add_field(name = 'Использование', value = f'`?розыгрыш <кол-во победителей> <время> <приз>`\n┗ Создаст розыгрыш от вашего лица на определенное время.', inline = False)
            emb.add_field(name = 'Пример', value = f'`?розыгрыш 1 1d 1 Место: 1000 рублей`\n┗ Создаст розыгрыш на 1 день для 1 победителя', inline = False)
            emb.add_field(name = 'Примечание', value = f'Время розыгрыша не может бысть указано в месяцах/годах', inline = False)
            emb.set_footer(text = 'Kremanit © 2021', icon_url = self.bot.user.avatar_url)
            emb.set_thumbnail(url = 'https://www.flaticon.com/premium-icon/icons/svg/2867/2429310.svg')
            await ctx.send(embed = emb)

def setup(bot):
    bot.add_cog(Giveaway(bot))
