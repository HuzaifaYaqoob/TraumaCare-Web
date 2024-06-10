
from datetime import datetime


GPT_COMMON_FUNCTIONS = [
    {
        "name": "user_asked_to_get_doctor_details",
        "description": "If user asks or indicates that he wanted to know about doctor or specific Doctor.",
        "parameters": {
            "type": "object",
            "properties": {
                "doctor_id": {
                    "type": "string",
                    "description": f"If user asks or indicates that he wanted to know about doctor or specific Doctor. Return Doctor ID"
                },
                "is_asked_about_available_hospitals": {
                    "type": "boolean",
                    "description": f"If user indicates or shows his interest that he wanted to know about doctor as well his availability in Hospitals. Return True"
                },
            },
            "required": [
                "doctor_id",
            ]
        }
    },
]