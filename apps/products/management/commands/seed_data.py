import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from faker import Faker

from apps.products.models import Category, Product
from apps.stores.models import Store, Inventory

fake = Faker()


class Command(BaseCommand):
    help = "Seed database with dummy data"

    def handle(self, *args, **kwargs):

        self.stdout.write("Deleting old data...")

        Inventory.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Store.objects.all().delete()

        # Categories
        self.stdout.write("Creating categories...")

        category_names = [
            "Electronics",
            "Fashion",
            "Books",
            "Home",
            "Sports",
            "Beauty",
            "Gaming",
            "Kitchen",
            "Automotive",
            "Office",
        ]

        categories = []

        for name in category_names:
            categories.append(Category(name=name))

        Category.objects.bulk_create(categories)

        categories = list(Category.objects.all())

        # Products
        self.stdout.write("Creating products...")

        products = []

        for _ in range(1000):
            products.append(
                Product(
                    title=f"{fake.word().title()} {fake.word().title()}",
                    description=fake.text(max_nb_chars=150),
                    price=Decimal(random.randint(100, 100000)),
                    category=random.choice(categories),
                )
            )

        Product.objects.bulk_create(products)

        products = list(Product.objects.all())

        # Stores
        self.stdout.write("Creating stores...")

        stores = []

        for _ in range(20):
            stores.append(
                Store(
                    name=fake.company(),
                    location=fake.city(),
                )
            )

        Store.objects.bulk_create(stores)

        stores = list(Store.objects.all())

        # Inventory
        self.stdout.write("Creating inventory...")

        inventories = []

        for store in stores:

            random_products = random.sample(products, 300)

            for product in random_products:

                inventories.append(
                    Inventory(
                        store=store,
                        product=product,
                        quantity=random.randint(0, 100),
                    )
                )

        Inventory.objects.bulk_create(inventories)

        self.stdout.write(
            self.style.SUCCESS("Database seeded successfully!")
        )