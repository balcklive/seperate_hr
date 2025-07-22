# Author: Peng Fei
# LLM tools for intelligent job requirement processing

import json
import os
from typing import Dict, Any
from openai import OpenAI
from config.settings import MODEL_NAME, TEMPERATURE, MAX_TOKENS, OPENAI_API_KEY

class LLMTools:
    def __init__(self):
        # Use API key from environment variables
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    def determine_scenario(self, user_input: str) -> str:
        """
        Use LLM to determine if user input contains detailed job description
        
        Args:
            user_input: User's input text
            
        Returns:
            str: "detailed_jd" or "need_conversation"
        """
        prompt = f"""
        Analyze the following user input and determine if it contains detailed job description information.

        User input:
        {user_input}

        Please determine:
        1. If the input contains detailed job information (skills, experience, responsibilities, etc.), return "detailed_jd"
        2. If the input lacks sufficient information or needs further inquiry, return "need_conversation"

        Return only one of the above options without any explanation.
        """
        
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a professional job description analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=TEMPERATURE,
            max_tokens=50
        )
        
        result = response.choices[0].message.content.strip().lower()
        return "detailed_jd" if "detailed_jd" in result else "need_conversation"
    
    def parse_job_description(self, jd_text: str) -> Dict[str, Any]:
        """
        Use LLM to parse detailed job description into structured format
        
        Args:
            jd_text: Job description text
            
        Returns:
            Dict: Parsed structured data
        """
        prompt = f"""
        Analyze the following job description and extract structured information. 
        Please output in JSON format only, without any explanation text.

        Job Description:
        {jd_text}

        Please extract the following information and return as JSON:
        {{
            "title": "job title",
            "description": "job description summary",
            "must_have": {{
                "technical_skills": ["skill1", "skill2"],
                "domain_experience": ["experience1", "experience2"],
                "soft_skills": ["skill1", "skill2"]
            }},
            "nice_to_have": ["bonus1", "bonus2"]
        }}

        Guidelines:
        1. technical_skills: programming languages, frameworks, tools, etc.
        2. domain_experience: industry experience, business domain knowledge
        3. soft_skills: communication, leadership, teamwork, etc.
        4. nice_to_have: non-essential but preferred skills or experience
        5. If no information is found for a category, return empty array
        """
        
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a professional job description analyst specializing in extracting and categorizing skill requirements."},
                {"role": "user", "content": prompt}
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            return result
        except json.JSONDecodeError:
            return self._get_default_structure()
    
    def generate_questions(self, current_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Use LLM to generate structured questions for scenario 2
        
        Args:
            current_info: Current job information
            
        Returns:
            Dict: Structured questions with options
        """
        context = ""
        if current_info:
            context = f"Current information: {json.dumps(current_info, indent=2)}"
        
        prompt = f"""
        Generate structured questions to gather job requirements information.
        
        {context}
        
        Please generate questions in the following JSON format:
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
        
        Generate relevant questions based on what information is still needed.
        """
        
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a professional HR specialist who creates structured interview questions."},
                {"role": "user", "content": prompt}
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            return result
        except json.JSONDecodeError:
            return self._get_default_questions()
    
    def parse_user_response(self, response: str, current_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Use LLM to parse user response and update job information
        
        Args:
            response: User's response text
            current_info: Current job information
            
        Returns:
            Dict: Updated job information and completion status
        """
        context = ""
        if current_info:
            context = f"Current job information: {json.dumps(current_info, indent=2)}"
        
        prompt = f"""
        Parse the following user response and update job information accordingly.
        
        User response: {response}
        {context}
        
        Please update the job information based on the user's response and return in JSON format:
        {{
            "updated_info": {{
                "title": "updated title",
                "description": "updated description",
                "must_have": {{
                    "technical_skills": ["updated skills"],
                    "domain_experience": ["updated experience"],
                    "soft_skills": ["updated skills"]
                }},
                "nice_to_have": ["updated bonuses"]
            }},
            "is_complete": true/false
        }}
        """
        
        response_obj = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a professional job description analyst who updates information based on user input."},
                {"role": "user", "content": prompt}
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        
        try:
            result = json.loads(response_obj.choices[0].message.content)
            return result
        except json.JSONDecodeError:
            return {"updated_info": current_info or self._get_default_structure(), "is_complete": False}
    
    def _get_default_structure(self) -> Dict[str, Any]:
        """Default structure for job requirements"""
        return {
            "title": "",
            "description": "",
            "must_have": {
                "technical_skills": [],
                "domain_experience": [],
                "soft_skills": []
            },
            "nice_to_have": []
        }
    
    def _get_default_questions(self) -> Dict[str, Any]:
        """Default questions structure"""
        return {
            "session_id": "",
            "questions_with_options": []
        } 