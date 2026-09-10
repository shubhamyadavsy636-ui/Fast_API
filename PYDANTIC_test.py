# from pydantic import BaseModel, EmailStr, Field
# from typing import List, Dict, Optional 

# class patient(BaseModel):
#     # this field give constrent on nuericala & string data , or to attach data
#      name: str = Field(max_length=50)
#      age: int = Field(gt=0, lt=100)
#      email: EmailStr 
#      # special keyword to get email aunthic data from user 
#      # in otional data is need not to fill compilersry it can be empty
#      # at the alleriges we put none (defult) 
#      allergies: Optional[List[str]] = None
#      phon: Optional[Dict[str, int]]


# def insert(p1: patient):
#      print(p1.name)
#      print(p1.age)
#      print(p1.allergies)
#      print(p1.phon)


# def update(p1: patient):
#      print(p1.name)
#      print(p1.age)
#      print(p1.allergies)
#      print(p1.phon)

# patient_info = {'name': 'subm', 'age': 20, 'email': "subm@gamil.com",'phon':{'home':987640, 'phon': 789465 }}

# p1 = patient(**patient_info)

# # insert(p1)
# update(p1)




# ---------------------------------------------------------------------
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
from typing import List, Dict, Optional, Annotated

class student(BaseModel):
     name: Annotated[str, Field(max_length=50, title="name of the student is ", description='given name must be in string ')]
     # strict don't allow to have type conv.
     age : int
     roll: Annotated[int, Field(gt=0, lt=100, default=18, strict=True)]
     subject: Optional[List[str]] = Field(max_length=5)
     contect: Dict[str, int]
     email: EmailStr

     @field_validator('email')
     @classmethod
     def email_valid(cls, value):
          valid_domain = ['hdfc.com', 'icici.com']
          domain = value.split('@')[-1]

          if domain not in valid_domain:
               raise ValueError("You are not a valid candidate")
          
          return value

# this fun return the name in the capital latter 
     @field_validator('name')
     @classmethod
     def name_valid(cls, value):
          return value.upper()

     @field_validator('age', mode='before')
     @classmethod
     def age_valid(cls,value):
          if 0 < value < 100:
               return value
          else :
               raise ValueError('age must be in b/w 0 - 100')


     @model_validator(mode='after')
     def emergnecy(cls, model):
          if model.age < 10 and 'emergency' not in model.contect:
               raise ValueError('age less then 10 must have emergency ')





stu_info = {
     'name':'subm', 'age': 19, 'roll':50, 'subject':['math','java','cpp'],'contect':{'phon':789465, 'home':987654}, 'email':'subm@hdfc.com'
}


def show(s1: student):
     print(s1.name)
     print(s1.age)
     print(s1.roll)
     print(s1.subject)
     print(s1.contect)
     print(s1.email)


s1 = student(**stu_info)

show(s1)


