from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import json
import os

app= FastAPI()

class companyUpdate(BaseModel):
       company_name: Optional[str]| None
       about_company: Optional[str]| None
       owner: Optional[str]| None
       employees: Optional[int]| None
       contact_information: Optional[str]| None
            
print(os.getcwd())

with open ("data.json","r") as file:
       data = json.load(file)

@app.get("/")
def company():
        return "Welcome"


@app.get("/company_name/{company_name}")
def get_company_name(company_name: str):
        for Data in data:
                if Data["company_name"]== company_name:
                       return {"Data":Data,
                                "Message":"Found"}

        return{"Message":"Not Found"}


@app.put("/company_name/{comapny_name}")
def update_company_name(company_name: str):
       for Data in data:
              if [company_name] == [company_name]:
                     Data.update({"company_name":"company_name",
                                  "about_company":"about_company",
                                  "owner":"owner",
                                  "employees":"employees",
                                  "contact_information":"contact_information"
                                  })
                     
                     with open ("data.json","w") as file:
                            data = json.load(file)
                     return {"message": "update succeefully"}
              else:
                     return {"message": "Not updated"}

              



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
