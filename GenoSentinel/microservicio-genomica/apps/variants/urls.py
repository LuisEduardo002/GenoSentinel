from django.urls import path

from .views import (
    GeneticVariantCreateView,
    GeneticVariantRetrieveView,
    GeneticVariantUpdateView,
    GeneticVariantDeleteView,
    GeneticVariantListView,
)

urlpatterns = [
    # Crear variante
    path('create/', GeneticVariantCreateView.as_view(), name='variant-create'),

    # Obtener, actualizar y eliminar por ID (UUID)
    path('get/<uuid:pk>/', GeneticVariantRetrieveView.as_view(), name='variant-detail'),
    path('update/<uuid:pk>/', GeneticVariantUpdateView.as_view(), name='variant-update'),
    path('delete/<uuid:pk>/', GeneticVariantDeleteView.as_view(), name='variant-delete'),

    # Listar variantes (con filtros opcionales ?gene_id=, ?chromosome=, ?impact=)
    path('', GeneticVariantListView.as_view(), name='variant-list'),
]
