from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
#import json


class UserRole(models.Model):
    role_id = models.BigAutoField(primary_key=True)
    role_name = models.CharField(max_length=25, unique=True)
    
    def __str__(self) -> str:
        return self.role_name
    

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_role = models.ForeignKey(UserRole, on_delete=models.CASCADE, related_name='Custom_user_role', default='')


class Families(models.Model):

    family_id = models.BigAutoField(primary_key=True)
    family_name = models.CharField(max_length=100, blank=False, null=False, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self) -> str:
        return self.family_name
    

class Fguard(models.Model):
    fguard_id = models.BigAutoField(primary_key=True)
    family_id = models.ForeignKey(Families, on_delete=models.CASCADE, related_name='fguard_family_id', default='')
    fguard_name =  models.CharField(max_length=100, blank=False, null=False, default='')
    fguard_phone = models.CharField(max_length = 25, blank=False, default='', null=False, unique=True)
    fguard_email = models.EmailField(max_length=200, unique=True, default='')
    armed = models.BooleanField(default = False)
    fguard_pic = models.ImageField(upload_to='families_pics', default='', blank=True, null=True) 

    def __str__(self) -> str:
        return (self.family_id.family_name + ' ' + self.fguard_name) 


class PaidGuards(models.Model):
    pguard_id = models.BigAutoField(primary_key=True)
    family_id = models.ForeignKey(
        Families, 
        on_delete=models.CASCADE, 
        related_name='pguard_family_id', 
        default=''
        ) 
    pguard_name =  models.CharField(max_length=100, blank=False, null=False, default='')
    pguard_phone = models.CharField(max_length = 25, blank=False, default='', null=False, unique=True)
    pguard_email = models.EmailField(max_length=200, unique=True, default='')
    armed = models.BooleanField(default = False)
    pguard_pic = models.ImageField(upload_to='families_pics', default='', blank=True, null=True) 

    def __str__(self) -> str:
        return (self.family_id.family_name + ' ' + self.pguard_name + str(self.pguard_id))
    

class Position(models.Model):

    position_id = models.BigAutoField(primary_key=True)
    position_name = models.CharField(max_length=100, blank=False, null=False, default='')

    def __str__(self) -> str:
        return self.position_name


class Shift(models.Model):
    shift_id = models.BigAutoField(primary_key=True)
    fguard_id = models.ManyToManyField(Fguard, related_name='shift_fguard_id')
    pguard_id = models.ManyToManyField(PaidGuards, related_name='shift_pguard_id')
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
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='Exchanges_position_id', default='')
    origin_guard_id = models.ForeignKey(Fguard, on_delete=models.CASCADE, related_name='Exchanges_origin_guard_id', default='')
    substitute_fguard_id = models.ForeignKey(Fguard, on_delete=models.CASCADE, related_name='Exchanges_substitute_guard_id', null=True, blank=True)
    substitute_Pguard_id = models.ForeignKey(PaidGuards, on_delete=models.CASCADE, related_name='Exchanges_substitute_Pguard_id', null=True, blank=True)
    exchange_type = models.CharField(max_length=8 , default='')
    shift_id = models.ForeignKey(
        Shift, 
        on_delete=models.CASCADE, 
        related_name='Exchanges_shift_id', 
        default=''
        )


