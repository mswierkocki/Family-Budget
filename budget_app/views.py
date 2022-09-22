import itertools
from decimal import Decimal

# Django Related
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.db.models import Sum

from django.conf import settings

# app related
from .forms import BudgetUpdateForm, NewIncomeForm, NewExpenseForm
from .models import Budget, Income, Expense, ExpenseCategory

# Constants
BUDGET_PAGINATION_BY = getattr(settings, "BUDGET_PAGINATION_BY", 10)
BUDGET_DETAILS_PAGINATION_BY = getattr(
    settings, "BUDGET_DETAILS_PAGINATION_BY", 10)
TWOPLACES = Decimal(10) ** -2
# Mixins


class ProfileRequiredMixin(LoginRequiredMixin):
    """Verify that the current user has profile."""

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'profile'):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class OwnerRequiredMixin(ProfileRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().owner != self.request.user.profile:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class BudgetOwnerRequiredMixin(LoginRequiredMixin):
    """Verify that the current user is owner of budget."""

    def dispatch(self, request, *args, **kwargs):
        if 'budget_pk' not in self.kwargs:
            return HttpResponseForbidden()
        budget = Budget.objects.get(pk=self.kwargs['budget_pk'])
        if budget.owner != self.request.user.profile:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


TWOPLACES = Decimal(10) ** -2
# Create your views here.


class HomeView(ProfileRequiredMixin, ListView):
    model = Budget
    paginate_by = 5  # BUDGET_PAGINATION_BY

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        shared_budgets = Budget.objects.filter(
            shared=self.request.user.profile)

        shared_paginator = Paginator(shared_budgets, self.paginate_by)
        shared_budgets_page = shared_paginator.get_page(
            self.request.GET.get('shared_page'))

        context['shared_budgets_list'] = shared_budgets_page
        context['shared_paginator'] = shared_paginator

        context['is_shared_paginated'] = shared_paginator.num_pages > 1
        return context

    def get_queryset(self):
        return Budget.objects.filter(owner=self.request.user.profile)


class BudgetCreateView(ProfileRequiredMixin, CreateView):
    model = Budget
    fields = ['name']

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)


class BudgetDetailView(ProfileRequiredMixin, DetailView):
    model = Budget
    paginate_by = 2

    def get_queryset(self):
        return super().get_queryset()

    def dispatch(self, request, *args, **kwargs):
        request_user = self.request.user.profile
        object = self.get_object()
        if not request_user == object.owner:
            if request_user not in object.shared.all():
                return HttpResponseForbidden()
        return super(BudgetDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BudgetDetailView, self).get_context_data(**kwargs)
        incomes = self.object.income.all()
        expenses = self.object.expense.all()
        # TODO add Pagination
        total_income = incomes.aggregate(Sum('value'))
        total_expenses = expenses.aggregate(Sum('value'))
        combined_list = itertools.zip_longest(incomes, expenses)
        context['combined'] = list(combined_list)
        context['total_income'] = Decimal(
            total_income['value__sum'] or '0').quantize(TWOPLACES)
        context['total_expenses'] = Decimal(
            total_expenses['value__sum'] or '0').quantize(TWOPLACES)
        context['is_owner'] = self.object.owner == self.request.user.profile

        return context


class BudgetUpdateView(OwnerRequiredMixin, UpdateView):
    model = Budget
    template_name_suffix = '_form_update'
    form_class = BudgetUpdateForm


class BudgetDeleteView(OwnerRequiredMixin, DeleteView):
    model = Budget
    success_url = reverse_lazy('budget-list')


class ExpenseCategoryAddView(CreateView, ProfileRequiredMixin):
    model = ExpenseCategory
    fields = ['name']
    template_name = 'budget_app/default_form.html'
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Add new Expense category"
        context['heading'] = context['title']
        return context


class CashFlowAddView(BudgetOwnerRequiredMixin, CreateView):
    template_name = 'budget_app/default_form.html'

    def get_success_url(self) -> str:
        budget_id = self.kwargs['budget_pk']
        return reverse_lazy('budget-detail', kwargs={'pk': budget_id},)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""

        form.instance.budget = Budget.objects.get(pk=self.kwargs['budget_pk'])
        return super().form_valid(form)


class ExpenseAddView(CashFlowAddView):
    model = Expense
    form_class = NewExpenseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Add new Expense"
        context['heading'] = context['title']
        # TODO: Maby use htmlx for that ? ofc we could move this to specialized template(like expense_form)
        # instead of using this 'hack'
        context['additional'] = mark_safe("<h6><a href={}>{}</a></h6>".format(
            reverse_lazy('expense-category-add'), "Did u know u can add new category here ?"))

        return context


class IncomeAddView(CashFlowAddView):
    model = Income
    form_class = NewIncomeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Add new Income"
        context['heading'] = context['title']
        return context


class CashFlowDetailView(BudgetOwnerRequiredMixin, UpdateView):
    fields = ["category", "value", 'date', 'text']

    def get_success_url(self) -> str:
        budget_id = self.kwargs['budget_pk']
        return reverse_lazy('budget-detail', kwargs={'pk': budget_id},)


class IncomeDetailView(CashFlowDetailView):
    model = Income


class ExpenseDetailView(CashFlowDetailView):
    model = Expense
