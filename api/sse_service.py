# Author: Peng Fei
# FastAPI SSE service for streaming job requirement processing

import json
import asyncio
from typing import AsyncGenerator
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from agent_modules.orchestrator import OrchestratorAgent

class JobDescriptionRequest(BaseModel):
    jd_text: str

class SSEService:
    def __init__(self):
        self.orchestrator = OrchestratorAgent()
        
        # Constants for progress tracking
        self.PROGRESS_STEPS = {
            'analyzing': 20,
            'parsing': 40,
            'extracting_skills': 60,
            'formatting': 80,
            'complete': 100
        }
    
    def create_app(self) -> FastAPI:
        """Create FastAPI app with SSE endpoints"""
        app = FastAPI(
            title="Job Requirement Generator API",
            description="SSE API for streaming job requirement processing",
            version="1.0.0"
        )
        
        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        @app.post("/api/process-jd")
        async def process_jd_stream(request: JobDescriptionRequest):
            """SSE endpoint for processing job descriptions"""
            if not request.jd_text.strip():
                raise HTTPException(status_code=400, detail="Job description text is required")
            
            return EventSourceResponse(
                self._stream_jd_processing(request.jd_text)
            )
        
        @app.get("/api/health")
        async def health_check():
            """Health check endpoint"""
            return {
                "status": "healthy",
                "service": "job-requirement-generator",
                "version": "1.0.0"
            }
        
        return app
    
    async def _stream_jd_processing(self, jd_text: str) -> AsyncGenerator[dict, None]:
        """
        Stream job description processing steps with real-time LLM output
        
        Args:
            jd_text: Job description text
            
        Yields:
            dict: SSE event data
        """
        try:
            # Use the new streaming orchestrator method
            async for stream_chunk in self.orchestrator.process_input_stream(jd_text):
                if stream_chunk["event"] == "progress":
                    data = stream_chunk["data"]
                    yield {
                        "event": "progress",
                        "data": json.dumps(data, ensure_ascii=False)
                    }
                elif stream_chunk["event"] == "complete":
                    data = stream_chunk["data"]
                    yield {
                        "event": "complete",
                        "data": json.dumps(data, ensure_ascii=False)
                    }
                elif stream_chunk["event"] == "partial_result":
                    data = stream_chunk["data"]
                    yield {
                        "event": "partial_result",
                        "data": json.dumps(data, ensure_ascii=False)
                    }
                elif stream_chunk["event"] == "error":
                    data = stream_chunk["data"]
                    yield {
                        "event": "error",
                        "data": json.dumps(data, ensure_ascii=False)
                    }
            
        except Exception as e:
            yield {
                "event": "error",
                "data": json.dumps({
                    "step": "error",
                    "message": f"Error: {str(e)}",
                    "progress": 0,
                    "error": True
                }, ensure_ascii=False)
            } 