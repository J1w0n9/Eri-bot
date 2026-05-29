from sqlalchemy import BigInteger, ForeignKey

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from database import Base


from typing import Optional

class Guild(Base):

    __tablename__ = "guilds"

    guild_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )

    create_channel_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        nullable=True
    )

class VoiceRoom(Base):

    __tablename__ = "voice_rooms"

    channel_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )

    guild_id: Mapped[int] = mapped_column(
        ForeignKey("guilds.guild_id")
    )

    owner_id: Mapped[int] = mapped_column(
        BigInteger
    )