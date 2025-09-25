from django.db import models
from Base.models import BaseModel, DatoArchivo

class CategoriaProducto(BaseModel):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la categoría", null=False, blank=False, unique=True)
    
    class Meta:
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Productos"
        db_table = "categorias_productos"

    def __str__(self):
        return self.nombre.title()
    
class Producto(BaseModel):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del producto")
    descripcion = models.TextField(verbose_name="Descripción del producto")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio del producto")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad en stock")
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.PROTECT, related_name="productos", verbose_name="Categoría")
    imagen = models.ForeignKey(DatoArchivo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Imagen del producto")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        db_table = "productos"

    def __str__(self):
        return f"{self.nombre} - {self.categoria.nombre}".title()
    
class MoviementoProducto(BaseModel):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="movimientos", verbose_name="Producto")
    cantidad = models.IntegerField(verbose_name="Cantidad cambiada (positiva o negativa)")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio del producto en el momento del cambio", null=True, blank=True)
    motivo = models.CharField(max_length=255, verbose_name="Motivo del cambio de inventario", null=True, blank=True)

    class Meta:
        verbose_name = "Movimiento de Producto"
        verbose_name_plural = "Movimientos de Productos"
        db_table = "movimientos_productos"

    def __str__(self):
        return f"{self.producto.nombre} - Cambio: {self.cantidad} - Motivo: {self.motivo}".title()

