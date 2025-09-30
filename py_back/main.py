from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import uvicorn
from datetime import datetime

app = FastAPI(title="Database Python API")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db_connection():
    try:
        conn = psycopg2.connect(
dbname ="fridge_db",
user="fridge_user",
password="1234",
host="localhost",
port="5432")
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        raise

# База знаний о категориях продуктов
PRODUCT_CATEGORIES = {
    "молочные": ["молоко", "сыр", "йогурт", "кефир", "творог", "сметана", "масло", "сливки"],
    "овощи": ["помидор", "огурец", "картофель", "морковь", "лук", "капуста", "перец"],
    "фрукты": ["яблоко", "банан", "апельсин", "лимон", "груша", "виноград"],
    "мясо": ["колбаса", "сосиски", "курица", "говядина", "свинина", "ветчина"],
    "напитки": ["сок", "вода", "чай", "кофе", "лимонад", "компот"],
    "хлеб": ["хлеб", "батон", "булка", "лаваш", "сухари"],
    "яйца": ["яйца", "яичница", "омлет"]
}

# Определяет категорию продукта
def categorize_product(product_name):
    product_lower = product_name.lower()
    for category, keywords in PRODUCT_CATEGORIES.items():
        for keyword in keywords:
            if keyword in product_lower:
                return category
    return "другое"

@app.get("/")
async def root():
    return {
        "message": "Python Database API работает",
        "timestamp": datetime.now().isoformat()
    }

# Получает все товары из базы данных с категориями
@app.get("/api/database-items")
async def get_database_items():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("SELECT * FROM fridge_items ORDER BY created_at DESC")
        items = cursor.fetchall()
        
        # Добавляем категории к каждому товару
        processed_items = []
        for item in items:
            category = categorize_product(item["name"])
            processed_item = dict(item)
            processed_item["category"] = category
            processed_items.append(processed_item)
        
        cursor.close()
        conn.close()
        
        print(f"Обработано {len(processed_items)} товаров из базы данных")
        return processed_items
        
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка базы данных: {str(e)}")

@app.post("/api/items")
async def create_item(item_data: dict):
    """Добавление нового товара в базу данных"""
    try:
        name = item_data.get("name", "").strip()
        is_in_fridge = item_data.get("isInFridge", True)
        
        if not name:
            raise HTTPException(status_code=400, detail="Название товара обязательно")
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute(
            "INSERT INTO fridge_items (name, is_in_fridge) VALUES (%s, %s) RETURNING *",
            (name, is_in_fridge)
        )
        
        new_item = cursor.fetchone()
        conn.commit()
        
        cursor.close()
        conn.close()
        
        if new_item:
            print(f"Добавлен новый товар: {name}")
            return dict(new_item)
        else:
            raise HTTPException(status_code=500, detail="Не удалось создать товар")
        
    except Exception as e:
        print(f"Ошибка при добавлении товара: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка базы данных: {str(e)}")

@app.get("/api/filter-by-category/{category}")
async def filter_by_category(category: str):
    """Фильтрует товары по категории из базы данных"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("SELECT * FROM fridge_items ORDER BY created_at DESC")
        all_items = cursor.fetchall()
        
        # Фильтруем по категории
        filtered_items = []
        for item in all_items:
            item_category = categorize_product(item["name"])
            if category.lower() in item_category.lower():
                processed_item = dict(item)
                processed_item["category"] = item_category
                filtered_items.append(processed_item)
        
        cursor.close()
        conn.close()
        
        print(f"Найдено {len(filtered_items)} товаров в категории '{category}'")
        return {
            "category": category,
            "count": len(filtered_items),
            "items": filtered_items
        }
        
    except Exception as e:
        print(f"Ошибка при фильтрации: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка базы данных: {str(e)}")


# Возвращает список всех категорий
@app.get("/api/categories")
async def get_categories():
    return {
        "categories": list(PRODUCT_CATEGORIES.keys()),
        "total_categories": len(PRODUCT_CATEGORIES)
    }

# Поиск продуктов по категории или названию в базе данных
@app.post("/api/search-products")
async def search_products(search_data: dict):
    search_query = search_data.get("query", "").lower().strip()
    
    if not search_query:
        return {"error": "Пустой поисковый запрос"}
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("SELECT * FROM fridge_items ORDER BY created_at DESC")
        all_items = cursor.fetchall()
        
        # Ищем по категории или названию
        found_items = []
        for item in all_items:
            item_category = categorize_product(item["name"])
            item_name_lower = item["name"].lower()
            
            # Проверяем совпадение с категорией или названием
            if (search_query in item_category or 
                search_query in item_name_lower or
                any(keyword in item_name_lower for keyword in PRODUCT_CATEGORIES.get(search_query, []))):
                
                processed_item = dict(item)
                processed_item["category"] = item_category
                processed_item["match_type"] = "category" if search_query in item_category else "name"
                found_items.append(processed_item)
        
        cursor.close()
        conn.close()
        
        print(f"По запросу '{search_query}' найдено {len(found_items)} товаров")
        return {
            "search_query": search_query,
            "found_count": len(found_items),
            "items": found_items
        }
        
    except Exception as e:
        print(f"Ошибка при поиске: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка базы данных: {str(e)}")


# Возвращает статистику по категориям
@app.get("/api/statistics")
async def get_statistics():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("SELECT * FROM fridge_items")
        all_items = cursor.fetchall()
        
        # Считаем статистику по категориям
        category_stats = {}
        for item in all_items:
            category = categorize_product(item["name"])
            if category not in category_stats:
                category_stats[category] = {"total": 0, "in_fridge": 0}
            
            category_stats[category]["total"] += 1
            if item["is_in_fridge"]:
                category_stats[category]["in_fridge"] += 1
        
        cursor.close()
        conn.close()
        
        return {
            "total_products": len(all_items),
            "categories": category_stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Ошибка при получении статистики: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка базы данных: {str(e)}")

if __name__ == "__main__":
    print("Запуск Python Database API на порту 8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)