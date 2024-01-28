import os
from datetime import datetime
from pymongo import MongoClient
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

cluster = MongoClient("mongodb+srv://Jhon:123321aa@cluster0.ccrp0ub.mongodb.net/?retryWrites=true&w=majority")
db = cluster.MockEGov
collection = db.Users

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# # 1
# pattern = {
#     "_id": 190068729008,
#     "idnumber": "116071805",
#     "sex": "male",
#     "name": "Nıkıta",
#     "surname": "Antonov",
#     "middlename": "Tımofeevıch",
#     "birthDate": datetime(2001, 6, 16),
#     "resident": True,
#     "region": "Almaty",
#     "phone": "+77882326699",
#     "email": "test5@gmail.com",
#     "validregis": {
#         "startdate": datetime(2017, 6, 16),
#         "enddate": datetime(2027, 6, 16),
#         "where": "MVD"
#     },
#     "residenceRegistration": "Almaty, gdetovo 45"
# }

# Insert the document into the collection
# collection.insert_one(pattern)
# print("Document inserted successfully!")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("pup.html", {"request": request})


@app.post("/calculate_fsum", response_class=HTMLResponse)
async def calculate_fsum(
    request: Request,
    risk: int = Form(...),
    active_recreation: str = Form(...),
    risk_level: int = Form(...),
    insurance_claims: str = Form(...),
):
    user_id_to_find = 190068729008
    query = {"_id": user_id_to_find}

    user_data = collection.find_one(query)

    if user_data:
        sex = user_data.get("sex")
        birth_date = user_data.get("birthDate")
        region = user_data.get("region")

        # Assign numerical values based on conditions
        sex_value = 2 if sex == "male" else 1  # 2 for male, 1 for female
        birth_year = birth_date.year if birth_date else None
        birth_date_value = 1 if birth_year and birth_year >= 2004 else (
            2 if birth_year and birth_year >= 1994 else (3 if birth_year and birth_year >= 1984 else None))
        region_value = 1 if region.lower() == "almaty" else 2  # 1 for Almaty, 2 for other regions

        fsum = 1000
        sport = 1
        riskwork = 1
        befor = 1

        # Calculate x
        x = sex_value + birth_date_value + region_value + sport + riskwork + befor

        # Apply conditions and update fsum
        if x < 10:
            fsum += 200
        elif x == 10:
            fsum += 400
        elif x > 10:
            fsum += 600

        # Multiply fsum by risk
        fsum *= 2 if risk == 1 else (4 if risk == 2 else (6 if risk == 3 else 1))

        # Now you can use fsum as needed
        return templates.TemplateResponse("pup.html", {"request": request, "fsum": fsum})
    else:
        return {"error": f"User with ID {user_id_to_find} not found."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
