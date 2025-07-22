# Author: Peng Fei
# Main entry point for job requirement generator

import json
import argparse
import asyncio
from agent_modules.orchestrator import OrchestratorAgent
from utils.session_manager import SessionManager
from api.server import run_server
from tests.sse_client_test import SSETestClient

def run_cli_mode():
    """Run in CLI mode for testing"""
    # Initialize session manager
    session_manager = SessionManager()
    
    # Initialize orchestrator agent
    orchestrator = OrchestratorAgent()
    
    # Example usage - Scenario 1: Detailed JD
    jd_text = """
    Senior Software Engineer
    
    We are looking for a Senior Software Engineer with 5+ years of experience in Python, 
    JavaScript, and cloud technologies. The ideal candidate should have experience with 
    microservices architecture, Docker, and Kubernetes. Strong problem-solving skills 
    and excellent communication abilities are required. Experience with machine learning 
    frameworks and data engineering is a plus.
    """
    
    print("=== Processing Detailed Job Description ===")
    result = orchestrator.process_input(jd_text)
    print(json.dumps(result, indent=2, ensure_ascii=False))

async def run_test_mode():
    """Run in test mode to test SSE API"""
    print("=== Running SSE API Test ===")
    test_client = SSETestClient()
    await test_client.test_sse_connection()

def main():
    """Main function with CLI argument support"""
    parser = argparse.ArgumentParser(description='Job Requirement Generator')
    parser.add_argument('--mode', choices=['cli', 'api', 'test'], default='cli',
                       help='Run mode: cli (command line), api (SSE server), or test (SSE client test)')
    
    args = parser.parse_args()
    
    if args.mode == 'api':
        run_server()
    elif args.mode == 'test':
        asyncio.run(run_test_mode())
    else:
        run_cli_mode()

if __name__ == "__main__":
    main() 