

from Doctor.models import Doctor, DoctorWithHospital


def user_asked_to_get_doctor_details(
    doctor_id = None,
    is_asked_about_available_hospitals=False,
    messages = []
):

    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except:
        return 'Sorry! This doctor does not exists'
    
    else:

        from ChatXpo.Sockets.Constant.Query import askChatXpo

        messages.append({'role' : 'system', 'content' : f'Name : {doctor.name}, ID : {str(doctor.id)}, Heading : {doctor.heading}, Working Since : {doctor.working_since.strftime("%d-%m-%Y")}, Approved : {doctor.is_approved}, About Doctor : {doctor.desc}'})
        messages.append({'role' : 'system', 'content' : f'Years of Experience : {doctor.years_of_experience}'})
        fee_range = doctor.fee_range
        if fee_range:
            messages.append({'role' : 'system', 'content' : f'Fee Range : Rs. {fee_range[0]} - Rs. {fee_range[1]}'})
        
        is_available_today = doctor.is_available_today
        if is_available_today:
            messages.append({'role' : 'system', 'content' : f'Available Today : {is_available_today.day.day} - {is_available_today.start_time.strftime("%I:%M %p")}'})
        
        if is_asked_about_available_hospitals:
            hospitals = DoctorWithHospital.objects.filter(doctor = doctor).values_list('hospital__name', flat=True)
            hospitals_string = ''
            for h in hospitals:
                hospitals_string += f'{h}, '
            messages.append({'role' : 'system', 'content' : 'List of available hospitals : ' + hospitals_string})
        
        response = askChatXpo(
            'Kindly Give me detail about this doctor',
            previousQueries=messages,
            onlyText=True,
        )
        return response

    