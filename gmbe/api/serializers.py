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


class PositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Position
        fields = '__all__'


class ShiftSerializer(serializers.ModelSerializer):

    family_id = FamiliesSerializer(many=True, read_only=True)

    class Meta:
        model = models.Shift
        fields = [
            'shift_id', 
            'family_id', 
            'position_id', 
            'shift_hour', 
            'shift_date', 
            'shift_day'
            ]

class GuardinglistSerializer(serializers.ModelSerializer):

    shifts = ShiftSerializer(many=True)
    glist_position_id = PositionSerializer()
    last_guard_id = FamiliesSerializer()

    class Meta:
        model = models.GuardingList
        fields = [
            'guarding_list_id', 
            'last_guard_id', 
            'glist_position_id', 
            'glist_date', 
            'glist_day', 
            'shifts'
            ]


class SetGuardingListSerializer(serializers.ModelSerializer):

    shifts = serializers.DictField()
    guard_id = FamiliesSerializer(read_only=True)
    position_id  = PositionSerializer()
    
    class Meta:
        model = models.SetGuardingList
        fields = [
            'list_date', 
            'list_day', 
            'shifts', 
            'guard_id', 
            'last_guard_id', 
            'position_id'
            ]


class ExchangesSerializer(serializers.ModelSerializer):

    origin_guard_id = FamiliesSerializer(read_only=True)
    substitute_guard_id = FamiliesSerializer(read_only=True)

    class Meta:
        model = models.Exchanges
        fields = [
            'exchange_id', 
            'exchange_date', 
            'exchange_day', 
            'exchange_hour', 
            'origin_guard_id', 
            'substitute_guard_id', 
            'exchange_type'
            ]
        

class PaidGuardsSerializer(serializers.ModelSerializer):

    puard_family_id = FamiliesSerializer(read_only=True)

    class Meta:
        model = models.PaidGuards
        fields = ['paid_guard_id', 'pguard_name', 'puard_phone', 'puard_family_id']