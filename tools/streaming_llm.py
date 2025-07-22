# Author: Peng Fei
# Streaming LLM tools for real-time job requirement processing

import json
import asyncio
from typing import AsyncGenerator, Dict, Any
from openai import OpenAI
from config.settings import MODEL_NAME, TEMPERATURE, MAX_TOKENS, OPENAI_API_KEY

class StreamingLLMTools:
    def __init__(self):
        # Use API key from environment variables
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    async def stream_parse_job_description(self, jd_text: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream parse job description using LLM with real-time output
        
        Args:
            jd_text: Job description text
            
        Yields:
            Dict: Streaming parsed data chunks
        """
        prompt = f"""
        Analyze the following job description and extract structured information step by step.
        Please provide your analysis in real-time as you process each section.

        Job Description:
        {jd_text}

        Please analyze and output in this order:
        1. Job title
        2. Job description summary
        3. Technical skills (programming languages, frameworks, tools)
        4. Domain experience (industry experience, business domain knowledge)
        5. Soft skills (communication, leadership, teamwork)
        6. Nice-to-have skills (non-essential but preferred)

        Output each section as it's analyzed, using this format:
        {{"section": "title", "content": "extracted title"}}
        {{"section": "description", "content": "extracted description"}}
        {{"section": "technical_skills", "content": ["skill1", "skill2"]}}
        {{"section": "domain_experience", "content": ["exp1", "exp2"]}}
        {{"section": "soft_skills", "content": ["skill1", "skill2"]}}
        {{"section": "nice_to_have", "content": ["bonus1", "bonus2"]}}
        """
        
        try:
            stream = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a professional job description analyst. Provide real-time analysis as you process each section."},
                    {"role": "user", "content": prompt}
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                stream=True
            )
            
            current_section = ""
            current_content = ""
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    current_content += content
                    
                    # Try to parse complete JSON objects
                    if content.strip().endswith('}'):
                        try:
                            # Look for complete JSON objects in the accumulated content
                            lines = current_content.split('\n')
                            for line in lines:
                                line = line.strip()
                                if line.startswith('{') and line.endswith('}'):
                                    try:
                                        data = json.loads(line)
                                        if 'section' in data and 'content' in data:
                                            yield {
                                                "type": "section_complete",
                                                "section": data["section"],
                                                "content": data["content"],
                                                "message": f"Completed analysis of {data['section']}"
                                            }
                                    except json.JSONDecodeError:
                                        continue
                        except Exception as e:
                            # If parsing fails, yield the raw content
                            yield {
                                "type": "content_chunk",
                                "content": content,
                                "message": "Processing job description..."
                            }
                    else:
                        # Yield partial content for real-time feedback
                        yield {
                            "type": "content_chunk",
                            "content": content,
                            "message": "Analyzing job description..."
                        }
            
            # Final yield to indicate completion
            yield {
                "type": "analysis_complete",
                "message": "Job description analysis completed"
            }
            
        except Exception as e:
            yield {
                "type": "error",
                "message": f"Error during analysis: {str(e)}"
            }
    
    async def stream_determine_scenario(self, user_input: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream determine scenario using LLM
        
        Args:
            user_input: User's input text
            
        Yields:
            Dict: Streaming scenario analysis
        """
        prompt = f"""
        Analyze the following user input and determine if it contains detailed job description information.
        Provide your analysis in real-time.

        User input:
        {user_input}

        Please analyze:
        1. Level of detail in the input
        2. Presence of specific job requirements
        3. Whether additional information is needed
        4. Final determination: "detailed_jd" or "need_conversation"
        """
        
        try:
            stream = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a professional job description analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=TEMPERATURE,
                max_tokens=200,
                stream=True
            )
            
            analysis_text = ""
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    analysis_text += content
                    
                    yield {
                        "type": "analysis_chunk",
                        "content": content,
                        "message": "Analyzing input detail level..."
                    }
            
            # Determine final scenario
            scenario = "detailed_jd" if "detailed_jd" in analysis_text.lower() else "need_conversation"
            
            yield {
                "type": "scenario_determined",
                "scenario": scenario,
                "message": f"Determined scenario: {scenario}"
            }
            
        except Exception as e:
            yield {
                "type": "error",
                "message": f"Error during scenario analysis: {str(e)}"
            }
    
    async def stream_generate_questions(self, current_info: Dict[str, Any] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream generate structured questions using LLM
        
        Args:
            current_info: Current job information
            
        Yields:
            Dict: Streaming question generation
        """
        context = ""
        if current_info:
            context = f"Current information: {json.dumps(current_info, indent=2)}"
        
        prompt = f"""
        Generate structured questions to gather job requirements information.
        Provide your analysis and question generation in real-time.

        {context}
        
        Please generate questions in this JSON format:
        {{
            "session_id": "",
            "questions_with_options": [
                {{
                    "question": "What is the primary role type for this position?",
                    "options": [
                        {{"text": "Technical/Engineering", "value": "technical", "description": "Software development, data engineering, DevOps roles"}},
                        {{"text": "Product Management", "value": "product", "description": "Product strategy, roadmap planning, stakeholder management"}}
                    ],
                    "allow_custom_input": true,
                    "required": true
                }}
            ]
        }}
        """
        
        try:
            stream = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a professional HR specialist who creates structured interview questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                stream=True
            )
            
            question_text = ""
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    question_text += content
                    
                    yield {
                        "type": "question_chunk",
                        "content": content,
                        "message": "Generating structured questions..."
                    }
            
            # Try to parse the complete questions JSON
            try:
                questions_data = json.loads(question_text)
                yield {
                    "type": "questions_complete",
                    "questions": questions_data,
                    "message": "Questions generation completed"
                }
            except json.JSONDecodeError:
                yield {
                    "type": "questions_complete",
                    "questions": self._get_default_questions(),
                    "message": "Using default questions structure"
                }
            
        except Exception as e:
            yield {
                "type": "error",
                "message": f"Error during question generation: {str(e)}"
            }
    
    def _get_default_questions(self) -> Dict[str, Any]:
        """Get default questions structure"""
        return {
            "session_id": "",
            "questions_with_options": [
                {
                    "question": "What is the primary role type for this position?",
                    "options": [
                        {"text": "Technical/Engineering", "value": "technical", "description": "Software development, data engineering, DevOps roles"},
                        {"text": "Product Management", "value": "product", "description": "Product strategy, roadmap planning, stakeholder management"},
                        {"text": "Sales/Marketing", "value": "sales", "description": "Customer acquisition, revenue generation, market expansion"},
                        {"text": "Operations", "value": "operations", "description": "Process optimization, team management, strategic planning"}
                    ],
                    "allow_custom_input": True,
                    "required": True
                }
            ]
        } 