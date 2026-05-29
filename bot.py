import os
import asyncio
import discord

from dotenv import load_dotenv
from discord.ext import commands

from database import engine, Base

import models


load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()

intents.guilds = True
intents.members = True
intents.voice_states = True


class MyBot(commands.Bot):

    async def setup_hook(self):

        async with engine.begin() as conn:

            await conn.run_sync(
                Base.metadata.create_all
            )


        for file in os.listdir("./cogs"):

            try:

                await self.load_extension(
                    f"cogs.{file[:-3]}"
                )
                print(
                    f"{file} 로드 완료"
                )

            except Exception as e:
                print(
                    f"{file} 로드 실패: {e}"
                )


        synced = await self.tree.sync()

        print(
            f"{len(synced)}개 글로벌 명령어 동기화 완료"
        )

bot = MyBot(
    command_prefix="/",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"{bot.user} 로그인 완료")

asyncio.run(
    bot.start(TOKEN)
)
