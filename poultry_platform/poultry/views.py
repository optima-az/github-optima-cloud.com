from django.shortcuts import render

from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import generic

from . import forms, models


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'poultry/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_batches = models.Batch.objects.select_related('species', 'location').filter(
            status=models.Batch.BatchStatus.ACTIVE
        )
        today = timezone.now().date()
        last_7_days = today - timedelta(days=7)

        feed_stats = models.FeedLog.objects.filter(record_date__gte=last_7_days).aggregate(
            total_feed=Sum('quantity_kg')
        )
        egg_stats = models.ProductionLog.objects.filter(record_date__gte=last_7_days).aggregate(
            total_eggs=Sum('eggs_total')
        )
        mortality_stats = models.MortalityLog.objects.filter(record_date__gte=last_7_days).aggregate(
            total_mortality=Sum('count')
        )

        context.update(
            {
                'active_batches': active_batches,
                'feed_last_7_days': feed_stats.get('total_feed') or 0,
                'eggs_last_7_days': egg_stats.get('total_eggs') or 0,
                'mortality_last_7_days': mortality_stats.get('total_mortality') or 0,
                'top_batches': active_batches.annotate(
                    eggs_7_days=Sum(
                        'production_logs__eggs_total',
                        filter=Q(production_logs__record_date__gte=last_7_days),
                    ),
                    mortality_7_days=Sum(
                        'mortality_logs__count',
                        filter=Q(mortality_logs__record_date__gte=last_7_days),
                    ),
                ).order_by('-eggs_7_days')[:5],
                'recent_feed_logs': models.FeedLog.objects.select_related('batch', 'feed_type')
                .order_by('-record_date')[:5],
                'recent_production_logs': models.ProductionLog.objects.select_related('batch')
                .order_by('-record_date')[:5],
                'recent_mortality_logs': models.MortalityLog.objects.select_related('batch')
                .order_by('-record_date')[:5],
            }
        )
        return context


class BatchListView(LoginRequiredMixin, generic.ListView):
    model = models.Batch
    template_name = 'poultry/batch_list.html'
    context_object_name = 'batches'
    paginate_by = 20

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related('species', 'location')
            .order_by('-arrival_date')
        )


class BatchCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.BatchForm
    template_name = 'poultry/form_base.html'
    success_url = reverse_lazy('poultry:batch-list')
    success_message = _('Quş partiyası uğurla yaradıldı.')

    def form_valid(self, form):
        form.instance.current_quantity = form.cleaned_data['initial_quantity']
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = _('Yeni partiya')
        return context


class FeedLogCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.FeedLogForm
    template_name = 'poultry/form_base.html'
    success_url = reverse_lazy('poultry:dashboard')
    success_message = _('Yemləmə qeydi əlavə olundu.')

    def form_valid(self, form):
        form.instance.recorded_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = _('Yemləmə qeydi')
        return context


class ProductionLogCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.ProductionLogForm
    template_name = 'poultry/form_base.html'
    success_url = reverse_lazy('poultry:dashboard')
    success_message = _('İstehsal qeydi əlavə olundu.')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = _('İstehsal qeydi')
        return context


class MortalityLogCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.MortalityLogForm
    template_name = 'poultry/form_base.html'
    success_url = reverse_lazy('poultry:dashboard')
    success_message = _('Tələfat qeydi əlavə olundu.')

    def form_valid(self, form):
        form.instance.recorded_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        batch = form.instance.batch
        batch.current_quantity = max(0, batch.current_quantity - form.instance.count)
        batch.save(update_fields=['current_quantity', 'updated_at'])
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = _('Tələfat qeydi')
        return context


class SaleRecordCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.SaleRecordForm
    template_name = 'poultry/form_base.html'
    success_url = reverse_lazy('poultry:dashboard')
    success_message = _('Satış qeydi əlavə olundu.')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        if form.instance.item_type == form.instance.ItemType.BIRD and form.instance.batch:
            batch = form.instance.batch
            birds_sold = int(form.instance.quantity)
            batch.current_quantity = max(0, batch.current_quantity - birds_sold)
            batch.save(update_fields=['current_quantity', 'updated_at'])
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = _('Satış qeydi')
        return context


class IncubationRecordCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.IncubationRecordForm
    template_name = 'poultry/form_base.html'
    success_url = reverse_lazy('poultry:dashboard')
    success_message = _('İnkubasiya qeydi əlavə olundu.')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = _('İnkubasiya qeydi')
        return context
