from django.db import models
from datetime import datetime, date

from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save

import pytz
from django.core.urlresolvers import reverse

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='student')
    dob = models.DateField(null=True)
    regno = models.CharField(max_length=20)

    def __str__(self):
        return "%s %s"%(self.user.first_name, self.user.last_name)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Student.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.student.save()

class Meal(models.Model):
    meal = models.CharField(max_length=20)
    def __str__(self):
        return "%s" %(self.meal)

class Reviews(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=timezone.now)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    review = models.TextField()
    pub_date = models.DateField(default=date.today)
    sentiment = models.CharField(max_length=10,blank=True, null=True, default= 0)
    rating = models.IntegerField(blank=True, null=True, default=0)
    score = models.FloatField(blank=True, null=True, default=0)

    def __str__(self):
        return "Review of " + str(self.student.user.first_name) + " = " + str(self.review) + " on " + str(self.pub_date) + ", " + (self.meal.meal)

    class Meta:
        verbose_name= 'Review'
        verbose_name_plural = 'Reviews'


