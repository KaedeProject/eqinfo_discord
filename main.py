from body.eqinfo import Eqinfo
from logger.logger import LogV1, LogV2
from dotenv import load_dotenv

import discord
import asyncio
import os

load_dotenv()

TOKEN = os.getenv('Token')
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

client = discord.Client(intents=intents)

eqinfo = Eqinfo()

async def send_to_all_guilds(message):
    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                try:
                    await channel.send(embed=message if isinstance(message, discord.Embed) else None, content=None if isinstance(message, discord.Embed) else message)
                    break
                except Exception as e:
                    LogV2(f"{guild.name} に送信失敗: {e}")
                continue

async def update_status():
    await client.wait_until_ready()
    while not client.is_closed():
        guild_count = len(client.guilds)
        activity = discord.Game(name=f"{guild_count} サーバーで稼働中")
        await client.change_presence(status=discord.Status.online, activity=activity)
        LogV1(f"ステータス更新: {guild_count} サーバー")
        await asyncio.sleep(300)

@client.event
async def on_ready():
    LogV1(f'Bot起動: {client.user} : {len(client.guilds)} サーバー参加中')

    client.loop.create_task(update_status())
    client.loop.create_task(eqinfo.EqinfoLoop(send_to_all_guilds))

client.run(TOKEN)