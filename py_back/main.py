from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Fridge Python API")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Простые тестовые данные
fridge_items = [
    {"id": 1, "name": "Питон Молоко", "is_in_fridge": True},
    {"id": 2, "name": "Питон Яйца", "is_in_fridge": True},
    {"id": 3, "name": "Питон Сыр", "is_in_fridge": False},
    {"id": 4, "name": "Питон Колбаса", "is_in_fridge": False},
]

@app.get("/")
async def root():
    return {"message": "Python FastAPI работает!"}

@app.get("/api/health")
async def health_check():
    return {"status": "OK", "backend": "Python FastAPI"}

@app.get("/api/items")
async def get_items():
    print("Python: Получен запрос на получение продуктов")
    return fridge_items

@app.post("/api/items")
async def create_item(item: dict):
    print(f"Python: Добавление продукта: {item}")
    new_id = max([i["id"] for i in fridge_items], default=0) + 1
    new_item = {
        "id": new_id,
        "name": item.get("name", "Без названия"),
        "is_in_fridge": item.get("isInFridge", True)
    }
    fridge_items.append(new_item)
    return new_item

@app.patch("/api/items/{item_id}/toggle")
async def toggle_item(item_id: int):
    print(f"Python: Переключение продукта {item_id}")
    for item in fridge_items:
        if item["id"] == item_id:
            item["is_in_fridge"] = not item["is_in_fridge"]
            return item
    return {"error": "Продукт не найден"}

@app.delete("/api/items/{item_id}")
async def delete_item(item_id: int):
    print(f"Python: Удаление продукта {item_id}")
    for i, item in enumerate(fridge_items):
        if item["id"] == item_id:
            deleted_item = fridge_items.pop(i)
            return {"message": "Продукт удален", "deleted_item": deleted_item}
    return {"error": "Продукт не найден"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )