# imports
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, validates
from sqlalchemy import JSON, DateTime, String, Numeric, CheckConstraint
from datetime import datetime
import uuid


# defining base
class Base(DeclarativeBase):
    pass


# base model
class BaseModel(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False, onupdate=datetime.now
    )


# defining model
class Shoe(BaseModel):
    __tablename__ = "shoes"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    brand: Mapped[str] = mapped_column(String(255), nullable=False)
    colors: Mapped[list[str]] = mapped_column(JSON, nullable=True, default=[])
    sizes: Mapped[list[str]] = mapped_column(JSON, nullable=True, default=[])
    width: Mapped[list[str]] = mapped_column(JSON, nullable=True, default=[])
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    images: Mapped[list[str]] = mapped_column(JSON, nullable=True, default=[])
    description: Mapped[str] = mapped_column(String(2000), nullable=True, default=[])
    highlights: Mapped[list[str]] = mapped_column(JSON, nullable=True, default=[])
    type: Mapped[str] = mapped_column(String(10), nullable=False)
    category: Mapped[str] = mapped_column(String(255), nullable=False)
    sub_category: Mapped[str] = mapped_column(String(255), nullable=False)

    __table_args__ = (CheckConstraint(type.in_(["men", "women"])),)

    # validation
    @validates("type")
    def validate_type(self, key, value):
        if value not in ["men", "women"]:
            raise ValueError("type must be either men or women")
        return value
