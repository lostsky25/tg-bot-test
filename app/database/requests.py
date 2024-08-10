from app.database.models import async_session
from app.database.models import User, CategoryLevel1, CategoryLevel2, CategoryLevel3
from sqlalchemy import and_
from sqlalchemy import select, desc

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def add_category(category):
    async def safe_add(category, categoryType):
        database_category = await session.scalar(select(categoryType).where(categoryType.name == category.name))
        
        if not database_category:
            session.add(category)
            await session.commit()
            
    async with async_session() as session:
        if isinstance(category, CategoryLevel1):
            await safe_add(category, CategoryLevel1)
        elif isinstance(category, CategoryLevel2):
            await safe_add(category, CategoryLevel2)
        elif isinstance(category, CategoryLevel3):
            await safe_add(category, CategoryLevel3)

async def get_last_category(level):
    async with async_session() as session:
        match level:
            case 1:
                return await session.scalar(select(CategoryLevel1).order_by(desc(CategoryLevel1.id)).limit(1))
            case 2:
                return await session.scalar(select(CategoryLevel2).order_by(desc(CategoryLevel2.id)).limit(1))
            case 3:
                return await session.scalar(select(CategoryLevel3).order_by(desc(CategoryLevel3.id)).limit(1))


async def get_next_categories(level, category_id):
    async with async_session() as session:
        match level:
            case 1:
                return await session.scalars(select(CategoryLevel1))
            case 2:
                return await session.scalars(select(CategoryLevel2).where(and_(CategoryLevel2.prev_category_id == int(category_id), CategoryLevel2.level == int(level))))
            case 3:
                return await session.scalars(select(CategoryLevel3).where(and_(CategoryLevel3.prev_category_id == int(category_id), CategoryLevel3.level == int(level))))

async def get_prev_categories(level, prev_category_id):
    async with async_session() as session:
        match level:
            case 1:
                return await session.scalars(select(CategoryLevel1))
            case 2:
                level2_row = await session.scalar(select(CategoryLevel2).where(and_(CategoryLevel2.id == int(prev_category_id), CategoryLevel2.level == int(level))))
                level1_prev_category_id = (await session.scalar(select(CategoryLevel1).where(CategoryLevel1.id == int(level2_row.prev_category_id)))).id
                return await session.scalars(select(CategoryLevel2).where(and_(CategoryLevel2.prev_category_id == int(level1_prev_category_id), CategoryLevel2.level == int(level))))
            case 3:
                return await session.scalars(select(CategoryLevel3).where(and_(CategoryLevel3.prev_category_id == int(prev_category_id), CategoryLevel3.level == int(level))))

