from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientVariantReportViewSet

router = DefaultRouter()
router.register(r'', PatientVariantReportViewSet, basename='patient-report')

urlpatterns = router.urls