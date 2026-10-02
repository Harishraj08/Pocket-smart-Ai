from ..schemas import *
from ..vendor_catalog import get_catalog
from ..gemini_utils import gemini_available,generate_recommendation

def pick(cat,name):
    m=[x for x in cat if x["category"].lower()==name.lower()]
    return m[0] if m else None

def mock_home(r):
    cat=get_catalog("home"); out=[]
    for i in r.items:
        p=pick(cat,i.category) or pick(cat,"decor") or cat[0]
        q=i.quantity; unit=float(p["price"]); subtotal=unit*q
        out.append(RecommendationItem(name=p["name"],category=i.category,platform=p["platform"],estimated_price=unit,quantity=q,subtotal=subtotal,
            reason=f"Selected for the {i.style} style requested for the {r.room}.",url=p["url"]))
    # Keep fallback total inside budget by reducing quantities, then remove expensive items if necessary.
    total=sum(x.subtotal for x in out)
    for x in sorted(out,key=lambda z:z.subtotal,reverse=True):
        while total>r.budget and x.quantity>1:
            x.quantity-=1;x.subtotal=x.estimated_price*x.quantity;total=sum(z.subtotal for z in out)
    out=[x for x in out if x.subtotal<=r.budget] or out[:1]
    total=min(sum(x.subtotal for x in out),r.budget)
    return RecommendationResponse(planner="home",title=f"Budget plan for your {r.room}",
      summary=f"A {r.room} setup balancing {', '.join(r.priorities) if r.priorities else 'value, functionality and style'}.",
      budget=r.budget,estimated_total=total,remaining_budget=r.budget-total,
      budget_allocations=[BudgetAllocation(category="Furniture",amount=r.budget*.45,percentage=45,note="Functional pieces"),
      BudgetAllocation(category="Lighting",amount=r.budget*.2,percentage=20,note="Lighting"),
      BudgetAllocation(category="Decor",amount=r.budget*.2,percentage=20,note="Visual finishing"),
      BudgetAllocation(category="Buffer",amount=r.budget*.15,percentage=15,note="Contingency")],
      recommendations=out,tips=["Check dimensions before buying.","Keep a delivery/installation buffer."],ai_generated=False)

def mock_party(r):
    cat=get_catalog("party"); out=[]
    food=pick(cat,"catering"); q=max(1,r.guests); total=food["price"]*q
    if total>r.budget*.45:q=max(1,int(r.budget*.45//food["price"]));total=food["price"]*q
    out.append(RecommendationItem(name=food["name"],category="catering",platform=food["platform"],estimated_price=food["price"],quantity=q,subtotal=total,reason=f"Food allocation for {r.guests} guests.",url=food["url"]))
    deco=min([x for x in cat if x["category"]=="decoration"],key=lambda x:abs(x["price"]-r.budget*.2))
    out.append(RecommendationItem(name=deco["name"],category="decoration",platform=deco["platform"],estimated_price=deco["price"],quantity=1,subtotal=deco["price"],reason=f"Balanced for a {r.event_type} event.",url=deco["url"]))
    ent=pick(cat,"entertainment")
    if ent and sum(x.subtotal for x in out)+ent["price"]<=r.budget:out.append(RecommendationItem(name=ent["name"],category="entertainment",platform=ent["platform"],estimated_price=ent["price"],quantity=1,subtotal=ent["price"],reason="Adds entertainment within the plan.",url=ent["url"]))
    total=min(sum(x.subtotal for x in out),r.budget)
    return RecommendationResponse(planner="party",title=f"{r.event_type.title()} party plan",summary=f"A practical event budget for {r.guests} guests at {r.venue}.",
      budget=r.budget,estimated_total=total,remaining_budget=r.budget-total,
      budget_allocations=[BudgetAllocation(category="Catering",amount=r.budget*.45,percentage=45,note="Food"),
      BudgetAllocation(category="Decoration",amount=r.budget*.2,percentage=20,note="Decor"),
      BudgetAllocation(category="Entertainment",amount=r.budget*.2,percentage=20,note="Entertainment"),
      BudgetAllocation(category="Accommodation",amount=r.budget*.15,percentage=15,note="Optional stay")],
      recommendations=out,tips=["Confirm guest count before ordering.","Treat platform prices as estimates."],ai_generated=False)

def mock_jewelry(budget,occasion,style,image=False):
    cat=get_catalog("jewelry"); out=[]; remain=budget
    preferred=[x for x in cat if ("statement" in x["name"].lower())==(style.lower() in {"bold","festive"})]+cat
    seen=set()
    for p in preferred:
        if p["name"] in seen or p["price"]>remain:continue
        seen.add(p["name"]);out.append(RecommendationItem(name=p["name"],category=p["category"],platform=p["platform"],estimated_price=p["price"],quantity=1,subtotal=p["price"],
          reason=f"Fits a {style} look for {occasion}"+(" and can be coordinated with the uploaded outfit." if image else ""),url=p["url"]))
        remain-=p["price"]
        if len(out)==3:break
    return RecommendationResponse(planner="jewelry",title=f"Jewelry ideas for {occasion}",summary=f"{style.title()} options around your budget.",
      budget=budget,estimated_total=budget-remain,remaining_budget=remain,
      budget_allocations=[BudgetAllocation(category="Primary piece",amount=budget*.55,percentage=55,note="Main focus"),
      BudgetAllocation(category="Supporting piece",amount=budget*.3,percentage=30,note="Coordination"),
      BudgetAllocation(category="Buffer",amount=budget*.15,percentage=15,note="Price variation")],
      recommendations=out,tips=["Check material and size specifications before purchase."],ai_generated=False)

def generate_home(r):
    if gemini_available():
        try:return generate_recommendation("home",r.model_dump(),get_catalog("home"))
        except Exception:pass
    return mock_home(r)
def generate_party(r):
    if gemini_available():
        try:return generate_recommendation("party",r.model_dump(),get_catalog("party"))
        except Exception:pass
    return mock_party(r)
def generate_jewelry(budget,occasion,style,color,image_bytes=None,image_mime=None):
    if gemini_available():
        try:return generate_recommendation("jewelry",{"budget":budget,"occasion":occasion,"style":style,"color_preference":color},get_catalog("jewelry"),image_bytes,image_mime)
        except Exception:pass
    return mock_jewelry(budget,occasion,style,bool(image_bytes))
