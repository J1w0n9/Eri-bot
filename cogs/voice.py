import discord

from discord.ext import commands
from discord import app_commands

from services.voice_service import (
    set_create_channel,
    get_create_channel
)

# 유저가 생성한 개인 음성채널 저장
create_channels = set()


class Voice(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @app_commands.command(
        name="생성방",
        description="음성채널 생성용 방을 만듭니다."
    )
    async def create_room(
        self,
        interaction: discord.Interaction,
        category: discord.CategoryChannel
    ):

        voice_channel = await category.create_voice_channel(
            name="🔊 채널 생성"
        )

        success = await set_create_channel(
            interaction.guild.id,
            voice_channel.id
        )

        if not success:

            await interaction.response.send_message(
                "먼저 /등록 명령어를 사용해주세요.",
                ephemeral=True
            )

            await voice_channel.delete()

            return

        await interaction.response.send_message(
            f"생성용 채널 생성 완료: {voice_channel.mention}"
        )

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState
    ):

        # -----------------------------
        # 개인 채널 삭제 처리
        # -----------------------------
        if before.channel:

            if before.channel.id in create_channels:

                if len(before.channel.members) == 0:

                    await before.channel.delete()

                    create_channels.remove(
                        before.channel.id
                    )

                    print(
                        f"{before.channel.name} 삭제 완료"
                    )

        # 음성채널 입장 안했으면 종료
        if not after.channel:

            return

        # 생성용 채널 ID 조회
        create_channel_id = await get_create_channel(
            member.guild.id
        )

        if not create_channel_id:

            return

        # 생성용 채널이 아니면 종료
        if after.channel.id != create_channel_id:

            return

        category = after.channel.category

        # 개인 채널 생성
        new_channel = await category.create_voice_channel(
            name=f"{member.display_name}의 방"
        )

        # 권한 부여
        await new_channel.set_permissions(
            member,
            manage_channels=True,
            move_members=True
        )

        # 유저 이동
        await member.move_to(
            new_channel
        )

        # 삭제 대상 등록
        create_channels.add(
            new_channel.id
        )

        print(
            f"{member} 채널 생성 완료"
        )


async def setup(bot):

    await bot.add_cog(
        Voice(bot)
    )