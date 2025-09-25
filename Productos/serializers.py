from rest_framework import serializers
from .models import Producto, CategoriaProducto, MoviementoProducto

class CategoriaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaProducto
        fields = ['id', 'nombre']
        
    def validate_nombre(self, value):
        existing = CategoriaProducto.objects.get(nombre__iexact=value)
        if self.instance and existing.id != self.instance.id:
            raise serializers.ValidationError("Ya existe una categoría con este nombre.")
        elif not self.instance:
            raise serializers.ValidationError("Ya existe una categoría con este nombre.")
        return value.title()
        
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'categoria', 'stock']
    
    