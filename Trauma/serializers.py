


from rest_framework import serializers

from Trauma.models import Speciality, Disease

class SpecialitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Speciality
        fields = ['id', 'name', 'svg_icon', 'color_code', 'description', 'image' ]

class DiseaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Disease
        fields = ['id', 'name', 'svg_icon', 'color_code', 'description', 'image' ]