# ventas/urls.py
"""URLs de la app ventas — W02."""
from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('', views.index, name='inicio'),
    # Espiral 2 W05:
    # path('lista/',          views.ventasListView.as_view(),   name='lista'),
    # path('nuevo/',          views.ventasCreateView.as_view(), name='crear'),
    # path('<int:pk>/',       views.ventasDetailView.as_view(), name='detalle'),
    # path('<int:pk>/editar/',views.ventasUpdateView.as_view(), name='editar'),
]