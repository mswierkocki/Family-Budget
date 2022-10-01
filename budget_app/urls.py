from django.urls import path

from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from budget_app import views, views_api

router = routers.DefaultRouter()
router.register(r'budget', views_api.BudgetAPI, basename='api-budget')
router.register(r'income', views_api.IncomeAPI, basename='api-income')
router.register(r'expense', views_api.IncomeAPI, basename='api-expense')


urlpatterns = [
    path('', login_required(views.HomeView.as_view()), name="home"),

    path('budget/add/', views.BudgetCreateView.as_view(), name="budget-add"),
    path('budget/<int:pk>/',
         views.BudgetDetailView.as_view(), name="budget-detail"),
    path('budget/<int:pk>/update/',
         views.BudgetUpdateView.as_view(), name="budget-update"),
    path('budget/<int:pk>/delete/',
         views.BudgetDeleteView.as_view(), name="budget-delete"),
    path('budget/<int:budget_pk>/add_income/',
         views.IncomeAddView.as_view(), name="income-add"),
    path('budget/<int:budget_pk>/add_expense/',
         views.ExpenseAddView.as_view(), name="expense-add"),
    path('budget/<int:budget_pk>/income/<int:pk>/delete/',
         views.IncomeDeleteView.as_view(), name="income-delete"),
    path('budget/<int:budget_pk>/expense/<int:pk>/delete/',
         views.ExpenseDeleteView.as_view(), name="expense-delete"),
    path('budget/<int:budget_pk>/income/<int:pk>/',
         views.IncomeDetailView.as_view(), name="income-details"),
    path('budget/<int:budget_pk>/expense/<int:pk>/',
         views.ExpenseDetailView.as_view(), name="expense-details"),

    path('expense/category/add/', views.ExpenseCategoryAddView.as_view(),
         name="expense-category-add"),

    path('api/', include(router.urls)),

    path('api/transactions/<int:budget_pk>/',
         views_api.TransactionAPI.as_view(), name='api-transaction-list'),
    path('api/transactions/<int:budget_pk>/<str:interval>/',
         views_api.TransactionAPI.as_view(), name='api-transaction-list'),


]
