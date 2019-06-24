from discord.ext import commands
from discord.utils import get

TOKEN = "NTkxNzQ4MjIxNjYwMDM3MTIx.XRDDGQ.HoUqIoQC4sQsWHujm-NmGj0t1mw"
BETA_TOKEN = "NTkyMTE1NDM0NjQ4NjMzMzc3.XRDDLQ.1XeBSurLxlZT5EhI1fD7yO19_Mo"
bot = commands.Bot(command_prefix="")
TAG = "KSTA"


async def on_ksta(message):
    valid_channels = ["ksta"]
    role = get(message.guild.roles, name=TAG)
    member = message.author
    if str(message.channel) in valid_channels:
        if member == message.guild.owner:
            return
        if message.content.endswith(TAG):
            if valid_name_length(message.content):
                await member.add_roles(role)
                await member.edit(nick=message.content)
                await message.channel.send(message.author.mention + " твой ник был изменён на: `" +
                                           message.author.display_name + "` и тебе выдали роль " + role.name)
            else:
                await member.send("Желаемый ник слишком длинный")
                await message.channel.purge(limit=1)
        else:
            await message.channel.purge(limit=1)
            await member.send(
                "Для получения роли напиши свой никнейм Fortnite на канале ksta. Пример: ``Ник KSTA``\n" +
                "Если у тебя уже есть роль и ник, не пиши больше ничего :) Я всё равно всё почистию и уберу :)")


async def send_online():
    guilds = bot.guilds
    for guild in guilds:
        channel = get(guild.channels, name="hello")
        await channel.send("ONLINE")


def valid_name_length(name):
    return len(name) < 32


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await send_online()


@bot.event
async def on_message(message):
    # print(message.content)
    if message.author == bot.user:
        return
    await on_ksta(message)


@bot.event
async def on_member_remove(member):
    channel = get(member.guild.channels, name="hello")
    await channel.send(member.mention + "has left")


bot.run(TOKEN)