# Author: Peng Fei
# Format conversion tool using LLM to ensure correct output structure

from typing import Dict, Any
from config.settings import OUTPUT_TEMPLATE, MODEL_NAME, TEMPERATURE, MAX_TOKENS
from tools.llm_tools import LLMTools

def format_output(parsed_data: Dict[str, Any], session_id: str = None) -> Dict[str, Any]:
    """
    Format output using LLM to ensure correct structure
    
    Args:
        parsed_data: Parsed job data
        session_id: Session identifier
        
    Returns:
        Dict: Formatted output in required structure
    """
    llm_tools = LLMTools()
    
    prompt = f"""
    Format the following parsed job data into the required output structure.
    
    Parsed data:
    {parsed_data}
    
    Session ID: {session_id or ""}
    
    Please format into this exact structure:
    {{
        "session_id": "session_id",
        "requirements": {{
            "title": "job title",
            "description": "job description",
            "must_have": {{
                "technical_skills": [],
                "domain_experience": [],
                "soft_skills": []
            }},
            "nice_to_have": []
        }}
    }}
    
    Ensure all fields are properly filled and the structure is exactly as specified.
    """
    
    response = llm_tools.client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a data formatting specialist."},
            {"role": "user", "content": prompt}
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )
    
    try:
        import json
        result = json.loads(response.choices[0].message.content)
        return result
    except:
        # Fallback to template
        formatted = OUTPUT_TEMPLATE.copy()
        formatted["session_id"] = session_id or ""
        formatted["requirements"].update(parsed_data)
        return formatted 