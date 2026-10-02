import json
from .config import get_settings
from .schemas import RecommendationResponse
try:
    from google import genai
except ImportError: genai=None

def gemini_available():
    s=get_settings()
    return bool(genai and s.gemini_api_key and s.ai_mode.lower()=="gemini")

def generate_recommendation(planner,payload,catalog,image_bytes=None,image_mime=None):
    if not gemini_available(): raise RuntimeError("Gemini is not enabled")
    s=get_settings(); client=genai.Client(api_key=s.gemini_api_key)
    prompt=f"""You are PocketSmart AI, a budget-aware recommendation assistant.
Planner: {planner}
User input: {json.dumps(payload,ensure_ascii=False,indent=2)}
Available simulated catalog: {json.dumps(catalog,ensure_ascii=False,indent=2)}
Rules:
1. Never exceed the user's budget.
2. Use only catalog items.
3. Balance functionality, style, price and preferences.
4. Prices are estimates, not live inventory.
5. Return JSON matching the requested schema."""
    contents=[prompt]
    if image_bytes:
        from PIL import Image
        from io import BytesIO
        contents.append(Image.open(BytesIO(image_bytes)))
    response=client.models.generate_content(
        model=s.gemini_model,contents=contents,
        config={"response_mime_type":"application/json","response_schema":RecommendationResponse,"temperature":0.35})
    if getattr(response,"parsed",None) is not None:
        return RecommendationResponse.model_validate(response.parsed)
    return RecommendationResponse.model_validate_json(response.text)
