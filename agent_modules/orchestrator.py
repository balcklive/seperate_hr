# Author: Peng Fei
# Orchestrator agent for job requirement generation system

from agents import Agent
from tools.llm_tools import LLMTools
from tools.streaming_llm import StreamingLLMTools
from agent_modules.jd_parser import JDParserAgent
from typing import AsyncGenerator, Dict, Any

class OrchestratorAgent:
    def __init__(self):
        self.llm_tools = LLMTools()
        self.streaming_llm = StreamingLLMTools()
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
        Process user input and determine next steps (synchronous version)
        
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
    
    async def process_input_stream(self, user_input: str, session_id: str = None) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Process user input with streaming output (asynchronous version)
        
        Args:
            user_input: User's job description or conversation
            session_id: Session identifier
            
        Yields:
            Dict: Streaming processing results
        """
        try:
            # Step 1: Start processing
            yield {
                "event": "progress",
                "data": {
                    "step": "started",
                    "message": "Starting job description analysis...",
                    "progress": 5
                }
            }
            
            # Step 2: Parse job description with real-time result building
            yield {
                "event": "progress",
                "data": {
                    "step": "parsing",
                    "message": "Analyzing job description...",
                    "progress": 10
                }
            }
            
            # Initialize partial result
            partial_result = {
                "session_id": session_id or "",
                "requirements": {
                    "title": "",
                    "description": "",
                    "must_have": {
                        "technical_skills": [],
                        "domain_experience": [],
                        "soft_skills": []
                    },
                    "nice_to_have": []
                }
            }
            
            # Stream JD parsing with partial result updates
            parsed_data = {}
            async for parse_chunk in self.streaming_llm.stream_parse_job_description(user_input):
                if parse_chunk["type"] == "section_complete":
                    section = parse_chunk["section"]
                    content = parse_chunk["content"]
                    parsed_data[section] = content
                    
                    # Update partial result based on section
                    if section == "title":
                        partial_result["requirements"]["title"] = content
                    elif section == "description":
                        partial_result["requirements"]["description"] = content
                    elif section == "technical_skills":
                        partial_result["requirements"]["must_have"]["technical_skills"] = content if isinstance(content, list) else []
                    elif section == "domain_experience":
                        partial_result["requirements"]["must_have"]["domain_experience"] = content if isinstance(content, list) else []
                    elif section == "soft_skills":
                        partial_result["requirements"]["must_have"]["soft_skills"] = content if isinstance(content, list) else []
                    elif section == "nice_to_have":
                        partial_result["requirements"]["nice_to_have"] = content if isinstance(content, list) else []
                    
                    # Yield partial result update
                    yield {
                        "event": "partial_result",
                        "data": {
                            "step": "parsing",
                            "message": f"Completed analysis of {section}",
                            "progress": 20 + (len(parsed_data) * 15),
                            "partial_result": partial_result.copy(),
                            "completed_section": section
                        }
                    }
                
                elif parse_chunk["type"] == "analysis_complete":
                    yield {
                        "event": "progress",
                        "data": {
                            "step": "formatting",
                            "message": "Finalizing results...",
                            "progress": 90
                        }
                    }
                    break
            
            # Final result
            yield {
                "event": "complete",
                "data": {
                    "step": "complete",
                    "message": "Job description processing completed",
                    "progress": 100,
                    "result": partial_result
                }
            }
                
        except Exception as e:
            yield {
                "event": "error",
                "data": {
                    "step": "error",
                    "message": f"Error during processing: {str(e)}",
                    "progress": 0,
                    "error": True
                }
            }
    
    def _format_parsed_data(self, parsed_data: Dict[str, Any], session_id: str = None) -> Dict[str, Any]:
        """
        Format parsed data into final result structure
        
        Args:
            parsed_data: Parsed job data
            session_id: Session identifier
            
        Returns:
            Dict: Formatted result
        """
        # Import formatter here to avoid circular imports
        from tools.formatter import format_output
        
        # Create a structured data object for formatting
        structured_data = {
            "title": parsed_data.get("title", ""),
            "description": parsed_data.get("description", ""),
            "must_have": {
                "technical_skills": parsed_data.get("technical_skills", []),
                "domain_experience": parsed_data.get("domain_experience", []),
                "soft_skills": parsed_data.get("soft_skills", [])
            },
            "nice_to_have": parsed_data.get("nice_to_have", [])
        }
        
        return format_output(structured_data, session_id)
    
    def handoff_to_jd_parser(self, jd_text: str, session_id: str = None):
        """Handoff to JD parser agent"""
        return self.jd_parser.parse_jd(jd_text, session_id)
