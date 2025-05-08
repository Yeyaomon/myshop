from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import Product
from .models import Cart, CartItem, Order

class CartAndCheckoutTests(TestCase):
    def setUp(self):
        # Register test user and product
        self.user = User.objects.create_user('u', 'u@example.com', 'pw')
        self.prod = Product.objects.create(name='Test', price=10, stock=5)
        self.client = Client()

    def test_add_view_remove_cart(self):
        # view_cart requires login
        resp = self.client.get(reverse('view_cart'))
        self.assertEqual(resp.status_code, 302)

        self.client.login(username='u', password='pw')

        # add to cart
        resp = self.client.get(reverse('add_to_cart', args=[self.prod.id]))
        self.assertRedirects(resp, reverse('view_cart'))
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)

        # view_cart normal mode has no "Delete Selected"
        resp = self.client.get(reverse('view_cart'))
        self.assertNotContains(resp, 'Delete Selected')

        # view_cart edit mode shows "Delete Selected"
        resp = self.client.get(reverse('view_cart') + '?edit=1')
        self.assertContains(resp, 'Delete Selected')

        # remove from cart
        item_id = cart.items.first().id
        resp = self.client.post(reverse('remove_from_cart'), {'item_ids': [item_id]})
        self.assertRedirects(resp, reverse('view_cart'))
        self.assertEqual(cart.items.count(), 0)

    def test_checkout_selected_and_error(self):
        self.client.login(username='u', password='pw')
        # add to cart
        self.client.get(reverse('add_to_cart', args=[self.prod.id]))
        cart = Cart.objects.get(user=self.user)
        item_id = cart.items.first().id

        # error when no items selected
        resp = self.client.post(reverse('checkout'), {})
        self.assertContains(resp, 'Please select at least one item to checkout.')

        # successful checkout of selected item
        resp = self.client.post(reverse('checkout'), {'item_ids': [item_id]})
        self.assertContains(resp, 'Thank you')
        self.assertEqual(Order.objects.filter(user=self.user).count(), 1)


class OrderHistoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('u2', 'u2@example.com', 'pw')
        self.order = Order.objects.create(user=self.user, total_amount=123)
        self.client = Client()
        self.client.login(username='u2', password='pw')

    def test_order_list_and_detail(self):
        # order list page
        resp = self.client.get(reverse('order_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, f'Order #{self.order.id}')

        # order detail page
        resp = self.client.get(reverse('order_detail', args=[self.order.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '123')
