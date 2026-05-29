import discord
from discord.ext import commands
from discord import app_commands

create_channels = set()


class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="핑",
        description="봇이 응답하는지 테스트하는 명령어입니다."
    )
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("퐁!")


async def setup(bot):
    await bot.add_cog(Ping(bot))