from rest_framework import serializers
from .models import Budget, CashFlow,Income,Expense


class CashFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlow
        fields = ['id','date','value','text']
        abstract = True
        
class IncomeSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=Income.Category.choices, source='get_category_display')
    class Meta:
        model = Income
        # fields = '__all__'
        exclude =['budget']
        
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'
class BudgetDetailSerializer(serializers.ModelSerializer):
    income = IncomeSerializer(many=True)
    class Meta:
        model = Budget
        fields = ['pk','name','owner','shared','income','expense']
    