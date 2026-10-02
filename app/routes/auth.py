from fastapi import APIRouter,HTTPException,Response,Request
from ..schemas import UserCreate,LoginRequest
from ..auth import *
router=APIRouter(prefix="/api/auth",tags=["auth"])
def pub(u):return {"id":u.id,"email":u.email,"name":u.name}
@router.post("/register",status_code=201)
def register(p:UserCreate,response:Response):
    try:u=create_user(p.email,p.name,p.password)
    except ValueError as e:raise HTTPException(409,str(e))
    t=create_access_token(u.id);response.set_cookie(COOKIE_NAME,t,httponly=True,samesite="lax");return {"user":pub(u),"access_token":t}
@router.post("/login")
def login(p:LoginRequest,response:Response):
    u=authenticate(p.email,p.password)
    if not u:raise HTTPException(401,"Invalid email or password.")
    t=create_access_token(u.id);response.set_cookie(COOKIE_NAME,t,httponly=True,samesite="lax");return {"user":pub(u),"access_token":t}
@router.post("/token")
def token(p:LoginRequest):
    u=authenticate(p.email,p.password)
    if not u:raise HTTPException(401,"Invalid email or password.")
    return {"access_token":create_access_token(u.id),"token_type":"bearer"}
@router.post("/logout")
def logout(response:Response):response.delete_cookie(COOKIE_NAME);return {"ok":True}
@router.get("/me")
def me(request:Request):
    u=get_user(decode_access_token(request.cookies.get(COOKIE_NAME,"")))
    if not u:raise HTTPException(401,"Not authenticated.")
    return {"user":pub(u)}
