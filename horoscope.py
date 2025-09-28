"""
Horoscope generation logic using LangGraph for agentic AI.
"""
import os
from datetime import datetime, timedelta
from typing import Dict, Any, AsyncGenerator
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langchain.tools import tool
from pydantic import BaseModel

# Initialize LLM (you'll need to set OPENAI_API_KEY environment variable)
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    streaming=True
)

class HoroscopeState(BaseModel):
    """State for the horoscope generation graph."""
    user_info: Dict[str, Any]
    prediction_type: str
    date: datetime
    current_step: str = "analyze"
    horoscope_content: str = ""
    error: str = ""

@tool
def analyze_birth_chart(user_info: str) -> str:
    """Analyze user's birth chart based on birth information."""
    return f"Analyzing birth chart for user born on {user_info}"

@tool
def get_planetary_positions(date: str) -> str:
    """Get planetary positions for a specific date."""
    return f"Retrieving planetary positions for {date}"

@tool
def generate_horoscope_content(analysis: str, prediction_type: str) -> str:
    """Generate horoscope content based on analysis and prediction type."""
    return f"Generating {prediction_type} horoscope based on: {analysis}"

def analyze_node(state: HoroscopeState) -> HoroscopeState:
    """Analyze user's birth information and current planetary positions."""
    try:
        user_info = state.user_info
        birth_info = f"Born on {user_info['birth_date']} at {user_info.get('birth_time', 'unknown time')} in {user_info.get('birth_place', 'unknown place')}"
        
        # Analyze birth chart
        birth_analysis = analyze_birth_chart(birth_info)
        
        # Get current planetary positions
        current_date = state.date.strftime("%Y-%m-%d")
        planetary_positions = get_planetary_positions(current_date)
        
        state.horoscope_content = f"{birth_analysis}\n{planetary_positions}"
        state.current_step = "generate"
        
    except Exception as e:
        state.error = f"Error in analysis: {str(e)}"
        state.current_step = "error"
    
    return state

def generate_node(state: HoroscopeState) -> HoroscopeState:
    """Generate the actual horoscope content."""
    try:
        if state.error:
            return state
            
        # Create system prompt for horoscope generation
        system_prompt = f"""You are an expert astrologer. Generate a {state.prediction_type} horoscope based on the following information:

User Information: {state.user_info}
Analysis: {state.horoscope_content}

Create a personalized, insightful horoscope that:
1. Is specific to the {state.prediction_type} timeframe
2. Incorporates astrological insights
3. Provides practical guidance
4. Is encouraging and positive
5. Is 2-3 paragraphs long

Format the response as a well-structured horoscope reading."""

        # Generate horoscope using LLM
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Generate my {state.prediction_type} horoscope for {state.date.strftime('%Y-%m-%d')}")
        ]
        
        response = llm.invoke(messages)
        state.horoscope_content = response.content
        state.current_step = "complete"
        
    except Exception as e:
        state.error = f"Error in generation: {str(e)}"
        state.current_step = "error"
    
    return state

def error_node(state: HoroscopeState) -> HoroscopeState:
    """Handle errors in the horoscope generation process."""
    state.horoscope_content = f"Sorry, I encountered an error generating your horoscope: {state.error}"
    state.current_step = "complete"
    return state

# Create the horoscope generation graph
def create_horoscope_graph():
    """Create and return the horoscope generation graph."""
    workflow = StateGraph(HoroscopeState)
    
    # Add nodes
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("error", error_node)
    
    # Add edges
    workflow.add_edge("analyze", "generate")
    workflow.add_edge("generate", END)
    workflow.add_edge("error", END)
    
    # Set entry point
    workflow.set_entry_point("analyze")
    
    return workflow.compile()

# Global graph instance
horoscope_graph = create_horoscope_graph()

async def generate_horoscope(
    user_info: Dict[str, Any], 
    prediction_type: str, 
    date: datetime
) -> str:
    """
    Generate a horoscope for a user.
    
    Args:
        user_info: Dictionary containing user's birth information
        prediction_type: Type of prediction (daily, weekly, monthly)
        date: Date for the prediction
    
    Returns:
        Generated horoscope content
    """
    try:
        # Create initial state
        initial_state = HoroscopeState(
            user_info=user_info,
            prediction_type=prediction_type,
            date=date
        )
        
        # Run the graph
        result = await horoscope_graph.ainvoke(initial_state.dict())
        
        return result["horoscope_content"]
        
    except Exception as e:
        return f"Error generating horoscope: {str(e)}"

async def generate_chat_response(
    user_info: Dict[str, Any], 
    message: str
) -> AsyncGenerator[str, None]:
    """
    Generate a streaming chat response for horoscope-related questions.
    
    Args:
        user_info: Dictionary containing user's birth information
        message: User's message
    
    Yields:
        Chunks of the response as they are generated
    """
    try:
        # Create system prompt for chat
        system_prompt = f"""You are a helpful astrologer assistant. The user's birth information is:
- Name: {user_info.get('name', 'Unknown')}
- Birth Date: {user_info.get('birth_date', 'Unknown')}
- Birth Time: {user_info.get('birth_time', 'Unknown')}
- Birth Place: {user_info.get('birth_place', 'Unknown')}

Answer their question about astrology, horoscopes, or their birth chart. Be helpful, accurate, and encouraging. Keep responses conversational and not too long."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=message)
        ]
        
        # Stream the response
        async for chunk in llm.astream(messages):
            if hasattr(chunk, 'content') and chunk.content:
                yield chunk.content
                
    except Exception as e:
        yield f"Error generating response: {str(e)}"
