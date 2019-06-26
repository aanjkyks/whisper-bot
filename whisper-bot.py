import asyncio
import urllib.parse

from discord.ext import commands, tasks
from discord.utils import get
from fortnite_python import Fortnite
from fortnite_python.exceptions import UnknownPlayerError
from twitch import TwitchClient


def file_reader(filename):
    file = open(filename)
    content = file.read()
    return content


TOKEN = file_reader("token.txt")
BETA_TOKEN = file_reader("beta-token.txt")
TWITCH_TOKEN = file_reader("twitch-token.txt")
FORTNITE_API_KEY = file_reader("fortnite-token.txt")
LOG_CHANNEL_NAME = "logs"

bot = commands.Bot(command_prefix="")
TAG = "KSTA"
client = TwitchClient(client_id=TWITCH_TOKEN)
TWITCH_CHANNEL = get(client.search.channels('ivanwhisper'), name="ivanwhisper")
fortnite = Fortnite(FORTNITE_API_KEY)


async def on_ksta(message):
    valid_channels = ["ksta"]
    role = get(message.guild.roles, name=TAG)
    member = message.author
    if str(message.channel) in valid_channels:
        if member == message.guild.owner:
            return
        if message.content.endswith(TAG):
            if valid_name_length(message.content):
                try:
                    player = fortnite.player(message.content)
                except UnknownPlayerError:
                    player = None
                except:
                    channel = get(message.guild.channels, name=LOG_CHANNEL_NAME)
                    await channel.send("Error accessing fortnite-tracker API")
                    return
                if player is not None:
                    await member.add_roles(role)
                    await member.edit(nick=message.content)
                    await message.channel.send(message.author.mention + " твой ник был изменён на: `" +
                                               message.content + "` и тебе выдали роль " + role.name)
                else:
                    await message.author.send(
                        "Ник не найден. Попробуй снова, когда сможешь себя найти здесь: " +
                        "https://fortnitetracker.com/profile/pc/" + urllib.parse.quote(message.content))
                    await message.channel.purge(limit=1)
            else:
                await member.send("Желаемый ник слишком длинный")
                await message.channel.purge(limit=1)
        else:
            await message.channel.purge(limit=1)
            await member.send(
                "Для получения роли напиши свой никнейм Fortnite на канале " + message.channel.mention +
                ". Пример: ``Ник " "KSTA``\n" +
                "Если у тебя уже есть роль и ник, не пиши больше ничего :) Я всё равно всё почистию и уберу :)")


async def send_online():
    guilds = bot.guilds
    for guild in guilds:
        channel = get(guild.channels, name=LOG_CHANNEL_NAME)
        await channel.send("ONLINE")


async def send_stream_notification(stream, channel):
    await channel.send(
        "@everyone " + stream.channel.display_name + " Стримит прямо сейчас! " + stream.channel.status +
        " Попасть на стрим можно здесь: " + stream.channel.url)


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
        self.offline = True
        self.notifier.start()
        self.check_role_members.start()

    def cog_unload(self):
        self.notifier.cancel()
        self.check_role_members.cancel()

    @tasks.loop(minutes=10)
    async def notifier(self):
        for guild in self.bot.guilds:
            stream = client.streams.get_stream_by_user(TWITCH_CHANNEL.id)
            if stream is not None:
                if self.offline:
                    channel = get(guild.channels, name=LOG_CHANNEL_NAME)
                    await send_stream_notification(stream, channel)
                    self.offline = False
            else:
                self.offline = True

    @notifier.before_loop
    async def before_notifier(self):
        await self.bot.wait_until_ready()

    @tasks.loop(hours=5)
    async def check_role_members(self):
        for guild in self.bot.guilds:
            channel = get(guild.channels, name=LOG_CHANNEL_NAME)
            await channel.send("Checking role members")
            role = get(guild.roles, name=TAG)
            for member in role.members:
                if member.display_name == "BOT KSTA" or member == guild.owner:
                    continue
                if not TAG in member.display_name:
                    await member.send("В нике отсутствует тег `" + TAG + "`. Я убрал тебе роль и ник на сервере.")
                    await member.remove_roles(role)
                    await member.edit(nick="")
                    continue
                try:
                    player = fortnite.player(member.display_name)
                except UnknownPlayerError:
                    player = None
                except:
                    channel = get(guild.channels, name="stream-an")
                    await channel.send("Error accessing fortnite-tracker API")
                    return
                if player is None:
                    await member.remove_roles(role)
                    await member.send("Не удалось найти игрока с ником `" + member.display_name +
                                      "`. Я Убрал тебе роль и ник на сервере. Проверь, находит ли тебя здесь: "
                                      "https://fortnitetracker.com/profile/pc/"
                                      + urllib.parse.quote(member.display_name))
                    await member.edit(nick="")
                await asyncio.sleep(5)
            await channel.send("role member check done")

    @check_role_members.before_loop
    async def before_notifier(self):
        await self.bot.wait_until_ready()


bot.add_cog(MyCog(bot))
bot.run(TOKEN)
