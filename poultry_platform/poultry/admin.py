from django.contrib import admin

from . import models


@admin.register(models.BirdSpecies)
class BirdSpeciesAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'breed', 'created_at')
    search_fields = ('code', 'name', 'breed')


@admin.register(models.FarmLocation)
class FarmLocationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'location_type', 'capacity', 'is_active')
    list_filter = ('location_type', 'is_active')
    search_fields = ('code', 'name')


@admin.register(models.FeedType)
class FeedTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'energy_kcal', 'protein_percent')
    search_fields = ('code', 'name')


@admin.register(models.Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'species',
        'arrival_date',
        'location',
        'initial_quantity',
        'current_quantity',
        'status',
    )
    list_filter = ('status', 'species', 'location__location_type')
    search_fields = ('code', 'species__name')
    autocomplete_fields = ('species', 'location')
    readonly_fields = ('current_quantity', 'created_at', 'updated_at')


@admin.register(models.IncubationRecord)
class IncubationRecordAdmin(admin.ModelAdmin):
    list_display = (
        'batch',
        'incubator_section',
        'egg_category',
        'eggs_set',
        'set_date',
        'hatched_chicks',
    )
    list_filter = ('egg_category', 'set_date')
    search_fields = ('batch__code', 'incubator_section')
    autocomplete_fields = ('batch',)


@admin.register(models.FeedLog)
class FeedLogAdmin(admin.ModelAdmin):
    list_display = ('batch', 'record_date', 'feed_type', 'quantity_kg', 'location')
    list_filter = ('feed_type', 'location__location_type', 'record_date')
    search_fields = ('batch__code',)
    autocomplete_fields = ('batch', 'location', 'feed_type', 'recorded_by')
    date_hierarchy = 'record_date'


@admin.register(models.ProductionLog)
class ProductionLogAdmin(admin.ModelAdmin):
    list_display = ('batch', 'record_date', 'eggs_total', 'category', 'storage_location')
    list_filter = ('category', 'storage_location__location_type')
    search_fields = ('batch__code',)
    autocomplete_fields = ('batch', 'storage_location')
    date_hierarchy = 'record_date'


@admin.register(models.MortalityLog)
class MortalityLogAdmin(admin.ModelAdmin):
    list_display = ('batch', 'record_date', 'count', 'mortality_type')
    list_filter = ('mortality_type', 'record_date')
    search_fields = ('batch__code',)
    autocomplete_fields = ('batch', 'recorded_by')
    date_hierarchy = 'record_date'


@admin.register(models.SaleRecord)
class SaleRecordAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name',
        'record_date',
        'item_type',
        'quantity',
        'unit_price',
        'batch',
    )
    list_filter = ('item_type', 'record_date')
    search_fields = ('customer_name', 'document_number', 'batch__code')
    autocomplete_fields = ('batch',)
    date_hierarchy = 'record_date'


@admin.register(models.DailyMetric)
class DailyMetricAdmin(admin.ModelAdmin):
    list_display = ('batch', 'date', 'feed_used_kg', 'eggs_collected', 'mortality_count', 'live_weight_kg')
    list_filter = ('date',)
    search_fields = ('batch__code',)
    autocomplete_fields = ('batch',)
    date_hierarchy = 'date'
