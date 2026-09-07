from django.urls import path
from .views import catalogo_productos, panel_admin, productos_admin, producto_crear, producto_editar, producto_eliminar, historial_pedidos, detalle_pedido, checkout

urlpatterns = [
    path('', catalogo_productos, name='catalogo'),
    path('panel/', panel_admin, name='panel_admin'),
    path('panel/productos/', productos_admin, name='productos_admin'),
    path('panel/productos/nuevo/', producto_crear, name='producto_crear'),
    path('panel/productos/<str:producto_id>/editar/', producto_editar, name='producto_editar'),
    path('panel/productos/<str:producto_id>/eliminar/', producto_eliminar, name='producto_eliminar'),
    path('panel/pedidos/', historial_pedidos, name='historial_pedidos'),
    path('panel/pedidos/<str:pedido_id>/', detalle_pedido, name='detalle_pedido'),
    path('checkout/<str:producto_id>/', checkout, name='checkout'),



]