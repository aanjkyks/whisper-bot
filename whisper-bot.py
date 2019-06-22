import discord

TOKEN = "NTkxNzQ4MjIxNjYwMDM3MTIx.XQ3h0g.tZeoZvrQtfo92VX4iPypChnPuzE"
client = discord.Client()
SERVER_ID = 432275330498035734
ROLE_ID = 591909793074249756
TAG = "KSTA"


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        return
    guild = client.get_guild(SERVER_ID)
    valid_channels = ["ksta"]
    channel = message.channel

    if str(message.channel) in valid_channels:
        if str(message.content).endswith("KSTA"):
            member = message.author
            role = guild.get_role(ROLE_ID)
            await member.edit(nick=message.content)
            if (role in member.roles) != 1:
                await member.add_roles(role)
            await channel.send(member.mention + " your name was changed to `" + str(
                message.content) + "` and you were given a role " + role.mention)
        else:
            await message.channel.purge(limit=1)


client.run(TOKEN)
