# proveedoress/urls.py
"""URLs de la app proveedores — W02."""
from django.urls import path
from . import views

app_name = 'proveedores'

urlpatterns = [
    path('', views.index, name='inicio'),
    # Espiral 2 W05:
    # path('lista/',          views.proveedoresListView.as_view(),   name='lista'),
    # path('nuevo/',          views.proveedoresCreateView.as_view(), name='crear'),
    # path('<int:pk>/',       views.proveedoresDetailView.as_view(), name='detalle'),
    # path('<int:pk>/editar/',views.proveedoresUpdateView.as_view(), name='editar'),
]