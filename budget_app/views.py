# Django Related
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


from budget_app.models import Budget


class ProfileRequiredMixin(LoginRequiredMixin):
    """Verify that the current user has profile."""

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'profile'):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
# Create your views here.


class HomeView(ProfileRequiredMixin, ListView):
    model = Budget

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        shared_budgets = Budget.objects.filter(
            shared=self.request.user.profile)
        context['shared_budgets'] = shared_budgets
        return context

    def get_queryset(self):
        return Budget.objects.filter(owner=self.request.user.profile)
