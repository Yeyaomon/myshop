import random, django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myshop.settings")
django.setup()

from faker import Faker
from django.contrib.auth.models import User
from products.models import Product
from orders.models import Order, OrderItem

# ./scipts/generate_fake.py
fake = Faker()

# User Registration
for _ in range(20):
    u = fake.user_name()
    if not User.objects.filter(username=u).exists():
        User.objects.create_user(username=u, email=fake.email(), password='123456')
users = list(User.objects.filter(is_staff=False))
prods = list(Product.objects.all())
# Order Generater
for _ in range(50):
    user = random.choice(users)
    o = Order.objects.create(user=user)
    for i in range(random.randint(1,4)):
        p = random.choice(prods)
        q = random.randint(1,3)
        OrderItem.objects.create(order=o, product=p, quantity=q, price=p.price)
        p.stock = max(0, p.stock - q); p.save()
    o.total_amount = sum(i.price*i.quantity for i in o.orderitem_set.all())
    o.save()
print("Fake data generation has completed")
