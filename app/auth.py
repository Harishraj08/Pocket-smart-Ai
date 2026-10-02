import hashlib,hmac,os
from datetime import datetime,timedelta,timezone
import jwt
from .config import get_settings
from .database import get_conn
from .models import User
COOKIE_NAME="pocketsmart_session"; ALGORITHM="HS256"

def hash_password(password):
    salt=os.urandom(16); d=hashlib.pbkdf2_hmac("sha256",password.encode(),salt,180000)
    return f"pbkdf2_sha256$180000${salt.hex()}${d.hex()}"
def verify_password(password,encoded):
    try:
        alg,rounds,salt,digest=encoded.split("$")
        if alg!="pbkdf2_sha256": return False
        d=hashlib.pbkdf2_hmac("sha256",password.encode(),bytes.fromhex(salt),int(rounds))
        return hmac.compare_digest(d.hex(),digest)
    except Exception: return False
def create_access_token(user_id):
    p={"sub":str(user_id),"exp":datetime.now(timezone.utc)+timedelta(hours=8)}
    return jwt.encode(p,get_settings().secret_key,algorithm=ALGORITHM)
def decode_access_token(token):
    try: return int(jwt.decode(token,get_settings().secret_key,algorithms=[ALGORITHM])["sub"])
    except Exception: return None
def create_user(email,name,password):
    from sqlite3 import IntegrityError
    try:
        with get_conn() as c:
            cur=c.execute("INSERT INTO users(email,name,password_hash) VALUES(?,?,?)",(email.lower(),name.strip(),hash_password(password)))
            return User(cur.lastrowid,email.lower(),name.strip(),"")
    except IntegrityError: raise ValueError("An account with this email already exists.")
def authenticate(email,password):
    with get_conn() as c: r=c.execute("SELECT * FROM users WHERE email=?",(email.lower(),)).fetchone()
    if not r or not verify_password(password,r["password_hash"]): return None
    return User(r["id"],r["email"],r["name"],r["password_hash"])
def get_user(user_id):
    if not user_id:return None
    with get_conn() as c:r=c.execute("SELECT * FROM users WHERE id=?",(user_id,)).fetchone()
    return User(r["id"],r["email"],r["name"],r["password_hash"]) if r else None
