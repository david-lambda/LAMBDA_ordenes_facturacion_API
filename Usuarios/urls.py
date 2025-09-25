from django.urls import path
from .views import LoginView, UsuarioView

urlpatterns = [
    path('usuarios/', UsuarioView.as_view(), name='usuario-list-create'),
    path('login/', LoginView.as_view(), name='usuario-login'),
]