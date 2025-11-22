from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GeneticVariantViewSet

router = DefaultRouter()
router.register(r'', GeneticVariantViewSet, basename='genetic-variant')

urlpatterns = router.urls