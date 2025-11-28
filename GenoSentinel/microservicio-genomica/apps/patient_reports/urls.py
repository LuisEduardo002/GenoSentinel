from django.urls import path

from .views import (
    PatientVariantReportCreateView,
    PatientVariantReportRetrieveView,
    PatientVariantReportUpdateView,
    PatientVariantReportDeleteView,
    PatientVariantReportListView,
    PatientReportSummaryView,
)

urlpatterns = [
    # Crear reporte
    path('create/', PatientVariantReportCreateView.as_view(), name='patient-report-create'),

    # Obtener, actualizar y eliminar por ID (UUID)
    path('get/<uuid:pk>/', PatientVariantReportRetrieveView.as_view(), name='patient-report-detail'),
    path('update/<uuid:pk>/', PatientVariantReportUpdateView.as_view(), name='patient-report-update'),
    path('delete/<uuid:pk>/', PatientVariantReportDeleteView.as_view(), name='patient-report-delete'),

    # Listar reportes (con filtros opcionales ?patient_id=, ?variant_id=)
    path('', PatientVariantReportListView.as_view(), name='patient-report-list'),

    # Resumen clínico + genómico para un paciente (patient_id es UUID)
    path('summary/<uuid:patient_id>/', PatientReportSummaryView.as_view(), name='patient-report-summary'),
]
