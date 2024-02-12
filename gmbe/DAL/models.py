from django.db import models
from django.contrib.auth.models import User



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

    
    def __str__(self) -> str:
        return self.family_name
    


class Stance(models.Model):

    SHIFT_CHOICES = (
        (1, 'שעה אחת'),
        (2, 'שעתיים' ),
        (3, '3 שעות'),
        (4, 'שעות 4' ),
        (5, 'שעות 6' ),
        (6, 'שעות 8' ),
        (7, 'שעות 12' ),
        (8, 'שעות 24' ),
    )

    GUARD_CHOICES = [(i, str(i)) for i in range(1, 13)]

    stance_id = models.BigAutoField(primary_key=True)
    stance_name = models.CharField(max_length=100, blank=False, null=False, default='', unique=True)
    shift_hours =  models.IntegerField(choices = SHIFT_CHOICES)
    how_many_guards = models.IntegerField(choices = GUARD_CHOICES)

    def __str__(self) -> str:
        return self.stance_name
    
class GuardingList(models.Model):

    guard_list_id = models.BigAutoField(primary_key=True)
    date = models.CharField(max_length=20, blank=False, null=False, default='')
    day = models.CharField(max_length=10, blank=False, null=False, default='')
    time = models.CharField(max_length=10, blank=False, null=False, default='')
    stance_id = models.ForeignKey(Stance, on_delete=models.CASCADE, related_name='stance_id_guarding_lists')
    stance_name = models.ForeignKey(Stance, on_delete=models.CASCADE, related_name='stance_name_guarding_lists')
    id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_id_guarding_lists')
    family_id = models.ForeignKey(Families, on_delete=models.CASCADE, related_name='family_id_guarding_lists')
    family_name = models.ForeignKey(Families, on_delete=models.CASCADE, related_name='family_name_guarding_lists')
    family_pic = models.ForeignKey(Families, on_delete=models.CASCADE, related_name='family_pic_guarding_lists')
    name1 = models.ForeignKey(Families, on_delete=models.CASCADE, related_name='name1_guarding_lists')
    phone1 = models.ForeignKey(Families, on_delete=models.CASCADE, related_name='phone1_guarding_lists')
    armed1 = models.ForeignKey(Families, on_delete=models.CASCADE, related_name='armed1_guarding_lists')
    name2 = models.ForeignKey(Families, on_delete=models.CASCADE, related_name='name2_guarding_lists')
    phone2 = models.ForeignKey(Families, on_delete=models.CASCADE, related_name='phone2_guarding_lists')
    armed2 = models.ForeignKey(Families, on_delete=models.CASCADE, related_name='armed2_guarding_lists')
    
    def __str__(self) -> str:
        return self.date+self.day