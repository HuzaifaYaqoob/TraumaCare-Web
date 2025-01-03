

categories_dict = {
    "Medicine": [
        "Energy Boosters", "Diet Supplements", "Allergy", "Anti Bacterials", "Anti Coagulants", "Anti Psychotics", "Asthma",
        "Cardiac Blood Medications", "Cholesterol Control", "Diabetic Management",
        "Neurology Medication", "Pain Killers", "Prescription Drugs", "Rheumatic Medication",
        "Steroids", "Topical Infections", "Vitamin B", "Vitamin C", "Vitamin D", "Vitamin E",
        "Supplements", "Antioxidants", "Oral Anti Diabetics", "Ulcer", "Injectable Anti Cancer",
        "Proton Pump Inhibitors", "Macrolides", "Bacterial Infections", "Surgical Medication",
        "Oral Asthma Preparations", "Epilepsy", "IBS", "Oncology Medication", "Specialty Medication",
        "H2 Receptor Antagonist", "Bronchodilators", "Respiratory Medication", "Anti Viral", "Diabetes",
        "Self Medications", "Other Cardiac Therapy", "Headache", "Cough Cold and Allergy",
        "Nervous System Disorders", "Sleep disorders", "Neuropathic Pain", "Malaria", "Local steroids",
        "Over The Counter Drugs", "Mood Elevators", "Skin Concern", "Topical Infections", "Burns",
        "Vitamins", "Vitamin B", "Vitamin C", "Vitamin D", "Vitamin E", "Minerals", "Calcium", "Iron", "Magnesium", "Chromium",
        "Vitamins and Nutritional Supplements", "Vitamins and supplements", "Medications", "Pregnancy Care", "Neurology", "Eye", "Infections", 
        "Ocular Anti Infectives", "High Blood Pressure", "Heart Disorders", 
        "Pain Relief", "Blood", "Intravenous Fluids", "Cancer", "Bone Disorders", 
        "Osteoporosis", "Lungs", "Cold and Flu", "Fever", "Beta Blocker", 
        "Diarrhea", "Anti fungals", "Eye and Ear Medication", "Stomach and Bowel", 
        "Respiratory Care", "Other Oral Anti Diabetics", "Herbal", "Gastrointestinal Disorders", 
        "Dyspepsia", "Haemorrhoids", "Sulfonylureas", "Liver", "Kidney Disorders", 
        "Oral Pain Killers", "Other Bacterial Infections", "Penicillins", 
        "Blood Cell Deficiencies", "Calcium Channel Blockers", "Multiple Sclerosis Medications", 
        "Sore Throat", "Fish Oil and Omega 3", "Homeopathic Drugs", "Male Sexual Dysfunction", 
        "Calcium and Mineral Supplement", "Muscle Pain Relief", "Ointments"
    ],
    "Non Medicine": [
        "Sun Care", "Baby Care", "Diet Supplements", "Energy Boosters", "Beauty and Skin",
        "Hair Care", "Hairloss Treatment", "Bath & Body", "Face Wash", "Face Serums",
        "Feminine Care", "Immunity Boosters", "Hand Sanitizers", "Sun Block", "Skin Care",
        "Skin Supplements", "Teething Essentials", "Toothpaste", "Tooth Brush", "Maternity Care",
        "Hair Conditioner", "Hair Serum", "Shower Gel", "Hair Mask", "Serums", "Hand Soap",
        "Face Whitening", "Body Care", "Baby Skin & Hair", "Hair Styling", "Hair Nourishment",
        "Baby Sun Care", "Baby Lotion", "Bath Accessories", "Face Masks", "Hair Oil",
        "Hair Supplements", "Lotions", "Sensitive & Irritated Scalp", "Hair Spray",
        "Vitamin D", "Multivitamins", "Baby Remedies", "Feminine Care", "Diabetic Foot and Skin Care",
        "Plant Sourced Supplements", "Vitamins and Nutritional Supplements", "Sexual Healthcare", "Mouth Wash", "Oral Gel", "Eye and Vision Support", "Dry Eyes", 
        "Face Mask & Sanitizers", "Eczema", "Non Sedative Anti Histamine", "Oral Care", 
        "Diabetic Supplements", "Herbal Remedies", "Rehydration", "Ginseng & Guarana", 
        "Condoms", "Hair", " Skin & Nails", "Soaps & Sanitizers", "Baby Oil", 
        "Nasal Allergy", "Bath and Body", "Grooming", "shampoos", "Nappy Rash", 
        "Diapers & Wipes", "Mothercare", "Solid & Semi Solid Food", "Skin Soap", 
        "Hair Removal Creams", "Mask", "Hair and Scalp Treatment", "Sexual Wellness", 
        "Dandruff", "Medicated Shampoo", "Hair Color", "Damaged & Brittle Hair", 
        "Mosquito Repellents", "Maca", "Lice Treatment", "Amino Acid", "Men Care", "Selenium"
    ],
    "Healthcare Equipment & Accessories": [
        "Surgicals and Disposables", "Wheelchairs & Canes", "Nebulizer", "Blood Pressure Monitors", "Diabetic Monitors and Strips",
        "Surgical Support", "Pacifiers & Soothers", "Orthopedic Braces", "Medical Devices",
        "Respiratory Equipments", "Medical Device", "Home Health Care", "Home Healthcare",
        "Patient Therapy & Rehabilitation", "First Aid Kit", "Hand Wash", "Hand Sanitizers",
        "Medical Accessories", "First aid and disposables", "Wound care", "Surgical Care", "Orthopedic Soft Goods and Braces", "Wheel Chairs"
    ],
    "Consumer & Lifestyle Products": [
        "Hair Care", "Sun Care", "Face Wash", "Baby Feeding Essentials", "Baby Nutrition", "Milk Formula", "Milk Products",
        "Royal Jelly & Honey Derivatives", "Dietary Supplements", "Energy Boosters",
        "Healthy Food", "Collagen & Silica", "Mom & Baby", "Baby Food", "Baby Skin Treatments",
        "Baby Lotion", "Bathing Essentials", "Beauty", "Consumer Products", "Healthy Breathing",
        "Immunity Disorders", "Healthy Food", "Vitamins and Nutritional Supplements", "Facial Skin Care",
        "Bath and Body", "Grooming", "shampoos", "Nappy Rash", "Diapers & Wipes", 
        "Mothercare", "Solid & Semi Solid Food", "Skin Soap", "Hair Removal Creams", 
        "Hair and Scalp Treatment", "Hair Color", "Damaged & Brittle Hair", 
        "Face Mask & Sanitizers", "Eczema", "Mask", "Soaps & Sanitizers", "Baby Oil", 
        "Maca", "Mosquito Repellents", "Dandruff", "Medicated Shampoo", "Devices"
    ],
    "Others": [
        "Corona Essentials", "Shop by Condition", "Special Discounts", "Best Selling Collection",
        "New collection", "Smog Essentials", "Daily Essentials", "Sunscreen", "Masks",
        "Echinacea", "Garlic", "Chromium", "Iron", "Ginkgo Biloba", "Gels", "Sexual Healthcare",
        "Shop in Shop", "taxable18"
    ]
}





from django.core.management.base import BaseCommand

from Product.models import SubCategory, ProductCategory


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        for cat, sub_cats in categories_dict.items():
            cat, c_c = ProductCategory.objects.get_or_create(name=cat)
            for sbc in sub_cats:
                sbc, c = SubCategory.objects.get_or_create(name=sbc)
                sbc.category.add(cat)
                sbc.save()

        self.stdout.write(self.style.SUCCESS('Categories Added'))

