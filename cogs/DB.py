import discord

from discord.ext import commands
from discord import app_commands

from services.guilds_service import (
    register_guild
)


class DB(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    @app_commands.command(
        name="등록",
        description="현재 서버를 등록합니다."
    )
    async def register(
        self,
        interaction: discord.Interaction
    ):

        success = await register_guild(
            interaction.guild.id
        )

        if not success:

            await interaction.response.send_message(
                "이미 등록된 서버입니다.",
                ephemeral=True
            )

            return

        await interaction.response.send_message(
            "서버 등록 완료!"
        )


async def setup(bot):
    await bot.add_cog(DB(bot))