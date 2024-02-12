from rest_framework import serializers
from dal import models

class FamiliesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Families
        fields = '__all__'