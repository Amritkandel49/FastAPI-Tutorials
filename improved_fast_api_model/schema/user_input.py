from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Annotated, Literal
from config.city_tiers import tier_1_cities, tier_2_cities

class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the person in years")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the person in kg")]
    height: Annotated[float, Field(..., gt=0, description="Height of the person in cm")]
    income_lpa: Annotated[float, Field(..., gt=0, description="Annual income of the person in lakhs")]
    smoker: Annotated[bool, Field(..., description="Smoking status of the person")]
    city: Annotated[str, Field(..., description="City of residence")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description="Occupation of the person")]

    @computed_field
    @property
    def bmi(self) -> float:
        height_m = self.height / 100
        return self.weight / (height_m ** 2) if height_m > 0 else 0.0
    

    @computed_field
    @property
    def lifestyle_risk(self)-> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
        
    @field_validator('city')
    @classmethod
    def validate_city(cls, value):
        return value.strip().title()