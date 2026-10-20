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
            'nombre': 'La despensa embrujada',
            'icono': '🎃',
            'url': reverse('productos:inicio'),
            'descripcion': 'Productos, precios y existencias bajo vigilancia',
        },
        {
            'nombre': 'Los visitantes de la noche',
            'icono': '🧛',
            'url': reverse('clientes:inicio'),
            'descripcion': 'Quién te compra y cómo contactarlo',
        },
        {
            'nombre': 'Los brujos proveedores',
            'icono': '🧙',
            'url': reverse('proveedores:inicio'),
            'descripcion': 'Quién te surte la poción y a qué precio',
        },
        {
            'nombre': 'El caldero de ventas',
            'icono': '🍬',
            'url': reverse('ventas:inicio'),
            'descripcion': 'Pedidos y cobros: el botín de la noche',
        },
        {
            'nombre': 'La bola de cristal',
            'icono': '🔮',
            'url': reverse('reportes:inicio'),
            'descripcion': 'Mira cómo va tu negocio en números',
        },
        {
            'nombre': 'El laboratorio secreto',
            'icono': '🦇',
            'url': '/admin/',
            'descripcion': 'Panel de administración para tus hechizos',
        },
    ]
    return render(request, 'bienvenida.html', {'modulos': modulos})