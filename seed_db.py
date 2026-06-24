import os
import django
import random
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth.models import User
from shop.models import Category, Manufacturer, Product, Cart, CartItem

def seed():
    CartItem.objects.all().delete()
    Cart.objects.all().delete()
    Product.objects.all().delete()
    Manufacturer.objects.all().delete()
    Category.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()

    manufacturers = []
    m_data = [("Canon", "Япония"), ("Nikon", "Япония"), ("Sony", "Япония"), ("Fujifilm", "Япония"), ("Panasonic", "Япония")]
    for name, country in m_data:
        m = Manufacturer.objects.create(name=name, country=country, description=f"Производитель {name}")
        manufacturers.append(m)

    categories = []
    for i in range(1, 11):
        c = Category.objects.create(name=f"Категория {i}", description=f"Описание категории {i}")
        categories.append(c)

    products = []
    for i in range(1, 35):
        p = Product.objects.create(
            name=f"Фототовар {i}",
            description=f"Подробное описание фототовара под номером {i}",
            product_image="products/default.jpg",
            price=Decimal(random.randint(100, 2000)),
            stock_quantity=random.randint(10, 50),
            category=random.choice(categories),
            manufacturer=random.choice(manufacturers)
        )
        products.append(p)

    for i in range(1, 6):
        user = User.objects.create_user(username=f"user_{i}", password="password123")
        cart = Cart.objects.create(user=user)
        selected_products = random.sample(products, 2)
        for prod in selected_products:
            CartItem.objects.create(cart=cart, product=prod, quantity=random.randint(1, 3))

    print("База успешно заполнена тестовыми данными!")

if __name__ == "__main__":
    seed()