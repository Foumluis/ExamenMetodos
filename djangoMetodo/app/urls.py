
from django.urls import path, include

from . import views

urlpatterns = [
    # Home
    path('home/', views.home, name='home'),
    
    # Análisis Univariado
    path('univariado/distribucion-genero/', views.distribucion_clientes_genero, name='distribucion_genero'),
    
    # Análisis Bivariado
    path('bivariado/comparacion-generos/', views.comparacion_compras_generos, name='comparacion_generos'),
    path('bivariado/categoria-monto/', views.relacion_categoria_monto, name='categoria_monto'),
    path('bivariado/ventas-categoria/', views.cantidad_ventas_categoria, name='ventas_categoria'),
    
    # Análisis de Ubicación
    path('ubicacion/ubicacion-monto/', views.relacion_ubicacion_monto, name='ubicacion_monto'),
    path('ubicacion/presencia-geografica/', views.presencia_geografica, name='presencia_geografica'),
    
    # Análisis Multivariado
    path('multivariado/categoria-talla/', views.compras_categoria_talla, name='categoria_talla'),
    
    # Problemas
    path('problemas/', views.problemas, name='problemas'),
    path('problemas/problema1/', views.problema1, name='problema1'),
    path('problemas/problema2/', views.problema2, name='problema2'),
    path('problemas/problema3/', views.problema3, name='problema3'),
    
    # Alcance
    path('alcance/', views.alcance, name='alcance'),
]
    