from rest_framework import serializers
from ..dal import models

class FamiliesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Families
        fields = '__all__'


class PaidGuardsSerializer(serializers.ModelSerializer):

    family_id = FamiliesSerializer(read_only=True)

    class Meta:
        model = models.PaidGuards
        fields = [
            'pguard_id', 
            'family_id', 
            'pguard_name', 
            'pguard_phone', 
            'pguard_email', 
            'armed', 
            'pguard_pic'
            ]
        

class FguardSerializer(serializers.ModelSerializer):

    family_id = FamiliesSerializer(read_only=True)

    class Meta:
        model = models.Fguard
        fields = [
            'fguard_id', 
            'family_id', 
            'fguard_name', 
            'fguard_phone', 
            'fguard_email', 
            'armed', 
            'fguard_pic'
            ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Position
        fields = '__all__'


class ShiftSerializer(serializers.ModelSerializer):

    fguard_id = FguardSerializer(many=True, read_only=True)
    pguard_id = PaidGuardsSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Shift
        fields = [
            'shift_id', 
            'fguard_id', 
            'pguard_id', 
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

    origin_guard_id = FguardSerializer(read_only=True)
    substitute_fguard_id = FguardSerializer(read_only=True)
    substitute_Pguard_id = PaidGuardsSerializer(read_only=True)
    position_id = PositionSerializer(read_only=True)

    class Meta:
        model = models.Exchanges
        fields = [
            'exchange_id', 
            'exchange_date', 
            'exchange_day', 
            'exchange_hour', 
            'position_id',
            'origin_guard_id', 
            'substitute_fguard_id', 
            'substitute_Pguard_id', 
            'exchange_type'
            ]
        
