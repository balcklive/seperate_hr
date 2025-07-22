#!/usr/bin/env python3
# Author: Peng Fei
# Script to start the FastAPI SSE server

import os
import sys
import uvicorn
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from api.server import create_server

def main():
    """Start the FastAPI server"""
    app = create_server()
    
    # Configuration
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 7000))
    reload = os.getenv('ENVIRONMENT') == 'development'
    
    print(f"Starting FastAPI SSE server on {host}:{port}")
    print("Available endpoints:")
    print("  POST /api/process-jd - Stream job description processing")
    print("  GET  /api/health     - Health check")
    print("  GET  /docs           - API documentation")
    print("  GET  /redoc          - Alternative API documentation")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    main() 