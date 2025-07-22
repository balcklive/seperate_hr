# Author: Peng Fei
# Main entry point for job requirement generator

import json
from agent_modules.orchestrator import OrchestratorAgent
from utils.session_manager import SessionManager

def main():
    """Main function"""
    # API key is automatically loaded from .env file via config/settings.py
    
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
    
    print("\n" + "="*50 + "\n")
    
    # Example usage - Scenario 2: Need conversation
    short_input = "I need a software engineer"
    
    print("=== Processing Short Input (Need Conversation) ===")
    result = orchestrator.process_input(short_input)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main() 