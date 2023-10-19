import re
import typing

import discord
from discord.ext import commands
import asyncio
from investing_scraper import scrap
import functools
from datetime import datetime
from datetime import timedelta
from pytz import timezone
import asyncio
from discord.ext import tasks

fmt = "%H:%M"
fmt2 = "%m-%d"
FN_CHANNEL = 1152668967157104755
LOG_CHANNEL = 1161018317025329204

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

CONTINUE = True


async def run_blocking(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
    func = functools.partial(blocking_func, *args,
                             **kwargs)  # `run_in_executor` doesn't support kwargs, `functools.partial` does
    return await client.loop.run_in_executor(None, func)


@client.event
async def on_ready():
    print('Ready!')
    print('------------------')


@tasks.loop(hours=1)
async def send_news():
    print('started')
    now_time = datetime.now(timezone('America/Vancouver'))
    if now_time.hour == 19:
        print('passed')
        chanel = client.get_channel(FN_CHANNEL)
        print(datetime.now(timezone('America/Vancouver')))
        res = await run_blocking(scrap)
        print(res)
        flag = 0
        for item in res:
            flag+=1
            emb = discord.Embed(title='\U0001F4F0' + f' {item[0]}', colour=0xff0000)
            emb.add_field(name="Time:", value=f'Tomorrow  {item[1]}', inline=False)
            emb.add_field(name="Effects:", value=f'{item[2]}', inline=False)
            await chanel.send(embed=emb)
        if flag == 0:
            await chanel.send(embed=discord.Embed(title="No important news for tomorrow!", description="Stay tuned", color=0x00ff1e))
    print('done!')


@commands.has_permissions(administrator=True)
@client.command()
async def start(ctx):
    if ctx.channel.id != FN_CHANNEL:
        return
    chanel = client.get_channel(LOG_CHANNEL)
    await chanel.send('Started!')
    send_news.start()


@commands.has_permissions(administrator=True)
@client.command()
async def stop(ctx):
    if ctx.channel.id != FN_CHANNEL:
        return
    print('Stopped')
    chanel = client.get_channel(LOG_CHANNEL)
    await chanel.send('Stopped!')
    send_news.stop()

@commands.has_permissions(administrator=True)
@client.command()
async def inf(ctx):
    if ctx.channel.id != FN_CHANNEL:
        return
    await ctx.send('!start - start bot, the news will come every day at 19:00 (Pacific Time)')
    await ctx.send('!stop - stop bot')


client.run('MTE1ODg2NDQ1NDE1OTcxNjM2Mg.GAV0pd.XW_18dMm6CsLnWLMudrAhcciR8ve5FsP1-QFmQ')
