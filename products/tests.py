from django.test import TestCase, Client
from django.core.management import call_command
from django.urls import reverse
from products.models import Product

class ImportProductsTest(TestCase):
    def test_import_command(self):
        before = Product.objects.count()
        call_command('import_products')
        after = Product.objects.count()
        self.assertTrue(after > before)


class ProductViewTests(TestCase):
    def setUp(self):
        self.prod = Product.objects.create(name='P1', price=1, stock=1)
        self.client = Client()

    def test_product_list_view(self):
        resp = self.client.get(reverse('product_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.prod.name)

    def test_product_detail_view(self):
        resp = self.client.get(reverse('product_detail', args=[self.prod.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.prod.name)
