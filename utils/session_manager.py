# Author: Peng Fei
# Session management utility for job requirement generator

import uuid
from datetime import datetime
from typing import Dict

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
    
    def create_session(self) -> str:
        """Create new session"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "status": "active",
            "created_at": datetime.now(),
            "data": {}
        }
        return session_id
    
    def get_session(self, session_id: str) -> Dict:
        """Get session information"""
        return self.sessions.get(session_id, {})
    
    def update_session(self, session_id: str, data: Dict) -> bool:
        """Update session data"""
        if session_id in self.sessions:
            self.sessions[session_id]["data"].update(data)
            return True
        return False
    
    def close_session(self, session_id: str) -> bool:
        """Close session"""
        if session_id in self.sessions:
            self.sessions[session_id]["status"] = "closed"
            return True
        return False 