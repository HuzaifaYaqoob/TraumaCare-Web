

from rest_framework import serializers

from Pharmacy.models import Store, StoreLocation, StoreProductFile


class StoreProductFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreProductFile
        fields = '__all__'