
from datetime import datetime

from .Doctor.Functions import GPT_COMMON_FUNCTIONS as DoctorFunctions
from .Appointment.Functions import GPT_COMMON_FUNCTIONS as AppointmentFunctions

GPT_COMMON_FUNCTIONS = []


GPT_COMMON_FUNCTIONS.extend(AppointmentFunctions)
GPT_COMMON_FUNCTIONS.extend(DoctorFunctions)