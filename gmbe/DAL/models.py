from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
#import json


class UserRole(models.Model):
    role_id = models.BigAutoField(primary_key=True)
    role_name = models.CharField(max_length=25, unique=True)
    
    def __str__(self) -> str:
        return self.role_name
    

class Families(models.Model):

    family_id = models.BigAutoField(primary_key=True)
    family_name = models.CharField(max_length=100, blank=False, null=False, default='')
    family_pic = models.ImageField(upload_to='families_pics', default='', blank=True, null=True) 
    name1 = models.CharField(max_length = 25, blank=False, null=False)
    phone1 = models.CharField(max_length = 25, blank=False, default='', null=False, unique=True)
    armed1 = models.BooleanField(default = False)
    name2 = models.CharField(max_length = 25, blank=True, null=True)
    phone2 = models.CharField(max_length = 25, blank=True, null=True)
    armed2 = models.BooleanField(default = False)
    id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    role_name = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=True)
    
    def __str__(self) -> str:
        return self.family_name
    

class Position(models.Model):

    position_id = models.BigAutoField(primary_key=True)
    position_name = models.CharField(max_length=100, blank=False, null=False, default='')

    def __str__(self) -> str:
        return self.position_name


class Shift(models.Model):
    shift_id = models.BigAutoField(primary_key=True)
    family_id = models.ManyToManyField(Families, related_name='shift_family_id')
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='Shift_position_id', default='')
    shift_hour = models.CharField(max_length=10, blank=False, null=False, default='')
    shift_date = models.DateField(default=timezone.now)
    shift_day = models.CharField(max_length=10, blank=False, null=False, default='')


class GuardingList(models.Model):
    
    guarding_list_id = models.BigAutoField(primary_key=True)
    last_guard_id = models.ForeignKey(Families, on_delete=models.CASCADE, related_name='GuardingList_last_guard_id', default='')
    glist_position_id = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='GuardingList_position_id', default='')
    glist_date = models.DateField(default=timezone.now)
    glist_day = models.CharField(max_length=10,default='')
    shifts = models.ManyToManyField(Shift, related_name='guardinglist_shifts', default='NO SHIFTS')

class SetGuardingList(models.Model):

    list_date = models.CharField(max_length=15 , default='')    
    list_day = models.CharField(max_length=15 , default='')    
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='SetGuardingList_position_id', default='')   
    shifts = models.TextField(default='') 
    last_guard_id = models.ForeignKey(Families, on_delete=models.CASCADE, related_name='SetGuardingList_last_guard_id', default='')


class Exchanges(models.Model):

    exchange_id = models.BigAutoField(primary_key=True)
    exchange_date = models.CharField(max_length=15 , default='')
    exchange_day = models.CharField(max_length=15 , default='')
    exchange_hour = models.CharField(max_length=8 , default='')
    origin_guard_id = models.ForeignKey(Families, on_delete=models.CASCADE, related_name='Exchanges_origin_guard_id', default='')
    substitute_guard_id = models.ForeignKey(Families, on_delete=models.CASCADE, related_name='Exchanges_substitute_guard_id', default='')
    exchange_type = models.CharField(max_length=8 , default='')


class PaidGuards(models.Model):

    paid_guard_id = models.BigAutoField(primary_key=True)
    pguard_name = models.CharField(max_length=100, blank=False, null=False, default='')
    puard_phone = models.CharField(max_length = 25, blank=True, null=True)
    puard_family_id = models.ForeignKey(Families, on_delete=models.CASCADE, related_name='PaidGuards_family_id', default='')