from django.urls import path
from .views import LoginView, UsuarioView, SolicitudCambioContrasenaView, CambioContrasenaView

urlpatterns = [
    path('usuarios/', UsuarioView.as_view(), name='usuario-list-create'),
    path('login/', LoginView.as_view(), name='usuario-login'),
    path('solicitud-cambio-password/', SolicitudCambioContrasenaView.as_view(), name='solicitud-cambio-password'),
    path('cambio-password/', CambioContrasenaView.as_view(), name='cambio-password'),
]