# Author: Peng Fei
# JD parser agent for intelligent job description analysis

from agents import Agent
from tools.llm_tools import LLMTools
from tools.formatter import format_output

class JDParserAgent:
    def __init__(self):
        self.llm_tools = LLMTools()
        
        self.agent = Agent(
            name="jd_parser",
            instructions="""
            You are a JD parsing expert. Your tasks:
            1. Receive detailed job descriptions
            2. Use LLM to intelligently analyze job requirements
            3. Extract job title, description, required skills, and nice-to-have items
            4. Categorize skills into technical, domain experience, and soft skills
            5. Output standardized JSON format
            """,
            tools=[self.llm_tools.parse_job_description, format_output]
        )
    
    def parse_jd(self, jd_text: str, session_id: str = None) -> dict:
        """
        Parse job description using LLM
        
        Args:
            jd_text: Job description text
            session_id: Session identifier
            
        Returns:
            dict: Standardized job requirements JSON
        """
        # Use LLM to parse job description
        parsed_data = self.llm_tools.parse_job_description(jd_text)
        
        # Format output
        formatted_output = format_output(parsed_data, session_id)
        
        return formatted_output 