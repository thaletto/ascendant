"""
Chat functionality routes for Horoscope AI Backend.
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import AsyncGenerator
import json

from db import get_db, User, ChatMessage
from models import ChatRequest, ChatResponse
from horoscope import generate_chat_response

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/stream")
async def stream_chat(
    chat_data: ChatRequest, 
    db: AsyncSession = Depends(get_db)
):
    """
    Stream a chat response for horoscope-related questions.
    
    Args:
        chat_data: Chat request data
        db: Database session
    
    Returns:
        Streaming response with chat content
    """
    try:
        # Get user information
        result = await db.execute(select(User).where(User.id == chat_data.user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Prepare user info for chat
        user_info = {
            "name": user.name,
            "birth_date": user.birth_date.strftime("%Y-%m-%d"),
            "birth_time": user.birth_time,
            "birth_place": user.birth_place
        }
        
        # Save user message to database
        user_message = ChatMessage(
            user_id=chat_data.user_id,
            message=chat_data.message,
            is_user_message="user"
        )
        db.add(user_message)
        await db.commit()
        await db.refresh(user_message)
        
        # Generate streaming response
        async def generate_response() -> AsyncGenerator[str, None]:
            response_content = ""
            
            try:
                async for chunk in generate_chat_response(user_info, chat_data.message):
                    response_content += chunk
                    # Send chunk as Server-Sent Events
                    yield f"data: {json.dumps({'content': chunk, 'done': False})}\n\n"
                
                # Save assistant response to database
                assistant_message = ChatMessage(
                    user_id=chat_data.user_id,
                    message=chat_data.message,
                    response=response_content,
                    is_user_message="assistant"
                )
                db.add(assistant_message)
                await db.commit()
                
                # Send final message
                yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"
                
            except Exception as e:
                error_msg = f"Error generating response: {str(e)}"
                yield f"data: {json.dumps({'content': error_msg, 'done': True, 'error': True})}\n\n"
        
        return StreamingResponse(
            generate_response(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")

@router.get("/history/{user_id}")
async def get_chat_history(
    user_id: int, 
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """
    Get chat history for a user.
    
    Args:
        user_id: ID of the user
        limit: Maximum number of messages to return
        db: Database session
    
    Returns:
        List of chat messages
    """
    # Check if user exists
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get chat messages
    query = select(ChatMessage).where(
        ChatMessage.user_id == user_id
    ).order_by(ChatMessage.created_at.desc()).limit(limit)
    
    result = await db.execute(query)
    messages = result.scalars().all()
    
    return [ChatResponse.model_validate(message) for message in messages]

@router.delete("/history/{user_id}", status_code=204)
async def clear_chat_history(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Clear chat history for a user.
    
    Args:
        user_id: ID of the user
        db: Database session
    """
    # Check if user exists
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete all chat messages for the user
    from sqlalchemy import delete
    await db.execute(
        delete(ChatMessage).where(ChatMessage.user_id == user_id)
    )
    await db.commit()
    
    return None
