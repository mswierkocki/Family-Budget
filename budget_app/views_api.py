# REST framework
from rest_framework import viewsets
# from rest_framework.views import APIView
from rest_framework import filters


from rest_framework.permissions import IsAdminUser

# from .serializers import BudgetSerializer

from budget_app.filters import IsOwnerFilterBackend


class BudgetAPI(viewsets.ModelViewSet):
    """
    Budget Api
    """

    permission_classes = [IsAdminUser]
    filter_backends = [IsOwnerFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['name', 'shared']
    search_fields = ['^name', ]
