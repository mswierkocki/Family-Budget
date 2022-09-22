from rest_framework import serializers
from .models import Budget


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'
class BudgetDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['pk','name','owner','shared','income','expense']