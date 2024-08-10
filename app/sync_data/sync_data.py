from app.database.models import CategoryLevel1, CategoryLevel2, CategoryLevel3

from app.database.requests import add_category, get_last_category
import app.sync_data.requests as rq

url = "http://www.ozon.ru/api/composer-api.bx/_action/v2/categoryChildV3?menuId=185&categoryId=15500&hash="

mainCategories = {
        15500: "Электроника", # elektronika-15500/
        7500 : "Одежда и обувь", # odezhda-obuv-i-aksessuary-7500/
        17777: "Обувь", # obuv-17777/
        14500: "Дом и сад", # dom-i-sad-14500/
        7000 : "Детские товары", # detskie-tovary-7000/
        # 6500 : "Красота и здоровье", # krasota-i-zdorove-6500/
        # 10500: "Бытовая техника", # bytovaya-tehnika-10500/
        # 11000: "Спорт и отдых", # sport-i-otdyh-11000/
        # 9700 : "Строительство и ремонт", # stroitelstvo-i-remont-9700/
        # 9200 : "Продукты питания", # produkty-pitaniya-9200/
        # 6000 : "Аптека", # apteka-6000/
        # 12300: "Товары для живатных", # tovary-dlya-zhivotnyh-12300/
        # 16500: "Книги", # knigi-16500/
        # 33332: "Охота, рыбалка, туризм", # ohota-rybalka-turizm-33332/
        # 8500 : "Автотовары", # avtotovary-8500/
        # 15000: "Мебель", # mebel-15000/
        # 13500: "Хобби и творчество", # hobbi-i-tvorchestvo-13500/
        # 50001: "Ювелирные украшения", # yuvelirnye-ukrasheniya-50001/
        # 7697 : "Акссесуары", # aksessuary-7697/
        # 13300: "Игры и софт", # igry-i-soft-13300/
        # 18000: "Канцелярские товары", # kantselyarskie-tovary-18000/
        # 8000 : "Антиквариат, винтаж, исскуство", # antikvariat-vintazh-iskusstvo-8000/
        # 32056: "Цифровые товары", # tsifrovye-tovary-32056/
        # 14572: "Бытовая химия", # bytovaya-himiya-14572/
        # 25000: "Супермаркет", # supermarket-25000/?miniapp=supermarket
        # 39803: "Автомобили" # avtomobili-39803/
}

async def add_categories_to_db():
    for i, (keyCategory, mainCategory) in enumerate(mainCategories.items()):
        categories = await rq.get_all_categories(f"https://www.ozon.ru/api/composer-api.bx/_action/v2/categoryChildV3?menuId=185&categoryId={keyCategory}&hash=")
        
        await add_category(CategoryLevel1(url=categories['data']['url'], count=-1, level=1, name=categories['data']['title']))

        for j, columns in enumerate(categories['data']['columns']):
            if 'categories' in columns:
                for k, rows in enumerate(columns['categories']):
                    await add_category(CategoryLevel2(url=rows['url'], count=-1, level=2, name=rows['title'], prev_category_id=(await get_last_category(1)).id))

                    if 'categories' in rows:
                        for c, subRow in enumerate(rows['categories']):
                            await add_category(CategoryLevel3(url=subRow['url'], count=-1, level=3, name=subRow['title'], prev_category_id=(await get_last_category(2)).id))