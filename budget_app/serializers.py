from rest_framework import serializers

from budget_app.models import Budget, CashFlow, Income, Expense, MAX_DIGIT_CASHFLOW


class CashFlowSerializer(serializers.Serializer):
    pk = serializers.ReadOnlyField()
    date = serializers.DateTimeField()
    value = serializers.DecimalField(
        max_digits=MAX_DIGIT_CASHFLOW, decimal_places=2)
    text = serializers.CharField()

    class Meta:
        model = CashFlow
        fields = ['id', 'date', 'value', 'text']
        abstract = True

# class CashFlowAbstractSerializer(serializers.ModelSerializer):
#     pk = serializers.ReadOnlyField()
#     class Meta:
#         model = CashFlow
#         fields = ['id','date','value','text']
#         abstract = True


class IncomeSerializer(serializers.ModelSerializer):
    # lookup_url_kwarg=['budget']
    url = serializers.HyperlinkedRelatedField(
        view_name='api-income-detail', read_only=True, lookup_field='pk')
    category = serializers.ChoiceField(
        choices=Income.Category.choices, source='get_category_display')

    class Meta:
        model = Income
        # fields = '__all__'
        fields = ('text', 'value', 'url', 'category')
        #exclude =['budget']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'


class BudgetSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        view_name='budget-api-detail', read_only=True)

    class Meta:
        model = Budget
        #fields = '__all__'
        fields = ['url', 'pk', 'name', 'owner', 'shared', 'income', 'expense']


class BudgetDetailSerializer(serializers.ModelSerializer):
    income = IncomeSerializer(many=True)

    class Meta:
        model = Budget
        fields = ['pk', 'name', 'owner', 'shared', 'income', 'expense']
