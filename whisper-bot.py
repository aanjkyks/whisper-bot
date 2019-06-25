from discord.ext import commands, tasks
from discord.utils import get
from twitch import TwitchClient

TOKEN = "NTkxNzQ4MjIxNjYwMDM3MTIx.XRDVhw.iYuN5oCnoNTJ6jJ3asnzWEah9VA"
BETA_TOKEN = "NTkyMTE1NDM0NjQ4NjMzMzc3.XRDVow.uLRgLUP57oNZJ_V7w483W3DcNzM"
TWITCH_TOKEN = "i9m0l8qx20imglck9nifgc43p6lc4b"
bot = commands.Bot(command_prefix="")
TAG = "KSTA"
client = TwitchClient(client_id=TWITCH_TOKEN)
TWITCH_CHANNEL = get(client.search.channels('ivanwhisper'), name="ivanwhisper")


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


async def send_stream_notification(stream, channel):
    await channel.send(
        "@everyone " + stream.channel.display_name + " Стримит прямо сейчас! " + stream.channel.status + " Попасть на стрим можно здесь: " + stream.channel.url)


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


class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notifier.start()
        self.offline = True

    def cog_unload(self):
        self.notifier.cancel()

    @tasks.loop(minutes=10)
    async def notifier(self):
        for guild in self.bot.guilds:
            stream = client.streams.get_stream_by_user(TWITCH_CHANNEL.id)
            if not stream is None:
                if self.offline:
                    channel = get(guild.channels, name="hello")
                    await send_stream_notification(stream, channel)
                    self.offline = False
            else:
                self.offline = True

    @notifier.before_loop
    async def before_notifier(self):
        print("waiting...")
        await self.bot.wait_until_ready()


bot.add_cog(MyCog(bot))
bot.run(TOKEN)
