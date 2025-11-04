from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api_views, views

app_name = 'poultry'

router = DefaultRouter()
router.register(r'species', api_views.BirdSpeciesViewSet, basename='species')
router.register(r'locations', api_views.FarmLocationViewSet, basename='locations')
router.register(r'feed-types', api_views.FeedTypeViewSet, basename='feed-types')
router.register(r'batches', api_views.BatchViewSet, basename='batches')
router.register(r'incubations', api_views.IncubationRecordViewSet, basename='incubations')
router.register(r'feed-logs', api_views.FeedLogViewSet, basename='feed-logs')
router.register(r'production-logs', api_views.ProductionLogViewSet, basename='production-logs')
router.register(r'mortality-logs', api_views.MortalityLogViewSet, basename='mortality-logs')
router.register(r'sales', api_views.SaleRecordViewSet, basename='sales')
router.register(r'daily-metrics', api_views.DailyMetricViewSet, basename='daily-metrics')


urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('batches/', views.BatchListView.as_view(), name='batch-list'),
    path('batches/new/', views.BatchCreateView.as_view(), name='batch-create'),
    path('incubations/new/', views.IncubationRecordCreateView.as_view(), name='incubation-create'),
    path('feed/new/', views.FeedLogCreateView.as_view(), name='feed-log-create'),
    path('production/new/', views.ProductionLogCreateView.as_view(), name='production-log-create'),
    path('mortality/new/', views.MortalityLogCreateView.as_view(), name='mortality-log-create'),
    path('sales/new/', views.SaleRecordCreateView.as_view(), name='sale-record-create'),
    path('api/', include(router.urls)),
]
