import time
import asyncio
from app.database.models import async_session
from sqlalchemy import select, update

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from app.database.models import CategoryLevel1, CategoryLevel2, CategoryLevel3

async def updateAllCategoriesCount(categoryType):
    browser = webdriver.Chrome()
    browser.set_page_load_timeout(10)
    browser.get("https://www.ozon.ru")

    try:
        time.sleep(8)
        browser.find_element(By.ID, "reload-button").click()
        time.sleep(2)
    except NoSuchElementException:
        print("Exception: NoSuchElementException")
    
    async with async_session() as session:
        categories = await session.scalars(select(categoryType))
        for category in categories:
            try:
                new_count = ''

                browser.get("https://www.ozon.ru" + category.url)

                for ch in browser.find_element(By.XPATH, "//div[contains(@class, 'e2a')]/div[contains(@class, 'e3a')]/span").text:
                    if ch.isdigit():
                        new_count += str(ch)

                upd = (update(categoryType).where(categoryType.id == category.id).values(count=int(new_count)))
                await session.execute(upd)
            except NoSuchElementException:
                print("https://www.ozon.ru" + category.url, -1)
            except TimeoutException:
                print("Exception: TimeoutException")
        
        await session.commit()
    
    browser.quit()

async def main():
    while True:
        await updateAllCategoriesCount(CategoryLevel1)
        await updateAllCategoriesCount(CategoryLevel2)
        await updateAllCategoriesCount(CategoryLevel3)
        await asyncio.sleep(60 * 60)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')