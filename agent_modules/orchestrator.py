# Author: Peng Fei
# Orchestrator agent for job requirement generation system

from agents import Agent
from tools.llm_tools import LLMTools
from agent_modules.jd_parser import JDParserAgent

class OrchestratorAgent:
    def __init__(self):
        self.llm_tools = LLMTools()
        self.jd_parser = JDParserAgent()
        
        self.agent = Agent(
            name="orchestrator",
            instructions="""
            You are the main controller for the job requirement generation system.
            Your responsibilities:
            1. Analyze user input to determine the scenario
            2. Route to appropriate processing agent
            3. Coordinate workflow between different agents
            4. Ensure proper output format
            """,
            tools=[self.llm_tools.determine_scenario, self.handoff_to_jd_parser]
        )
    
    def process_input(self, user_input: str, session_id: str = None) -> dict:
        """
        Process user input and determine next steps
        
        Args:
            user_input: User's job description or conversation
            session_id: Session identifier
            
        Returns:
            dict: Processed result or questions for further conversation
        """
        # Use LLM to determine scenario
        scenario = self.llm_tools.determine_scenario(user_input)
        
        if scenario == "detailed_jd":
            # Route to JD parser
            return self.jd_parser.parse_jd(user_input, session_id)
        else:
            # Generate questions for conversation
            return self.llm_tools.generate_questions()
    
    def handoff_to_jd_parser(self, jd_text: str, session_id: str = None):
        """Handoff to JD parser agent"""
        return self.jd_parser.parse_jd(jd_text, session_id) 