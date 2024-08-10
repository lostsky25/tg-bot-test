import os
from dotenv import load_dotenv, dotenv_values
from sqlalchemy import BigInteger, String, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

load_dotenv()

engine = create_async_engine(url=f"postgresql+asyncpg://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}")

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

class CategoryLevel1(Base):
    __tablename__ = 'categories_level_1'

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    level: Mapped[int] = mapped_column(Integer)
    count: Mapped[int] = mapped_column(Integer)

class CategoryLevel2(Base):
    __tablename__ = 'categories_level_2'

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    level: Mapped[int] = mapped_column(Integer)
    count: Mapped[int] = mapped_column(Integer)
    prev_category_id: Mapped[int] = mapped_column(ForeignKey('categories_level_1.id'))

class CategoryLevel3(Base):
    __tablename__ = 'categories_level_3'

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    level: Mapped[int] = mapped_column(Integer)
    count: Mapped[int] = mapped_column(Integer)
    prev_category_id: Mapped[int] = mapped_column(ForeignKey('categories_level_2.id'))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)