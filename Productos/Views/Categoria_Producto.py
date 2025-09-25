from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response 
from rest_framework import status 
from ..models import CategoriaProducto
from ..serializers import CategoriaProductoSerializer


def get_categoria_producto_por_id(id):
    """Función para obtener una categoría de producto por su ID."""
    try:
        return CategoriaProducto.objects.get(id=id)
    except CategoriaProducto.DoesNotExist:
        return None

class CategoriaProductoView(APIView):
    def get(self, request, pk=None):
        if pk:
            categoria = get_categoria_producto_por_id(pk)
            if not categoria:
                return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CategoriaProductoSerializer(categoria)
        else:
            categorias = CategoriaProducto.objects.all()
            paginator = LimitOffsetPagination()
            categorias = paginator.paginate_queryset(categorias, request, view=self)
            serializer = CategoriaProductoSerializer(categorias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CategoriaProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        categoria = get_categoria_producto_por_id(pk)
        if not categoria:
            return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategoriaProductoSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        categoria = get_categoria_producto_por_id(pk)
        if not categoria:
            return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    
    
    
    