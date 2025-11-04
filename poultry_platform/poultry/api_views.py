from rest_framework import permissions, viewsets

from . import models, serializers


class BaseProtectedViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)


class BirdSpeciesViewSet(BaseProtectedViewSet):
    queryset = models.BirdSpecies.objects.all()
    serializer_class = serializers.BirdSpeciesSerializer


class FarmLocationViewSet(BaseProtectedViewSet):
    queryset = models.FarmLocation.objects.all()
    serializer_class = serializers.FarmLocationSerializer


class FeedTypeViewSet(BaseProtectedViewSet):
    queryset = models.FeedType.objects.all()
    serializer_class = serializers.FeedTypeSerializer


class BatchViewSet(BaseProtectedViewSet):
    queryset = models.Batch.objects.select_related('species', 'location').all()
    serializer_class = serializers.BatchSerializer


class IncubationRecordViewSet(BaseProtectedViewSet):
    queryset = models.IncubationRecord.objects.select_related('batch').all()
    serializer_class = serializers.IncubationRecordSerializer


class FeedLogViewSet(BaseProtectedViewSet):
    queryset = (
        models.FeedLog.objects.select_related('batch', 'location', 'feed_type', 'recorded_by')
        .all()
        .order_by('-record_date')
    )
    serializer_class = serializers.FeedLogSerializer


class ProductionLogViewSet(BaseProtectedViewSet):
    queryset = models.ProductionLog.objects.select_related('batch', 'storage_location').all()
    serializer_class = serializers.ProductionLogSerializer


class MortalityLogViewSet(BaseProtectedViewSet):
    queryset = models.MortalityLog.objects.select_related('batch', 'recorded_by').all()
    serializer_class = serializers.MortalityLogSerializer


class SaleRecordViewSet(BaseProtectedViewSet):
    queryset = models.SaleRecord.objects.select_related('batch').all()
    serializer_class = serializers.SaleRecordSerializer


class DailyMetricViewSet(BaseProtectedViewSet):
    queryset = models.DailyMetric.objects.select_related('batch').all()
    serializer_class = serializers.DailyMetricSerializer
