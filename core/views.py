# core/views.py
"""Vistas principales del proyecto ERP — W02.

Migración: HttpResponse → render() con templates y contexto.
"""
from django.shortcuts import render
from django.urls import reverse


def bienvenida(request):
    """Página de inicio del ERP con tarjetas de módulos.

    Context:
        modulos (list): Lista de dicts con icono, nombre, url y descripcion.

    Returns:
        HttpResponse con template bienvenida.html.
    """
    modulos = [
        {
            'nombre': 'Productos',
            'icono': '📦',
            'url': reverse('productos:lista'),
            'descripcion': 'Productos, precios y existencias',
        },
        {
            'nombre': 'Clientes',
            'icono': '👥',
            'url': reverse('clientes:lista'),
            'descripcion': 'Quién te compra y cómo contactarlo',
        },
        {
            'nombre': 'Proveedores',
            'icono': '🚚',
            'url': reverse('proveedores:lista'),
            'descripcion': 'Quién te surte y a qué precio',
        },
        {
            'nombre': 'Ventas',
            'icono': '🛒',
            'url': reverse('ventas:lista'),
            'descripcion': 'Pedidos y cobros',
        },
        {
            'nombre': 'Reportes',
            'icono': '📊',
            'url': reverse('reportes:inicio'),
            'descripcion': 'Mira cómo va tu negocio en números',
        },
        {
            'nombre': 'Administración',
            'icono': '⚙️',
            'url': '/admin/',
            'descripcion': 'Panel de administración del sistema',
        },
    ]
    return render(request, 'bienvenida.html', {'modulos': modulos})