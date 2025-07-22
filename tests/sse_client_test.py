# Author: Peng Fei
# Python SSE client for testing job requirement generator API

import asyncio
import aiohttp
import json
import time
from typing import AsyncGenerator

class SSEClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def process_jd_stream(self, jd_text: str) -> AsyncGenerator[dict, None]:
        """
        Process job description via SSE stream
        
        Args:
            jd_text: Job description text
            
        Yields:
            dict: Streamed response data
        """
        url = f"{self.base_url}/api/process-jd"
        headers = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }
        data = {"jd_text": jd_text}
        
        async with self.session.post(url, json=data, headers=headers) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"HTTP {response.status}: {error_text}")
            
            async for line in response.content:
                line = line.decode('utf-8').strip()
                
                if line.startswith('data: '):
                    try:
                        data = json.loads(line[6:])  # Remove 'data: ' prefix
                        yield data
                    except json.JSONDecodeError:
                        print(f"Failed to parse SSE data: {line}")
                elif line.startswith('event: '):
                    event_type = line[7:]  # Remove 'event: ' prefix
                    print(f"Event type: {event_type}")

class SSETestClient:
    def __init__(self):
        self.test_jd = """
        Senior Software Engineer
        
        We are looking for a Senior Software Engineer with 5+ years of experience in Python, 
        JavaScript, and cloud technologies. The ideal candidate should have experience with 
        microservices architecture, Docker, and Kubernetes. Strong problem-solving skills 
        and excellent communication abilities are required. Experience with machine learning 
        frameworks and data engineering is a plus.
        """
    
    async def test_sse_connection(self):
        """Test SSE connection and processing"""
        print("=== Testing SSE Job Description Processing ===")
        print(f"Job Description:\n{self.test_jd.strip()}")
        print("\n" + "="*50)
        
        async with SSEClient() as client:
            start_time = time.time()
            
            try:
                async for data in client.process_jd_stream(self.test_jd):
                    elapsed = time.time() - start_time
                    
                    if 'step' in data:
                        print(f"[{elapsed:.2f}s] Step: {data['step']}")
                        print(f"    Message: {data['message']}")
                        print(f"    Progress: {data.get('progress', 0)}%")
                        
                        if data['step'] == 'complete':
                            print("\n=== Final Result ===")
                            result = data.get('result', {})
                            print(json.dumps(result, indent=2, ensure_ascii=False))
                            break
                    
                    if data.get('error'):
                        print(f"ERROR: {data['message']}")
                        break
                        
            except Exception as e:
                print(f"Connection error: {e}")
    
    async def test_health_check(self):
        """Test health check endpoint"""
        print("\n=== Testing Health Check ===")
        
        async with SSEClient() as client:
            try:
                async with client.session.get(f"{client.base_url}/api/health") as response:
                    if response.status == 200:
                        health_data = await response.json()
                        print(f"Health check passed: {health_data}")
                    else:
                        print(f"Health check failed: HTTP {response.status}")
            except Exception as e:
                print(f"Health check error: {e}")

async def main():
    """Main test function"""
    test_client = SSETestClient()
    
    # Test health check
    await test_client.test_health_check()
    
    # Test SSE processing
    await test_client.test_sse_connection()

if __name__ == "__main__":
    asyncio.run(main()) 