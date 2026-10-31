from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import json

app = FastAPI()


class CompanyUpdate(BaseModel):
    company_name: Optional[str] = None
    about_company: Optional[str] = None
    owner: Optional[str] = None
    employees: Optional[int] = None
    contact_information: Optional[str] = None

class companypost(BaseModel):
    company_name: Optional[str] = None
    about_company: Optional[str] = None
    owner: Optional[str] = None
    employees: Optional[int] = None
    contact_information: Optional[str] = None

class companypost2(BaseModel):
    new_key: str
    new_value: str| int| float| None= None


# Load the list of company from the file
with open("data.json", "r") as file:
    company = json.load(file)

def save_data():
    with open("data.json", "w") as file:
        json.dump(company, file, indent=4)


@app.get("/")
def home():
    return "Welcome"


@app.get("/company_name/{company_name}")
def get_company_name(company_name: str):
    for companise in company:
        if companise["company_name"] == company_name:
            return {"companise": companise, "Message": "Found"}

    raise HTTPException(status_code=404, detail="Company not found")


@app.put("/company_name/{company_name}")
def update_company_name(company_name: str, data: CompanyUpdate):
    for companise in company:
        if companise["company_name"] == company_name:
            if data.company_name is not None:
                companise["company_name"] = data.company_name
            if data.about_company is not None:
                companise["about_company"] = data.about_company
            if data.owner is not None:
                companise["owner"] = data.owner
            if data.employees is not None:
                companise["employees"] = data.employees
            if data.contact_information is not None:
                companise["contact_information"] = data.contact_information

            save_data()
            return {"message": "Successfully Updated", "company": companise}

    raise HTTPException(status_code=404, detail="Company not found")

@app.post("/company")
def post_company(data: companypost):
    for companise in company:
        if companise["company_name"] == data.company_name:
            raise HTTPException(status_code=409, detail="Company already exists")
 
    new_post = data.model_dump()
    company.append(new_post)
 
    save_data()
 
    return {"message": "Company added", "company": new_post}


PROTECTED_FIELDS = ["company_name"]

@app.patch("/company_name/{company_name}/field")
def add_or_change_field(company_name: str, data: companypost2):
    if data.new_key in PROTECTED_FIELDS:
        raise HTTPException(status_code=400, detail=f"'{data.new_key}' cannot be changed here")

    for companise in company:
        if companise["company_name"] == company_name:
            companise[data.new_key] = data.new_value

            save_data()

            return {"message": "Field updated", "company": companise }

    raise HTTPException(status_code=404, detail="Company not found")


@app.delete("/company_name/{company_name}")
def del_company(company_name: str):
    for companise in company:
        if companise["company_name"] == company_name:
            company.remove(companise)

            save_data()

            return {"message": "Company is deleted"}

    raise HTTPException(status_code=404, detail="Company not found")

             


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)