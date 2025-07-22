# Author: Peng Fei
# FastAPI server for job requirement generator

import os
import uvicorn
from api.sse_service import SSEService

def create_server():
    """Create and configure the API server"""
    sse_service = SSEService()
    app = sse_service.create_app()
    
    return app

def run_server():
    """Run the API server"""
    app = create_server()
    
    # Configuration
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8000))
    reload = os.getenv('ENVIRONMENT') == 'development'
    
    print(f"Starting FastAPI SSE server on {host}:{port}")
    print("Available endpoints:")
    print("  POST /api/process-jd - Stream job description processing")
    print("  GET  /api/health     - Health check")
    print("  GET  /docs           - API documentation")
    
    uvicorn.run(
        "api.server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    run_server() 