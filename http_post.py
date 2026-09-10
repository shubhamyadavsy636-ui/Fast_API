import json
from fastapi import FastAPI, HTTPException
from typing import  Annotated, Literal, Optional
from fastapi.responses import JSONResponse 
from pydantic import BaseModel, Field, computed_field 

app = FastAPI()

def load_data():
    with open('patient.json','r') as f:
        data = json.load(f)
        return data
    
def save_data(data):
    with open('patient.json', 'w') as f:
        json.dump(data, f, indent=4)

class Patient(BaseModel):
    id: Annotated[int, Field(..., description='Give the name of the patient ')]
    name: Annotated[str, Field(..., description='Give name of the patient')]
    city: Annotated[str, Field(..., description='Enter the city of the patient')]
    gender: Annotated[Literal["Male","Female","Other"], Field(..., description="Enter the gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description='Height must be in mtrs')]
    weight: Annotated[float, Field(...,gt=0, description='Weight must be in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight/((self.height/100)**2),2)
    

    @computed_field
    @property
    def categories(self) -> str:
        if self.bmi < 18.5:
            return "underweight"
        elif 18.5 <= self.bmi < 23:
            return "normal"
        else: 
            return "overweight"    
        

class update_patient(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    gender: Annotated[Literal["Male","Female","Other"], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

        
# /-------------------------------------------------------------------------
# post to add the data

@app.post('/patient', status_code=201)
def add_patient(patient : Patient):
    data = load_data()        
    
    #load the data 
    data = load_data()

    # cheak if patient is alrady in the data
    if any(p["id"] == patient.id for p in data['patients']):
        raise HTTPException(409 , detail='patient is already exit')

    # if not then put the record in the data
    data['patients'].append(patient.model_dump())
    save_data(data)

    return {
        "message": "patient data saved successfully",
        "patient": patient
    }




# ----------------------------------------------------------------------
# put to update the data

@app.put('/edit/{patient_id}')
def update(patient_id:int, patient:update_patient):

    data = load_data()
    
    for p in data['patients']:
        if p['id'] == patient_id:

            update_data = patient.model_dump(exclude_unset=True)

            for key , value in update_data.items():
                p[key] = value

            save_data(data)

            return {
                'message': 'patient update successfully',
                "patient": p
            }

    raise HTTPException(status_code=404 , detail="patient not found")
    

    

