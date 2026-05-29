from sqlalchemy import select

from database import SessionLocal
from models import Guild


async def register_guild(guild_id: int):

    async with SessionLocal() as session:

        result = await session.execute(

            select(Guild).where(
                Guild.guild_id == guild_id
            )
        )

        guild = result.scalar_one_or_none()

        if guild:

            return False

        new_guild = Guild(
            guild_id=guild_id
        )

        session.add(new_guild)

        await session.commit()

        return True