from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GeneViewSet

router = DefaultRouter()
router.register(r'', GeneViewSet, basename='gene')

urlpatterns = router.urls