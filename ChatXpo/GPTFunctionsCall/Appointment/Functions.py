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
                    "description": f"Start Date of Slots range. Date must be onward from today date which is ({datetime.now().strftime('%Y-%m-%d')}), e.g YYYY-MM-DD"
                },
                "slotsCount": {
                    "type": "number",
                    "description": "Total slots user wants to see, e.g 2"
                },
            },
            "required": [
                "appointmentDate",
            ]
        }
    },
]

