import json
from fastapi import APIRouter,Request,UploadFile,File,Form,HTTPException
from ..auth import COOKIE_NAME,decode_access_token
from ..config import get_settings
from ..database import get_conn
from ..schemas import HomeRequest,PartyRequest,RecommendationResponse
from ..services.recommendation_service import *
router=APIRouter(prefix="/api",tags=["planners"])
def uid(req):return decode_access_token(req.cookies.get(COOKIE_NAME,""))
def save(req,planner,budget,result):
    u=uid(req)
    if not u:return
    with get_conn() as c:c.execute("INSERT INTO recommendations(user_id,planner,budget,request_json,response_json) VALUES(?,?,?,?,?)",(u,planner,budget,"{}",result.model_dump_json()))
@router.get("/health")
def health():
    s=get_settings();return {"status":"ok","app":s.app_name,"ai_mode":s.ai_mode,"gemini_configured":bool(s.gemini_api_key)}
@router.post("/generate-home",response_model=RecommendationResponse)
def home(p:HomeRequest,request:Request):
    r=generate_home(p);save(request,"home",p.budget,r);return r
@router.post("/generate-party",response_model=RecommendationResponse)
def party(p:PartyRequest,request:Request):
    r=generate_party(p);save(request,"party",p.budget,r);return r
@router.post("/generate-jewelry",response_model=RecommendationResponse)
async def jewelry(request:Request,budget:float=Form(...),occasion:str=Form(...),style:str=Form("minimal"),color_preference:str=Form(""),outfit_image:UploadFile|None=File(None)):
    s=get_settings();b=None;m=None
    if outfit_image and outfit_image.filename:
        if outfit_image.content_type not in {"image/jpeg","image/png","image/webp"}:raise HTTPException(400,"Upload a JPEG, PNG, or WebP image.")
        b=await outfit_image.read()
        if len(b)>s.max_image_mb*1024*1024:raise HTTPException(413,f"Image must be <= {s.max_image_mb} MB.")
        m=outfit_image.content_type
    r=generate_jewelry(budget,occasion,style,color_preference,b,m);save(request,"jewelry",budget,r);return r
@router.get("/history")
def history(request:Request):
    u=uid(request)
    if not u:raise HTTPException(401,"Login to view history.")
    with get_conn() as c:rows=c.execute("SELECT id,planner,budget,response_json,created_at FROM recommendations WHERE user_id=? ORDER BY id DESC LIMIT 50",(u,)).fetchall()
    return [{"id":x["id"],"planner":x["planner"],"budget":x["budget"],"created_at":x["created_at"],"result":json.loads(x["response_json"])} for x in rows]
