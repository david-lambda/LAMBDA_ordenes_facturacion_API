from django.contrib import admin
from .models import Producto, CategoriaProducto, MoviementoProducto

admin.site.register(Producto)
admin.site.register(CategoriaProducto)
admin.site.register(MoviementoProducto)
