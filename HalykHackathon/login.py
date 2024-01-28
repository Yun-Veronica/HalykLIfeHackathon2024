from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

app = FastAPI()

# Подключение к базе данных
cluster = MongoClient("mongodb+srv://Jhon:123321aa@cluster0.ccrp0ub.mongodb.net/?retryWrites=true&w=majority")
db = cluster.MockEGov
collection = db.Users

# Инициализация шаблонов Jinja2
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(request: Request, user_id: int = Form(...), username: str = Form(...), surname: str = Form(...)):
    # Проверка данных в MongoDB
    search_params = {
        "_id": user_id,
        "name": username,
        "surname": surname
    }
    result = collection.find_one(search_params)

    if result:
        return templates.TemplateResponse("welcome.html", {"request": request, "username": username})
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error_message": "Invalid credentials"})
