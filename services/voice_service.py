from sqlalchemy import select

from database import SessionLocal

from models import (
    Guild,
    VoiceRoom
)


async def set_create_channel(
    guild_id: int,
    channel_id: int
):

    async with SessionLocal() as session:

        result = await session.execute(

            select(Guild).where(
                Guild.guild_id == guild_id
            )
        )

        guild = result.scalar_one_or_none()

        if not guild:

            return False

        guild.create_channel_id = channel_id

        await session.commit()

        return True


async def get_create_channel(
    guild_id: int
):

    async with SessionLocal() as session:

        result = await session.execute(

            select(Guild).where(
                Guild.guild_id == guild_id
            )
        )

        guild = result.scalar_one_or_none()

        if not guild:

            return None

        return guild.create_channel_id