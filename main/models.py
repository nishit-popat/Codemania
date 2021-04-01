from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Contest(models.Model):
    contest_name = models.CharField(max_length=200)
    contest_date = models.DateTimeField('date published')

    def __str__(self):
        return self.contest_name


class Problem(models.Model):
    contest_reference = models.ForeignKey(Contest, on_delete=models.CASCADE)
    problem_name = models.CharField(max_length=200)
    problem_definition = models.TextField(max_length=700)
    marks = models.IntegerField(default=0)
    testfile = models.FileField(upload_to='testfile/')

    def __str__(self):
        return self.problem_name
 

class Profile(models.Model):
    user_ref = models.OneToOneField(User, on_delete=models.CASCADE)
    pr1_points = models.IntegerField(default=0)
    pr2_points = models.IntegerField(default=0)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user_ref=user)
        profile.save() 

post_save.connect(create_profile, sender=User)

'''
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    '''