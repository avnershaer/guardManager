from rest_framework import serializers
from ..dal import models


class FamiliesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Families
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = '__all__'