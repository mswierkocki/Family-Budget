# REST framework
from urllib import request
from rest_framework import viewsets
# from rest_framework.views import APIView
from rest_framework import filters


from rest_framework.permissions import BasePermission, IsAdminUser

from .serializers import BudgetSerializer,BudgetDetailSerializer

from budget_app.models import Budget
from budget_app.filters import IsOwnerFilterBackend


class ProfileRequiredPermisson(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'profile')


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
