import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(
    command_prefix="/",
    intents=discord.Intents.default()
)

# 생성용 채널 ID 저장
create_channels = set()

# 봇이 만든 임시 채널 저장
temp_channels = set()


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

    print(f"Logged in as {bot.user}")


# 생성용 채널 만드는 슬래시 커맨드
@bot.tree.command(
    name="생성방",
    description="음성채널 생성용 방을 만듭니다."
)
async def create_room(
    interaction: discord.Interaction,
    category: discord.CategoryChannel
):

    voice_channel = await category.create_voice_channel(
        name="🔊 채널 생성"
    )

    create_channels.add(voice_channel.id)

    await interaction.response.send_message(
        f"생성용 채널 생성 완료: {voice_channel.mention}"
    )

#핑퐁 커맨드
@bot.tree.command(
    name="핑",
    description="봇이 응답하는지 테스트하는 명령어입니다."
)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("퐁!")


# 음성 상태 변경 감지
@bot.event
async def on_voice_state_update(member, before, after):

    # 생성용 채널 입장
    if after.channel and after.channel.id in create_channels:

        category = after.channel.category

        # 개인 채널 생성
        new_channel = await member.guild.create_voice_channel(
            name=f"{member.name}의 채널",
            category=category
        )

        temp_channels.add(new_channel.id)

        # 유저 이동
        await member.move_to(new_channel)

    # 채널 퇴장
    if before.channel:

        # 봇이 만든 임시 채널인지 확인
        if before.channel.id in temp_channels:

            # 아무도 없으면 삭제
            if len(before.channel.members) == 0:

                temp_channels.remove(before.channel.id)

                await before.channel.delete()

bot.run(TOKEN)
