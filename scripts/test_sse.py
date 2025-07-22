#!/usr/bin/env python3
# Author: Peng Fei
# Script to test the SSE API

import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tests.sse_client_test import SSETestClient

async def main():
    """Run SSE API tests"""
    print("=== Job Requirement Generator SSE API Test ===")
    
    test_client = SSETestClient()
    
    # Test health check
    await test_client.test_health_check()
    
    # Test SSE processing
    await test_client.test_sse_connection()
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    asyncio.run(main()) 