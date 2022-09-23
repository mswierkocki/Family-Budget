# REST framework
import re
from urllib import request
from rest_framework import viewsets
# from rest_framework.views import APIView
from rest_framework import filters


from rest_framework.permissions import BasePermission, IsAdminUser

from .serializers import BudgetSerializer,BudgetDetailSerializer, IncomeSerializer

from budget_app.models import Budget
from budget_app.filters import IsOwnerFilterBackend


class ProfileRequiredPermisson(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'profile')

from rest_framework.decorators import action
from rest_framework.response import Response
class BudgetAPI(viewsets.ModelViewSet):
    """
    Budget Api
    """

    permission_classes = [ProfileRequiredPermisson, IsAdminUser]
    filter_backends = [IsOwnerFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['name', 'shared']
    search_fields = ['^name', ]

    def get_queryset(self):
        return Budget.objects.filter(owner=self.request.user.profile)

    def get_serializer_class(self):
        if self.action == 'list' and self.detail:
            print("GOT: if self.action == 'list' and self.detail:")
        if self.action == 'retrieve':
            return BudgetDetailSerializer

        return BudgetSerializer
    def paginate_queryset(self, queryset, view=None):
        if 'no_page' in self.request.query_params:
            return None
        else:
            return self.paginator.paginate_queryset(queryset, self.request, view=self)
    @action(detail=True,url_name="list-income")
    def income(self,request=None,pk=None,*args,**kwargs):
        budget=self.get_object()
        
        serializer = IncomeSerializer(budget.income.all(),many=True)
        return Response(serializer.data)
    
    @action(detail=True,url_name="list-transaction")
    def transaction(self,request=None,pk=None,*args,**kwargs):
        budget=self.get_object()
        # budget.income.all()
        # shared_paginator = Paginator(shared_budgets, self.paginate_by)
        # shared_budgets_page = shared_paginator.get_page(
        #     self.request.GET.get('shared_page'))
        serializer = IncomeSerializer(budget.income.all(),many=True)
        return Response(serializer.data)
class IncomeAPI(viewsets.ModelViewSet):
    """
    Income Api
    """

    permission_classes = [ProfileRequiredPermisson, IsAdminUser]
    filter_backends = [IsOwnerFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['name', 'shared']
    search_fields = ['^name', ]

    def get_queryset(self):
        return Budget.objects.filter(owner=self.request.user.profile)

    def get_serializer_class(self):
        if self.action == 'list' and self.detail:
            print("GOT: if self.action == 'list' and self.detail:")
        if self.action == 'retrieve':
            return BudgetDetailSerializer

        return BudgetSerializer