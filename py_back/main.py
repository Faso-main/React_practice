from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

app = FastAPI(title="Python Test API")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Python FastAPI работает!",
        "backend": "Python", 
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    }

@app.get("/api/python-test")
async def python_test():
    return {
        "message": "Связь установлена!",
        "language": "Python",
        "framework": "FastAPI",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "success"
    }

@app.get("/api/python-message")
async def python_message():

    return {
        "text": 'YESYESYES',
        "type": "python_message",
        "success": True
    }

if __name__ == "__main__":
    print("Запуск Python тестового сервера на порту 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)