from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from LAMBDA_ordenes_facturacion_API.correo import enviar_correo
from .models import Usuario
from .serializers import UsuarioSerializer, UsuarioLoginSerializer

class UsuarioView(APIView):

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        try:
            usuario = Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        serializer = UsuarioLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['usuario']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'usuario': UsuarioSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SolicitudCambioContrasenaView(APIView):
    def post(self, request):
        correo = request.data.get('correo')
        if not correo:
            return Response({"error": "El campo 'correo' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            usuario = Usuario.objects.get(correo=correo)
            # Aquí se implementaría la lógica para enviar el correo de cambio de contraseña
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario con este correo no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        #Generar token de reseteo y guardarlo en el usuario
        usuario.create_reset_token()

        #Enviar correo con el token
        url = f"{settings.FRONTEND_URL}{settings.CAMBIO_PASSWORD_URL}?token={usuario.reset_password_token}"
        print(url)  # Para propósitos de depuración, eliminar en producción
        enviar_correo(
            asunto="Solicitud de cambio de contraseña",
            plantilla="cambio_contrasenia.html",
            contexto={
                "usuario": usuario,
                "link": url
            },
            destinatarios=[usuario.correo]
        )

        return Response({"message": "Correo de cambio de contraseña enviado."}, status=status.HTTP_200_OK)

class CambioContrasenaView(APIView):
    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({"error": "El parámetro 'token' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            usuario = Usuario.objects.get(reset_password_token=token)
            if not usuario.validate_reset_token(token):
                return Response({"error": "Token inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)
        except Usuario.DoesNotExist:
            return Response({"error": "Token inválido."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Token válido."}, status=status.HTTP_200_OK)

    def post(self, request):
        token = request.data.get('token')
        nueva_contrasena = request.data.get('nueva_contrasena')
        confirmacion_contrasena = request.data.get('confirmacion_contrasena')

        if not token:
            return Response({"error": "El campo 'token' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            usuario = Usuario.objects.get(reset_password_token=token)
            if not usuario.validate_reset_token(token):
                return Response({"error": "Token inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)
        except Usuario.DoesNotExist:
            return Response({"error": "Token inválido."}, status=status.HTTP_400_BAD_REQUEST)
        
        #Validar las contraseñas
        if not nueva_contrasena or not confirmacion_contrasena:
            return Response({"error": "Los campos de contraseña son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)
        
        if nueva_contrasena != confirmacion_contrasena:
            return Response({"error": "Las contraseñas no coinciden."}, status=status.HTTP_400_BAD_REQUEST) 
        
        usuario.set_password(nueva_contrasena)
        usuario.reset_password_token = None
        usuario.reset_token_created_at = None
        usuario.save()
        
        return Response({"message": "Contraseña cambiada exitosamente."}, status=status.HTTP_200_OK)
