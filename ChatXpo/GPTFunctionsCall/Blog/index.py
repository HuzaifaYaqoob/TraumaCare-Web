
from datetime import datetime, timedelta

from Doctor.models import DoctorWithHospital, DoctorTimeSlots, Doctor
from Appointment.models import Appointment, AppointmentGroup


from Blog.models import Tag, BlogPost, Category

def generate_blog_post(
    title = 'None',
    content = 'None',
    category = 'None',
    read_time = 3,
    tags = [],
    messages=[],
    **kwargs
):

    
    category, created = Category.objects.get_or_create(name = category)
    post = BlogPost.objects.create(
        title = title,
        gpt_content = content,
        content = content,
        category = category,
        read_time = read_time,
    )

    for tags in tags:
        Tag.objects.create(
            post = post,
            name = tags
        )

    return f'Created {title}'
