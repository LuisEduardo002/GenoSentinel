from django.urls import path

from .views import (
    GeneCreateView,
    GeneRetrieveView,
    GeneUpdateView,
    GeneDeleteView,
    GeneListView,
)

urlpatterns = [
    # Crear gen
    path('create/', GeneCreateView.as_view(), name='gene-create'),

    # Obtener, actualizar y eliminar por ID (UUID)
    path('get/<uuid:pk>/', GeneRetrieveView.as_view(), name='gene-detail'),
    path('update/<uuid:pk>/', GeneUpdateView.as_view(), name='gene-update'),
    path('delete/<uuid:pk>/', GeneDeleteView.as_view(), name='gene-delete'),

    # Listar genes (con filtro opcional ?symbol=)
    path('', GeneListView.as_view(), name='gene-list'),
]
