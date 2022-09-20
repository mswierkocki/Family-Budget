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


class Budget(models.Model):
    """
    A class used to represent a Budget

    Fields
    ----------
    name : str
        the name of the budget
    owner : :model:`budget_app.Profile`
        the owner of the budget
    shared : list of :model:`budget_app.Profile`'s
        to whom Budget is shared

    Methods
    -------
    is_owner(user_profile: :model:`budget_app.Profile`)
        returns whether the requested user is budget owner
    """

    name = models.CharField(max_length=50, null=False, blank=False)
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="owning_budgets")
    shared = models.ManyToManyField(
        Profile, related_name="sharing", blank=True)

    class Meta:
        verbose_name = 'Budget'

    def __str__(self):
        return "{}'s '{}' budget.".format(self.owner.user.username, self.name)

    def is_owner(self, user_profile):
        return self.owner == user_profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
