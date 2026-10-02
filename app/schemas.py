from typing import Literal
from pydantic import BaseModel, Field, field_validator
PlannerName=Literal["home","party","jewelry"]

class UserCreate(BaseModel):
    email:str=Field(min_length=5,max_length=200); name:str=Field(min_length=2,max_length=100); password:str=Field(min_length=6,max_length=128)
    @field_validator("email")
    @classmethod
    def email_lower(cls,v): return v.strip().lower()

class LoginRequest(BaseModel):
    email:str; password:str
    @field_validator("email")
    @classmethod
    def email_lower(cls,v): return v.strip().lower()

class HomeItem(BaseModel):
    category:str=Field(min_length=2,max_length=80); quantity:int=Field(ge=1,le=100); style:str="modern"
class HomeRequest(BaseModel):
    budget:float=Field(gt=0,le=10000000); room:str=Field(min_length=2,max_length=80)
    items:list[HomeItem]=Field(min_length=1,max_length=30); priorities:list[str]=Field(default_factory=list,max_length=10)
class PartyRequest(BaseModel):
    budget:float=Field(gt=0,le=10000000); guests:int=Field(gt=0,le=10000); event_type:str=Field(min_length=2,max_length=80)
    venue:str="home"; city:str=""; priorities:list[str]=Field(default_factory=list,max_length=10)
class RecommendationItem(BaseModel):
    name:str; category:str; platform:str; estimated_price:float=Field(ge=0); quantity:int=Field(ge=1); subtotal:float=Field(ge=0)
    reason:str; url:str|None=None
class BudgetAllocation(BaseModel):
    category:str; amount:float=Field(ge=0); percentage:float=Field(ge=0,le=100); note:str
class RecommendationResponse(BaseModel):
    planner:PlannerName; title:str; summary:str; budget:float; estimated_total:float=Field(ge=0)
    remaining_budget:float; budget_allocations:list[BudgetAllocation]=[]; recommendations:list[RecommendationItem]=[]
    tips:list[str]=[]; source_note:str="Platform data is simulated unless a live partner integration is configured."
    ai_generated:bool=False
