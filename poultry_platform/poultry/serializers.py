from rest_framework import serializers

from . import models


class BirdSpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BirdSpecies
        fields = '__all__'


class FarmLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FarmLocation
        fields = '__all__'


class FeedTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeedType
        fields = '__all__'


class BatchSerializer(serializers.ModelSerializer):
    species_detail = BirdSpeciesSerializer(source='species', read_only=True)
    location_detail = FarmLocationSerializer(source='location', read_only=True)

    class Meta:
        model = models.Batch
        fields = (
            'id',
            'code',
            'species',
            'species_detail',
            'origin',
            'arrival_date',
            'location',
            'location_detail',
            'initial_quantity',
            'current_quantity',
            'status',
            'notes',
            'created_at',
            'updated_at',
        )


class IncubationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IncubationRecord
        fields = '__all__'


class FeedLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeedLog
        fields = '__all__'


class ProductionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductionLog
        fields = '__all__'


class MortalityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MortalityLog
        fields = '__all__'


class SaleRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SaleRecord
        fields = '__all__'


class DailyMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailyMetric
        fields = '__all__'
