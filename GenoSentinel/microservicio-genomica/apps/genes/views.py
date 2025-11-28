from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .models import Gene
from .serializers import GeneSerializer


class GeneCreateView(APIView):
    """Crear un nuevo gen"""

    @extend_schema(
        request=GeneSerializer,
        responses={
            201: GeneSerializer,
            400: {"description": "Datos inválidos"},
        },
        summary="Crear un nuevo gen",
        tags=["genes"],
    )
    def post(self, request):
        serializer = GeneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def _get_gene_or_404(pk):
    try:
        return Gene.objects.get(pk=pk)
    except Gene.DoesNotExist:
        return None


class GeneRetrieveView(APIView):
    """Obtener un gen por ID"""

    @extend_schema(
        responses={
            200: GeneSerializer,
            404: {"description": "Gen no encontrado"},
        },
        summary="Obtener un gen por ID",
        tags=["genes"],
    )
    def get(self, request, pk):
        gene = _get_gene_or_404(pk)
        if gene is None:
            return Response({"detail": "Gene not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GeneSerializer(gene)
        return Response(serializer.data)


class GeneUpdateView(APIView):
    """Actualizar un gen por ID"""

    @extend_schema(
        request=GeneSerializer,
        responses={
            200: GeneSerializer,
            400: {"description": "Datos inválidos"},
            404: {"description": "Gen no encontrado"},
        },
        summary="Actualizar un gen por ID",
        tags=["genes"],
    )
    def patch(self, request, pk):
        gene = _get_gene_or_404(pk)
        if gene is None:
            return Response({"detail": "Gene not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GeneSerializer(gene, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GeneDeleteView(APIView):
    """Eliminar un gen por ID"""

    @extend_schema(
        responses={
            204: None,
            404: {"description": "Gen no encontrado"},
        },
        summary="Eliminar un gen por ID",
        tags=["genes"],
    )
    def delete(self, request, pk):
        gene = _get_gene_or_404(pk)
        if gene is None:
            return Response({"detail": "Gene not found"}, status=status.HTTP_404_NOT_FOUND)
        gene.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GeneListView(APIView):
    """Listar genes, opcionalmente filtrando por símbolo"""

    @extend_schema(
        responses={200: GeneSerializer(many=True)},
        summary="Listar genes",
        tags=["genes"],
    )
    def get(self, request):
        symbol = request.query_params.get("symbol")
        queryset = Gene.objects.all()
        if symbol:
            queryset = queryset.filter(symbol__icontains=symbol)
        serializer = GeneSerializer(queryset, many=True)
        return Response(serializer.data)
