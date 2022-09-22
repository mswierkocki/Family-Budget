#REST framework1
from rest_framework import viewsets
from rest_framework.views import APIView
#from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS,AllowAny


from .serializers import *


class BudgetAPI(viewsets.ModelViewSet):
    """
    Main Budged Api  class that provide enpoints for Budget API
    """
    permission_classes = [AllowAny]
     
    def get_queryset(self):
        return Budget.objects.all()
        return self.request.user.accounts.all()
        #return self.request.user.accounts.all()
    
    
    def get_serializer_class(self):
        # if self.action == 'create':
        #     return CreateVendingUserSerializer
        return BudgetSerializer