from rest_framework.views import APIView
from rest_framework.response import JsonResponse
from ..models import DatoArchivo

class ObtenerArchivoView(APIView):
    
    def get(self, request, pk):
        pass
    