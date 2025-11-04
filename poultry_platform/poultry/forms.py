from django import forms

from . import models


class DateInput(forms.DateInput):
    input_type = 'date'


class BatchForm(forms.ModelForm):
    class Meta:
        model = models.Batch
        fields = (
            'code',
            'species',
            'origin',
            'arrival_date',
            'location',
            'initial_quantity',
            'status',
            'notes',
        )
        widgets = {
            'arrival_date': DateInput(),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class FeedLogForm(forms.ModelForm):
    class Meta:
        model = models.FeedLog
        fields = (
            'batch',
            'location',
            'feed_type',
            'record_date',
            'quantity_kg',
            'note',
        )
        widgets = {
            'record_date': DateInput(),
            'note': forms.Textarea(attrs={'rows': 2}),
        }


class ProductionLogForm(forms.ModelForm):
    class Meta:
        model = models.ProductionLog
        fields = (
            'batch',
            'record_date',
            'eggs_total',
            'category',
            'storage_location',
            'note',
        )
        widgets = {
            'record_date': DateInput(),
            'note': forms.Textarea(attrs={'rows': 2}),
        }


class MortalityLogForm(forms.ModelForm):
    class Meta:
        model = models.MortalityLog
        fields = (
            'batch',
            'record_date',
            'count',
            'mortality_type',
            'reason',
            'note',
        )
        widgets = {
            'record_date': DateInput(),
            'note': forms.Textarea(attrs={'rows': 2}),
        }


class SaleRecordForm(forms.ModelForm):
    class Meta:
        model = models.SaleRecord
        fields = (
            'batch',
            'record_date',
            'item_type',
            'quantity',
            'unit',
            'unit_price',
            'customer_name',
            'document_number',
            'note',
        )
        widgets = {
            'record_date': DateInput(),
            'note': forms.Textarea(attrs={'rows': 2}),
        }


class IncubationRecordForm(forms.ModelForm):
    class Meta:
        model = models.IncubationRecord
        fields = (
            'batch',
            'incubator_section',
            'egg_category',
            'eggs_set',
            'set_date',
            'expected_hatch_date',
            'hatched_chicks',
            'hatch_date',
            'notes',
        )
        widgets = {
            'set_date': DateInput(),
            'expected_hatch_date': DateInput(),
            'hatch_date': DateInput(),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
