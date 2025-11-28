from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from django.conf import settings
import requests

from .models import PatientVariantReport
from .serializers import PatientVariantReportSerializer


class PatientVariantReportCreateView(APIView):
    """Crear un nuevo reporte de variante para un paciente"""

    @extend_schema(
        request=PatientVariantReportSerializer,
        responses={
            201: PatientVariantReportSerializer,
            400: {"description": "Datos inválidos"},
        },
        summary="Crear un nuevo reporte de variante para un paciente",
        tags=["patient-reports"],
    )
    def post(self, request):
        serializer = PatientVariantReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def _get_report_or_404(pk):
    try:
        return PatientVariantReport.objects.get(pk=pk)
    except PatientVariantReport.DoesNotExist:
        return None


class PatientVariantReportRetrieveView(APIView):
    """Obtener un reporte de variante por ID"""

    @extend_schema(
        responses={
            200: PatientVariantReportSerializer,
            404: {"description": "Reporte no encontrado"},
        },
        summary="Obtener un reporte de variante por ID",
        tags=["patient-reports"],
    )
    def get(self, request, pk):
        report = _get_report_or_404(pk)
        if report is None:
            return Response({"detail": "Report not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PatientVariantReportSerializer(report)
        return Response(serializer.data)


class PatientVariantReportUpdateView(APIView):
    """Actualizar un reporte de variante por ID"""

    @extend_schema(
        request=PatientVariantReportSerializer,
        responses={
            200: PatientVariantReportSerializer,
            400: {"description": "Datos inválidos"},
            404: {"description": "Reporte no encontrado"},
        },
        summary="Actualizar un reporte de variante por ID",
        tags=["patient-reports"],
    )
    def patch(self, request, pk):
        report = _get_report_or_404(pk)
        if report is None:
            return Response({"detail": "Report not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PatientVariantReportSerializer(report, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientVariantReportDeleteView(APIView):
    """Eliminar un reporte de variante por ID"""

    @extend_schema(
        responses={
            204: None,
            404: {"description": "Reporte no encontrado"},
        },
        summary="Eliminar un reporte de variante por ID",
        tags=["patient-reports"],
    )
    def delete(self, request, pk):
        report = _get_report_or_404(pk)
        if report is None:
            return Response({"detail": "Report not found"}, status=status.HTTP_404_NOT_FOUND)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PatientVariantReportListView(APIView):
    """Listar reportes de variantes de pacientes, con filtros opcionales"""

    @extend_schema(
        responses={200: PatientVariantReportSerializer(many=True)},
        summary="Listar reportes de variantes de pacientes",
        tags=["patient-reports"],
    )
    def get(self, request):
        patient_id = request.query_params.get("patient_id")
        variant_id = request.query_params.get("variant_id")

        queryset = PatientVariantReport.objects.all()
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        if variant_id:
            queryset = queryset.filter(variant_id=variant_id)

        serializer = PatientVariantReportSerializer(queryset, many=True)
        return Response(serializer.data)


class PatientReportSummaryView(APIView):
    """Obtener un resumen combinado clínico + genómico para un paciente"""

    @extend_schema(
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'patientId': {'type': 'integer'},
                    'clinicalRecords': {},
                    'genomicReports': PatientVariantReportSerializer(many=True),
                },
            },
            404: {"description": "No existen reportes para este paciente"},
            502: {"description": "Error al comunicarse con el microservicio de Clínica"},
        },
        summary="Obtener resumen clínico + genómico de un paciente",
        tags=["patient-reports"],
    )
    def get(self, request, patient_id):
        # Reportes genómicos locales para el paciente
        reports = PatientVariantReport.objects.filter(patient_id=patient_id)
        if not reports.exists():
            return Response(
                {"detail": "No existen reportes para este paciente"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Llamar al microservicio de Clínica dentro del clúster / entorno
        base_url = getattr(settings, 'CLINICA_BASE_URL', 'http://localhost:3001')

        # Historias clínicas del paciente
        clinical_url = f"{base_url}/clinical-records?patientId={patient_id}"
        try:
            clinical_response = requests.get(clinical_url, timeout=5)
            clinical_response.raise_for_status()
            clinical_data = clinical_response.json()
        except Exception:
            return Response(
                {"detail": "Error al comunicarse con el microservicio de Clínica"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        # Datos básicos del paciente
        patient_url = f"{base_url}/patients/get/{patient_id}"
        try:
            patient_response = requests.get(patient_url, timeout=5)
            patient_response.raise_for_status()
            patient_data = patient_response.json()
        except Exception:
            # Si falla la obtención de datos básicos del paciente, devolvemos igualmente los reportes con clinical_data
            patient_data = None

        # Construir una lista de "reportes enriquecidos" similares al ejemplo de tu compañero
        enriched_reports = []
        for report in reports:
            variant = report.variant
            gene = variant.gene

            enriched_reports.append(
                {
                    "id": str(report.id),
                    "patient_id": str(report.patient_id),
                    "variant_id": str(variant.id),
                    "gene_symbol": getattr(gene, "symbol", None),
                    "gene_full_name": getattr(gene, "full_name", None),
                    "chromosome": getattr(variant, "chromosome", None),
                    "position": getattr(variant, "position", None),
                    "reference_base": getattr(variant, "reference_base", None),
                    "alternate_base": getattr(variant, "alternate_base", None),
                    "impact": getattr(variant, "impact", None),
                    "detection_date": report.detection_date,
                    "allele_frequency": report.allele_frequency,
                    "created_at": report.created_at,
                    "updated_at": report.updated_at,
                    "patient_data": patient_data,
                }
            )

        return Response(enriched_reports)
