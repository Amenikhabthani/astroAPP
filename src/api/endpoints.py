from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from services.astrology_service import process_natal_aspects_request, format_astrology_prompt, summarize_chart, get_natal_chart
from services.llm_service import generate_interpretation
from services.utilis import  classify_question
from db.database import save_question, get_last_n_questions, supabase, get_mock_user_id
from fastapi import Request

router = APIRouter()

class AstrologyRequest(BaseModel):
    question: str
    datetime: Optional[dict] = None
    location: Optional[dict] = None
# Define the response model
class AstrologyResponse(BaseModel):
    question: str
    interpretation: str
    history: Optional[List[dict]] = None  

@router.post("/natal-aspects-data")
async def natal_aspects_endpoint(request: AstrologyRequest):
    try:
        result = process_natal_aspects_request(request.question, request.datetime, request.location)
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class QuestionInput(BaseModel):
    question: str

@router.post("/classify")
def classify_endpoint(input_data: QuestionInput):
    try:
        result = classify_question(input_data.question)
        return {"classification": result}  # Ensure it's returned as a valid dictionary
    except Exception as e:
        return {"error": str(e)}

# Use the generate_interpretation function without chunking
@router.post("/interpret", response_model=AstrologyResponse)
async def interpret_astrology(request: Request, astrology_request: AstrologyRequest):
    try:
        # Use the mock user ID for testing
        user_id = get_mock_user_id(request)

        # Step 1: Generate the natal chart data
        chart_data = get_natal_chart(astrology_request.question, astrology_request.datetime, astrology_request.location)
        if not chart_data:
            return "⚠️ Could not generate a chart from the provided datetime and location."

        # Step 2: Summarize the natal chart
        summary = summarize_chart(chart_data)

        # Step 3: Fetch history (but do not return it later)
        history_items = get_last_n_questions(user_id)
        history_dicts = [{"question": item["question"], "interpretation": item["interpretation"]} for item in history_items]

        # Step 4: Format the prompt and generate interpretation in one go
        prompt = format_astrology_prompt(summary, astrology_request.question, history_dicts)
        full_interpretation = generate_interpretation(prompt)

        # Save the current interaction
        save_question(user_id, astrology_request.question, full_interpretation, astrology_request.datetime, astrology_request.location)

        # Do NOT return history in the response
        return {
            "question": astrology_request.question,
            "interpretation": full_interpretation,
            "history":history_dicts
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to interpret astrology: {str(e)}")
@router.get("/history")
def get_history(request: Request):
    user_id = request.client.host
    history = get_last_n_questions(user_id, n=10)
    return {"history": history}
