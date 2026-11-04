"""Suite de pruebas W12 — PDF (xhtml2pdf) y exportación Excel (openpyxl)."""
from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from clientes.models import Cliente
from configuracion.models import ConfiguracionERP
from productos.models import Categoria, Producto
from ventas.models import DetalleVenta, Venta


class DocumentosW12Test(TestCase):
    def setUp(self):
        ConfiguracionERP.get_instance()
        self.user = User.objects.create_user('pdfuser', password='pass')
        cat = Categoria.objects.create(nombre='Cat Test')
        prod = Producto.objects.create(
            nombre='Producto Test', precio=Decimal('100.00'), stock=10, categoria=cat
        )
        cli = Cliente.objects.create(nombre='Cliente Test', correo='test@test.com')
        self.venta = Venta.objects.create(cliente=cli)
        DetalleVenta.objects.create(
            venta=self.venta, producto=prod, cantidad=1, precio_unitario=Decimal('100.00')
        )

    def test_pdf_sin_login_redirige(self):
        r = self.client.get(reverse('ventas:pdf', args=[self.venta.pk]))
        self.assertEqual(r.status_code, 302)

    def test_pdf_con_login_devuelve_200(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse('ventas:pdf', args=[self.venta.pk]))
        self.assertEqual(r.status_code, 200)
        self.assertIn('application/pdf', r.get('Content-Type', ''))
        self.assertTrue(r.content[:4] == b'%PDF')

    def test_excel_exportar_devuelve_200(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse('productos:exportar_excel'))
        self.assertEqual(r.status_code, 200)
        self.assertIn('spreadsheetml', r.get('Content-Type', ''))