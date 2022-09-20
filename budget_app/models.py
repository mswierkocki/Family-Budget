from django.db import models
# Create your models here.

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(models.Model):
    """
    A class used to represent User
    Related to :model: `auth.User` and :model:`budget_app.Budget`
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Profile'

    def __str__(self):
        return "{}'s profile".format(self.user.username.capitalize())



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
