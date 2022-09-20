from django import forms
from django.core.exceptions import ValidationError

from budget_app.models import Budget, Expense, Profile, Income

# Create the form class.


class BudgetUpdateForm(forms.ModelForm):

    class Meta:
        model = Budget
        fields = ['name', 'shared']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if 'initial' in kwargs:
        self.base_fields['shared'].queryset = Profile.objects.exclude(
            pk=self.instance.owner.pk)

    def clean(self):
        """Check if we dont share budget to ourself"""
        cleaned_data = super().clean()
        owner = self.instance.owner
        shared = cleaned_data['shared']
        if owner in shared:
            raise ValidationError("You can not share budget to Yourself!")
        return cleaned_data


class NewIncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['date', 'value', 'text', 'category']


class NewExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'value', 'text', 'category']
