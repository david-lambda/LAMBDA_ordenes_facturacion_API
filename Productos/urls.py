from django.urls import path, include
from .Views.Categoria_Producto import *

urlpatterns = [
    path('categoria-producto/', CategoriaProductoView.as_view(), name='categoria_producto_detail'),
    path('categoria-producto/<int:pk>/', CategoriaProductoView.as_view(), name='categoria_producto_detail'),

]

