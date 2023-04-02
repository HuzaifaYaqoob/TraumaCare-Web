


from rest_framework import serializers

from Trauma.models import Speciality

class SpecialitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Speciality
        fields = ['id', 'name', 'svg_icon', 'color_code', 'description', 'image' ]