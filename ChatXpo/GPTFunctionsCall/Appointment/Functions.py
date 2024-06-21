from datetime import datetime

GPT_COMMON_FUNCTIONS = [
    {
        "name": "appointment_get_doctor_availability",
        "description": "only If the user asks for available slots at any specific date and time OR If user asks for available slots in a range of date and time OR if user wants to know available time slots.",
        "parameters": {
            "type": "object",
            "properties": {
                "appointmentDate": {
                    "type": "string",
                    "description": f"Start Date of Slots range. Date must be onward from today date which is ({datetime.now().strftime('%Y-%m-%d')}), e.g YYYY-MM-DD. Slot date is not required from user. If user mentioned then that perfect, If not then return today's date"
                },
                "doctor_id": {
                    "type": "string",
                    "description": f"If user asks or indicates that he wanted to know about doctor or specific Doctor. Return Doctor ID"
                },
                "hospital_id": {
                    "type": "string",
                    "description": f"To know about Doctors available slots, Hospital ID is required. Return Hospital ID"
                },
                "slotsCount": {
                    "type": "number",
                    "description": "Total slots user wants to see, e.g 2"
                },
            },
            "required": [
                "hospital_id",
                "doctor_id",
            ]
        }
    },
    {
        "name": "book_user_appointment",
        "description": "only If the user asks for available slots at any specific date and time OR If user asks for available slots in a range of date and time OR if user wants to know available time slots.",
        "parameters": {
            "type": "object",
            "properties": {
                "appointmentDate": {
                    "type": "string",
                    "description": f"Start Date of Slots range. Date must be onward from today date which is ({datetime.now().strftime('%Y-%m-%d')}), e.g YYYY-MM-DD. Slot date is not required from user. If user mentioned then that perfect, If not then return today's date"
                },
                "doctor_id": {
                    "type": "string",
                    "description": f"If user asks or indicates that he wanted to know about doctor or specific Doctor. Return Doctor ID"
                },
                "hospital_id": {
                    "type": "string",
                    "description": f"To know about Doctors available slots, Hospital ID is required. Return Hospital ID"
                },
                "location_id": {
                    "type": "string",
                    "description": f"To know about Doctors available slots, Hospital ID is required. Return Hospital ID"
                },
                "selected_time": {
                    "type": "string",
                    "description": "Selected time in 24 hours format for appointment e.g 06:00:00"
                },
            },
            "required": [
                "hospital_id",
                "location_id",
                "doctor_id",
                "appointmentDate",
                "selected_time",
            ]
        }
    },
]

