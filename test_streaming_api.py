#!/usr/bin/env python3
# Author: Peng Fei
# Test script for streaming API

import asyncio
import aiohttp
import json
import time

async def test_streaming_api():
    """Test the streaming API with real-time output"""
    
    # Test job description
    jd_text = """
    Senior Software Engineer
    
    We are looking for a Senior Software Engineer with 5+ years of experience in Python, 
    JavaScript, and cloud technologies. The ideal candidate should have experience with 
    microservices architecture, Docker, and Kubernetes. Strong problem-solving skills 
    and excellent communication abilities are required. Experience with machine learning 
    frameworks and data engineering is a plus.
    """
    
    url = "http://localhost:8000/api/process-jd"
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
    }
    data = {"jd_text": jd_text}
    
    print("=== Testing Streaming Job Description Processing ===")
    print(f"Job Description:\n{jd_text.strip()}")
    print("\n" + "="*50)
    
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        
        try:
            async with session.post(url, json=data, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    print(f"HTTP {response.status}: {error_text}")
                    return
                
                print("Streaming response:")
                print("-" * 30)
                
                async for line in response.content:
                    line = line.decode('utf-8').strip()
                    
                    if line.startswith('event: '):
                        event_type = line[7:]  # Remove 'event: ' prefix
                        print(f"\n[EVENT] {event_type}")
                        
                    elif line.startswith('data: '):
                        try:
                            data = json.loads(line[6:])  # Remove 'data: ' prefix
                            elapsed = time.time() - start_time
                            
                            if 'step' in data:
                                print(f"[{elapsed:.2f}s] Step: {data['step']}")
                                print(f"    Message: {data['message']}")
                                print(f"    Progress: {data.get('progress', 0)}%")
                                
                                # Show additional info for parsing steps
                                # Show partial result updates
                                if event_type == "partial_result" and "partial_result" in data:
                                    print(f"    Partial Result Update:")
                                    partial = data["partial_result"]
                                    if "requirements" in partial:
                                        req = partial["requirements"]
                                        if req.get("title"):
                                            print(f"        Title: {req["title"]}")
                                        if req.get("description"):
                                            print(f"        Description: {req["description"]}")
                                        if req.get("must_have", {}).get("technical_skills"):
                                            print(f"        Technical Skills: {req["must_have"]["technical_skills"]}")
                                        if req.get("must_have", {}).get("domain_experience"):
                                            print(f"        Domain Experience: {req["must_have"]["domain_experience"]}")
                                        if req.get("must_have", {}).get("soft_skills"):
                                            print(f"        Soft Skills: {req["must_have"]["soft_skills"]}")
                                        if req.get("nice_to_have"):
                                            print(f"        Nice to Have: {req["nice_to_have"]}")
                                    print()
                                if 'parsed_section' in data:
                                    print(f"    Parsed: {data['parsed_section']} = {data['parsed_content']}")
                                
                                if data['step'] == 'complete':
                                    print("\n=== Final Result ===")
                                    result = data.get('result', {})
                                    print(json.dumps(result, indent=2, ensure_ascii=False))
                                    break
                            
                            if data.get('error'):
                                print(f"ERROR: {data['message']}")
                                break
                                
                        except json.JSONDecodeError as e:
                            print(f"Failed to parse SSE data: {line}")
                            print(f"Error: {e}")
                
        except Exception as e:
            print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(test_streaming_api()) 