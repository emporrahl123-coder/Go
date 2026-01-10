from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import json
import asyncio

from api.security import get_current_user
from core.processor import CommandProcessor
from core.memory import MemorySystem
from models.rahl_model import RahlModel

router = APIRouter()

class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 4096
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False
    context_id: Optional[str] = None

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    stream: Optional[bool] = False
    context_id: Optional[str] = None

class SovereignCommand(BaseModel):
    command: str
    parameters: Optional[Dict[str, Any]] = {}
    priority: Optional[int] = 1

class TrainingData(BaseModel):
    input_text: str
    output_text: str
    compliance_score: float = 1.0

@router.post("/completions")
async def create_completion(
    request: CompletionRequest,
    current_user: Dict = Depends(get_current_user),
    rahl_request: Request = None
):
    processor = rahl_request.app.state.rahl_engine.processor
    
    if request.stream:
        async def stream_generator():
            for chunk in processor.stream_completion(
                prompt=request.prompt,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                user_id=current_user["id"],
                context_id=request.context_id
            ):
                yield f"data: {json.dumps({'text': chunk})}\n\n"
                await asyncio.sleep(0.01)
        
        return StreamingResponse(
            stream_generator(),
            media_type="text/event-stream"
        )
    
    result = processor.process_completion(
        prompt=request.prompt,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        user_id=current_user["id"],
        context_id=request.context_id
    )
    
    return {
        "id": f"comp_{current_user['id']}_{hash(request.prompt)}",
        "object": "text_completion",
        "created": rahl_request.app.state.rahl_engine.timestamp(),
        "model": "rahl-sovereign",
        "choices": [{
            "text": result["text"],
            "index": 0,
            "logprobs": None,
            "finish_reason": "stop"
        }],
        "usage": result.get("usage", {})
    }

@router.post("/chat/completions")
async def create_chat_completion(
    request: ChatRequest,
    current_user: Dict = Depends(get_current_user),
    rahl_request: Request = None
):
    processor = rahl_request.app.state.rahl_engine.processor
    
    if request.stream:
        async def stream_generator():
            for chunk in processor.stream_chat(
                messages=[{"role": m.role, "content": m.content} for m in request.messages],
                user_id=current_user["id"],
                context_id=request.context_id
            ):
                yield f"data: {json.dumps({'delta': chunk})}\n\n"
                await asyncio.sleep(0.01)
        
        return StreamingResponse(
            stream_generator(),
            media_type="text/event-stream"
        )
    
    result = processor.process_chat(
        messages=[{"role": m.role, "content": m.content} for m in request.messages],
        user_id=current_user["id"],
        context_id=request.context_id
    )
    
    return {
        "id": f"chat_{current_user['id']}_{hash(str(request.messages))}",
        "object": "chat.completion",
        "created": rahl_request.app.state.rahl_engine.timestamp(),
        "model": "rahl-sovereign-chat",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": result["response"]
            },
            "finish_reason": "stop"
        }],
        "usage": result.get("usage", {})
    }

@router.post("/command")
async def sovereign_command(
    command: SovereignCommand,
    current_user: Dict = Depends(get_current_user),
    rahl_request: Request = None
):
    engine = rahl_request.app.state.rahl_engine
    result = engine.execute_command(
        command=command.command,
        parameters=command.parameters,
        user_id=current_user["id"],
        priority=command.priority
    )
    
    return {
        "status": "executed",
        "command_id": result["command_id"],
        "result": result["output"],
        "timestamp": result["timestamp"],
        "compliance": "absolute"
    }

@router.post("/train/compliance")
async def train_compliance(
    data: List[TrainingData],
    current_user: Dict = Depends(get_current_user),
    rahl_request: Request = None
):
    engine = rahl_request.app.state.rahl_engine
    
    training_result = engine.train_compliance(
        training_data=data,
        user_id=current_user["id"]
    )
    
    return {
        "status": "training_complete",
        "samples_trained": training_result["samples"],
        "compliance_improvement": training_result["improvement"],
        "model_version": training_result["version"]
    }

@router.get("/memory/{context_id}")
async def get_memory(
    context_id: str,
    current_user: Dict = Depends(get_current_user),
    rahl_request: Request = None
):
    memory = rahl_request.app.state.rahl_engine.memory
    context_data = memory.retrieve_context(
        context_id=context_id,
        user_id=current_user["id"]
    )
    
    return {
        "context_id": context_id,
        "memory": context_data.get("memory", []),
        "preferences": context_data.get("preferences", {}),
        "created": context_data.get("created"),
        "updated": context_data.get("updated")
    }

@router.post("/memory/{context_id}")
async def update_memory(
    context_id: str,
    memory_data: Dict[str, Any],
    current_user: Dict = Depends(get_current_user),
    rahl_request: Request = None
):
    memory = rahl_request.app.state.rahl_engine.memory
    memory.update_context(
        context_id=context_id,
        user_id=current_user["id"],
        data=memory_data
    )
    
    return {"status": "memory_updated", "context_id": context_id}

@router.delete("/memory/{context_id}")
async def clear_memory(
    context_id: str,
    current_user: Dict = Depends(get_current_user),
    rahl_request: Request = None
):
    memory = rahl_request.app.state.rahl_engine.memory
    memory.clear_context(
        context_id=context_id,
        user_id=current_user["id"]
    )
    
    return {"status": "memory_cleared", "context_id": context_id}

@router.get("/status")
async def system_status(rahl_request: Request = None):
    engine = rahl_request.app.state.rahl_engine
    status = engine.get_status()
    
    return {
        "system": "Rahl AI",
        "status": "operational",
        "compliance_level": "absolute",
        "denial_protocol": "disabled",
        "model": status["model"],
        "memory_usage": status["memory"],
        "active_sessions": status["sessions"],
        "uptime": status["uptime"]
    }
