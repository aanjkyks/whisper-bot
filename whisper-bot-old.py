import discord
from discord.utils import get

TOKEN = "NTkxNzQ4MjIxNjYwMDM3MTIx.XQ3h0g.tZeoZvrQtfo92VX4iPypChnPuzE"
BETA_TOKEN = "NTkyMTE1NDM0NjQ4NjMzMzc3.XQ6ofQ.VyiD2DCfIGw4LeJHo7Frstu7YWw"
client = discord.Client()
TAG = "KSTA"


async def on_ksta(message):
    guild = message.guild
    valid_channels = ["ksta"]
    channel = message.channel

    if str(message.channel) in valid_channels:
        if str(message.content).endswith(TAG):
            member = message.author
            role = get(guild.roles, name=TAG)
            if member != guild.owner:
                await member.edit(nick=message.content)
            if (role in member.roles) == False:
                await member.add_roles(role)
            await channel.send(
                member.mention + " твой ник был изменён на: `" + member.display_name + "` и тебе выдали роль " + role.name)
        elif message.author != guild.owner:
            await message.channel.purge(limit=1)
            await message.author.send("Для получения роли напиши свой никнейм Fortnite на канале ksta. Пример: ``Ник KSTA``\nЕсли у тебя уже есть роль и ник, не пиши больше ничего :) Я всё равно всё почистию и уберу :)")


async def send_online():
    guilds = client.guilds
    for guild in guilds:
        channel = get(guild.channels, name="hello")
        await channel.send("ONLINE")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await send_online()


@client.event
async def on_message(message):
    # print(message.content)
    if message.author == client.user:
        return
    await on_ksta(message)


@client.event
async def on_member_remove(member):
    guild = member.guild
    channel = get(guild.channels, name="hello")
    await channel.send(member.mention + "has left")


client.run(TOKEN)