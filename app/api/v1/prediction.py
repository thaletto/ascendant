"""
Prediction API endpoints for Ascendant astrology intelligence system.
"""

from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from google.adk import Runner
from agent import agent
from app.models import (
    PredictionRequest,
    PredictionResponse,
    BirthDataCreate,
    SessionInfo,
    SessionClearResponse,
)

router = APIRouter(prefix="/predict", tags=["prediction"])


# Models are now imported from app.models


# Store session data (in production, use Redis or database)
session_store: Dict[str, Dict[str, Any]] = {}


def get_or_create_session(session_id: str) -> Dict[str, Any]:
    """Get or create a session context."""
    if session_id not in session_store:
        session_store[session_id] = {"state": {}, "messages": [], "birth_data": None}
    return session_store[session_id]


@router.post("/", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Main prediction endpoint for general astrology questions.
    """
    try:
        # Get or create session
        session = get_or_create_session(request.session_id)

        # Initialize runner properly (no args)
        runner = Runner()
        runner.agent = agent  # assign root agent manually

        # If birth_data is provided, store it in session
        if request.birth_data:
            session["birth_data"] = request.birth_data
            session["state"]["birth_data"] = request.birth_data

        # Run the agent with the query
        result = await runner.run(input_text=request.query, state=session["state"])

        # Update session state and messages
        session["state"].update(result.state)
        session["messages"].append({"role": "user", "content": request.query})
        session["messages"].append({"role": "assistant", "content": result.text})

        return PredictionResponse(
            session_id=request.session_id,
            response=result.text,
            agent_used="AscendantRootAgent",
            status="success",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.post("/health", response_model=PredictionResponse)
async def predict_health(request: PredictionRequest):
    """Health-related astrology predictions."""
    health_query = f"Health and wellness astrology question: {request.query}"

    # Create a modified request for health focus
    health_request = request.copy()
    health_request.query = health_query

    return await predict(health_request)


@router.post("/career", response_model=PredictionResponse)
async def predict_career(request: PredictionRequest):
    """Career-related astrology predictions."""
    career_query = f"Career and profession astrology question: {request.query}"

    career_request = request.copy()
    career_request.query = career_query

    return await predict(career_request)


@router.post("/wealth", response_model=PredictionResponse)
async def predict_wealth(request: PredictionRequest):
    """Wealth and financial astrology predictions."""
    wealth_query = f"Wealth and financial astrology question: {request.query}"

    wealth_request = request.copy()
    wealth_request.query = wealth_query

    return await predict(wealth_request)


@router.post("/marriage", response_model=PredictionResponse)
async def predict_marriage(request: PredictionRequest):
    """Marriage-related astrology predictions."""
    marriage_query = f"Marriage and partnership astrology question: {request.query}"

    marriage_request = request.copy()
    marriage_request.query = marriage_query

    return await predict(marriage_request)


@router.post("/family", response_model=PredictionResponse)
async def predict_family(request: PredictionRequest):
    """Family-related astrology predictions."""
    family_query = f"Family and relationships astrology question: {request.query}"

    family_request = request.copy()
    family_request.query = family_query

    return await predict(family_request)


@router.post("/emotion", response_model=PredictionResponse)
async def predict_emotion(request: PredictionRequest):
    """Emotional and psychological astrology predictions."""
    emotion_query = f"Emotional and psychological astrology question: {request.query}"

    emotion_request = request.copy()
    emotion_request.query = emotion_query

    return await predict(emotion_request)


@router.post("/love", response_model=PredictionResponse)
async def predict_love(request: PredictionRequest):
    """Love and romance astrology predictions."""
    love_query = f"Love and romance astrology question: {request.query}"

    love_request = request.copy()
    love_request.query = love_query

    return await predict(love_request)


@router.post("/children", response_model=PredictionResponse)
async def predict_children(request: PredictionRequest):
    """Children and progeny astrology predictions."""
    children_query = f"Children and progeny astrology question: {request.query}"

    children_request = request.copy()
    children_request.query = children_query

    return await predict(children_request)


@router.post("/birth-data")
async def set_birth_data(request: BirthDataCreate):
    """
    Set birth data for a session.

    Args:
        request: Birth data request

    Returns:
        Confirmation message
    """
    try:
        session = get_or_create_session(request.session_id)

        # Convert BirthDataCreate to BirthData with defaults
        from app.models.birth_data import BirthData

        birth_data_obj = BirthData(**request.dict())
        birth_data_dict = birth_data_obj.to_dict()

        session["birth_data"] = birth_data_dict
        session["state"]["birth_data"] = birth_data_dict

        return {
            "message": "Birth data has been stored successfully",
            "session_id": request.session_id,
            "birth_data": birth_data_dict,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to store birth data: {str(e)}"
        )


@router.get("/session/{session_id}", response_model=SessionInfo)
async def get_session_info(session_id: str):
    """
    Get session information.

    Args:
        session_id: Session identifier

    Returns:
        Session information
    """
    if session_id not in session_store:
        raise HTTPException(status_code=404, detail="Session not found")

    session = session_store[session_id]

    # Create birth data summary if available
    birth_data_summary = None
    if session["birth_data"]:
        birth_data_summary = {
            "name": session["birth_data"].get("name"),
            "birth_date": f"{session['birth_data'].get('birth_year')}-{session['birth_data'].get('birth_month'):02d}-{session['birth_data'].get('birth_day'):02d}",
        }

    return SessionInfo(
        session_id=session_id,
        has_birth_data=session["birth_data"] is not None,
        message_count=len(session["messages"]),
        last_updated="now",  # In production, store timestamp
        birth_data_summary=birth_data_summary,
    )


@router.delete("/session/{session_id}", response_model=SessionClearResponse)
async def clear_session(session_id: str):
    """
    Clear session data.

    Args:
        session_id: Session identifier

    Returns:
        Confirmation message
    """
    if session_id in session_store:
        del session_store[session_id]
        return SessionClearResponse(
            message=f"Session {session_id} cleared successfully", session_id=session_id
        )
    else:
        raise HTTPException(status_code=404, detail="Session not found")
