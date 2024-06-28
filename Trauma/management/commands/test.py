



from django.core.management.base import BaseCommand

import csv

from Blog.Cronjob import generateBlogPost
from Blog.models import BlogPostTopic

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        # generateBlogPost()


        posts_data = [
            'What Causes Skin Tags? And How to Remove Them',
            'Amazing Benefits Of Applying Ice On Your Face!',
            'Skincare For Men: Overview and Products To Use',
            'Acne and Acne Scars',
            'Home Remedies To Get Rid Of Dark Knuckles Fast!',
            'How To Whiten Skin Overnight Naturally',
            'Surgical Methods Of Face Rejuvenation',
            '10 Benefits Of Vitamin E Capsules For Hair And Skin',
            'What To Avoid When Taking Glutathione?',
            'How To Get Dimples Permanently Without Surgery',
            'How To Reduce Lip Size Naturally Without Surgery',
            'Is Vaseline Good For Your Face?',
            'Biotin: Benefits, Side Effects & More',
            '13 Amazing Benefits Of Shea Butter',
            'Hair Loss in Females: Causes, Treatment, and Prevention',
            'Common Causes Of Acne And How You Can Avoid Them',
            'Top 10 Reasons For Hair Fall And Its Remedies',
            'How To Cure Shingles In 3 Days – Is It Possible?',
            'How To Get Rid Of Bags Under Eyes',
            'Sciatica Pain in Women: Causes, Symptoms, and Management',
            'Knee Pain in Women: Causes, Symptoms, and Treatments',
            'Osteoarthritis: Causes, Symptoms, Diagnosis & Treatment',
            'Arthritis Of Joints – Symptoms, Types & Treatment',
            'Tennis Elbow – Causes, Symptoms & Treatment',
            'Dorsalgia: Types, Causes, Symptoms & Treatment',
            '5 Great Tips for a Healthy Spine',
            '4 Most Common Childhood Orthopedic Conditions',
            '5 Ways to Manage Bad Days With Rheumatoid Arthritis',
            '5 Best Tips for Exercising With Osteoarthritis',
            'Vitamin D Deficiency Makes Bones Age Faster, Research Finds',
            'Dorsalgia: Types, Causes, Symptoms & Treatment',
            'Warning Signs of Breast Cancer – Breast Cancer Awareness Month 2024',
            '10 Early Symptoms Of Lung Cancer – Lung Cancer Awareness Month 2024',
            'Exploring Bladder Cancer Treatments',
            '9 Subtle Signs Of Cancer You Shouldn’t Ignore',
            'Period Essentials: Dos & Don’ts You Should Know About',
            'Skincare For Men: Overview and Products To Use',
            '7 Amazing Benefits Of Applying Ice On Your Face!',
            'Hormonal Contraception: It’s Type and Usage',
            'Why Should You Not Use Vagina Whitening Creams?',
        ]

        for p in posts_data:
            BlogPostTopic.objects.create(name = p)


        self.stdout.write(self.style.SUCCESS('Successfully added Specialities'))

