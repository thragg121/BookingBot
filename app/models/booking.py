from datetime import date, datetime, time

from sqlalchemy import Date, DateTime, ForeignKey, Time, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id"),
        nullable=False,
    )

    booking_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    booking_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
