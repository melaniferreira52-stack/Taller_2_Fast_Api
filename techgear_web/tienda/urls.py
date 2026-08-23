from django.urls import path
from .views import catalogo_productos

urlpatterns = [
    path('', catalogo_productos, name='catalogo'),
]