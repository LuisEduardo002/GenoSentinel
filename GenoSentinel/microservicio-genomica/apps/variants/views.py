from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .models import GeneticVariant
from .serializers import GeneticVariantSerializer


class GeneticVariantCreateView(APIView):
    """Crear una nueva variante genética"""

    @extend_schema(
        request=GeneticVariantSerializer,
        responses={
            201: GeneticVariantSerializer,
            400: {"description": "Datos inválidos"},
        },
        summary="Crear una nueva variante genética",
        tags=["variants"],
    )
    def post(self, request):
        serializer = GeneticVariantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def _get_variant_or_404(pk):
    try:
        return GeneticVariant.objects.get(pk=pk)
    except GeneticVariant.DoesNotExist:
        return None

class GeneticVariantRetrieveView(APIView):
    """Obtener una variante genética por ID"""

    @extend_schema(
        responses={
            200: GeneticVariantSerializer,
            404: {"description": "Variante no encontrada"},
        },
        summary="Obtener una variante genética por ID",
        tags=["variants"],
    )
    def get(self, request, pk):
        variant = _get_variant_or_404(pk)
        if variant is None:
            return Response({"detail": "Variant not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GeneticVariantSerializer(variant)
        return Response(serializer.data)


class GeneticVariantUpdateView(APIView):
    """Actualizar una variante genética por ID"""

    @extend_schema(
        request=GeneticVariantSerializer,
        responses={
            200: GeneticVariantSerializer,
            400: {"description": "Datos inválidos"},
            404: {"description": "Variante no encontrada"},
        },
        summary="Actualizar una variante genética por ID",
        tags=["variants"],
    )
    def patch(self, request, pk):
        variant = _get_variant_or_404(pk)
        if variant is None:
            return Response({"detail": "Variant not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GeneticVariantSerializer(variant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GeneticVariantDeleteView(APIView):
    """Eliminar una variante genética por ID"""

    @extend_schema(
        responses={
            204: None,
            404: {"description": "Variante no encontrada"},
        },
        summary="Eliminar una variante genética por ID",
        tags=["variants"],
    )
    def delete(self, request, pk):
        variant = _get_variant_or_404(pk)
        if variant is None:
            return Response({"detail": "Variant not found"}, status=status.HTTP_404_NOT_FOUND)
        variant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GeneticVariantListView(APIView):
    """Listar variantes genéticas, con filtros opcionales"""

    @extend_schema(
        responses={200: GeneticVariantSerializer(many=True)},
        summary="Listar variantes genéticas",
        tags=["variants"],
    )
    def get(self, request):
        gene_id = request.query_params.get("gene_id")
        chromosome = request.query_params.get("chromosome")
        impact = request.query_params.get("impact")

        queryset = GeneticVariant.objects.all()
        if gene_id:
            queryset = queryset.filter(gene_id=gene_id)
        if chromosome:
            queryset = queryset.filter(chromosome__iexact=chromosome)
        if impact:
            queryset = queryset.filter(impact=impact)

        serializer = GeneticVariantSerializer(queryset, many=True)
        return Response(serializer.data)
