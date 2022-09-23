import math
from decimal import Decimal

from django.db import models
# Create your models here.

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.urls import reverse

# This is the lowest nominal that can be set in cash flows, could be also 0.05 or 1.0
MINIMAL_VALUE_NOMINAL = Decimal(
    getattr(settings, "BUDGET_MINIMAL_VALUE_NOMINAL_STR", '0.01'))
MAXIMAL_CASHFLOW_VALUE = Decimal(
    getattr(settings, "BUDGET_MAXIMAL_CASHFLOW_VALUE_STR", '1000000'))
CURRENCY_SIGN = getattr(settings, "BUDGET_CURRENCY_SIGN", "$")


def validate_min_cashflow(value):
    if value < MINIMAL_VALUE_NOMINAL:
        raise ValidationError(
            '%(value)s is lower than %(min_nom)s!',
            params={'value': value, 'min_nom': str(MINIMAL_VALUE_NOMINAL)},
        )


def validate_max_cashflow(value):
    if value > MAXIMAL_CASHFLOW_VALUE:
        raise ValidationError(
            '%(value)s is higher than %(min_nom)s!',
            params={'value': value, 'min_nom': str(MAXIMAL_CASHFLOW_VALUE)},
        )


def get_sentinel_expense_category():
    return ExpenseCategory.objects.get_or_create(name='uncategorised')[0]


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
        ordering = ['-id']

    def __str__(self):
        return "{}'s '{}' budget.".format(self.owner.user.username, self.name)

    def get_absolute_url(self):
        return reverse('budget-detail', kwargs={'pk': self.pk})

    def is_owner(self, user_profile):
        return self.owner == user_profile

    def is_sharing(self):
        return self.shared.count() > 0


class CashFlow(models.Model):
    """
    Abstract class contains common fields for cash flow

    Fields
    ----------
    date : datetime
        the date of cashflow operation
    value : :model:`Decimal`
        the amount of the operation
    text='' : str
        the Optional text that is added to operation
    budget : :model:`budget_app.Budget`
        the related budget

    """

    date = models.DateTimeField(default=timezone.now)
    value = models.DecimalField(max_digits=math.ceil(math.log10(MAXIMAL_CASHFLOW_VALUE))+3,
                                decimal_places=2, default=0.0, validators=[validate_min_cashflow, validate_max_cashflow])
    budget = models.ForeignKey(
        Budget, related_name="%(class)s", on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True, max_length=255)

    class Meta:
        abstract = True
        ordering = ["date"]


class Income(CashFlow):
    """
    A representation of income cashflow operation, based on abstract :model:`budget_app.CashFlow`

    Fields
    ----------
    category : str
       an appropriate two-character category representation based on :model:`budget_app.Income.Category` choices
    """
    class Category(models.TextChoices):
        SALARY = 'w', 'Salary'
        BONUS = 'b', 'Bonus'
        SCHOLARSHIP = 's', 'Scholarship'
        PENSION = 'p', 'Pension'
        FAMILY_BENEFITS = 'fb', 'Family Benefits'
        FRANCHISE = 'f', 'Franchise'
        INTEREST = 'i', 'Interest'
        AFFILIATE_PROGRAMS = 'ap', 'Affiliate Programs'
        INVESTMENT = 'iv', 'Investment'
        DIVIDEND = 'd', 'Dividend'
        LEASE = 'l', 'Lease'
        STOCK_MARKET = 'sm', 'Stock Market'
        FUNDS = 'fn', 'Funds'
        DEPOSITS = 'de', 'Deposits'
        POCKET_MONEY = 'pm', 'Pocket Money'
        OTHER = 'o', 'Other'

    category = models.CharField(
        max_length=2,
        choices=Category.choices,
        default=Category.OTHER
    )

    class Meta(CashFlow.Meta):
        ordering = ["-value"]

    def __str__(self) -> str:
        return "{}{} from {}".format(self.value, CURRENCY_SIGN, Income.Category(self.category).label)


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Expense categories"
        ordering = ['pk']

    def __str__(self) -> str:
        return "{}".format(self.name)


class Expense(CashFlow):
    category = models.ForeignKey(
        ExpenseCategory, on_delete=models.SET(get_sentinel_expense_category))

    def __str__(self) -> str:
        return "{}{} on {}".format(self.value, CURRENCY_SIGN, self.category.name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
