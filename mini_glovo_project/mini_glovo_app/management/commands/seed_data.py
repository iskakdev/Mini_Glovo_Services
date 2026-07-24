import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker

from mini_glovo_app.models import Category, Store, Product, Review

fake = Faker('ru_RU')


CATEGORIES = [
    'Рестораны',
    'Супермаркеты',
    'Аптеки',
    'Цветы',
    'Электроника',
    'Кофейни',
    'Пекарни',
    'Зоомагазины',
]

STORES = {
    'Рестораны': [
        ('Bellissimo Pizza', 'Итальянская пицца на дровах, паста и брускетты. Быстрая доставка горячих блюд.'),
        ('Sushi Master', 'Свежие суши и роллы от шеф-повара с 15-летним опытом. Только качественная рыба.'),
        ('Burger House', 'Сочные бургеры из мраморной говядины, картофель фри и молочные коктейли.'),
        ('Дом Плова', 'Настоящий узбекский плов, шашлык и лепёшки из тандыра.'),
        ('Green Bowl', 'Полезные боулы, салаты и смузи для тех, кто следит за питанием.'),
    ],
    'Супермаркеты': [
        ('FreshMart', 'Свежие продукты, овощи и фрукты каждый день. Доставка за 30 минут.'),
        ('Народный', 'Широкий ассортимент продуктов по доступным ценам.'),
        ('EcoStore', 'Органические и фермерские продукты без химии.'),
    ],
    'Аптеки': [
        ('Аптека 36.6', 'Лекарства, витамины и товары для здоровья с доставкой на дом.'),
        ('Здоровье+', 'Широкий выбор медикаментов, консультация фармацевта онлайн.'),
    ],
    'Цветы': [
        ('Flower Room', 'Свежие букеты и композиции на любой праздник, доставка за час.'),
        ('Bloom Studio', 'Авторские букеты от флористов, оформление мероприятий.'),
    ],
    'Электроника': [
        ('TechZone', 'Смартфоны, ноутбуки и аксессуары с гарантией от производителя.'),
        ('GadgetPro', 'Умные гаджеты, наушники и зарядные устройства.'),
    ],
    'Кофейни': [
        ('Coffee Lab', 'Спешелти кофе, выпечка и авторские десерты.'),
        ('Bean&Go', 'Кофе навынос из зёрен собственной обжарки.'),
    ],
    'Пекарни': [
        ('Хлебный Дом', 'Свежая выпечка, хлеб на закваске и пирожные каждый день.'),
        ('Croissant Story', 'Французская выпечка, круассаны и багеты.'),
    ],
    'Зоомагазины': [
        ('PetShop', 'Корма, аксессуары и товары для ухода за питомцами.'),
        ('ЛапаДруга', 'Всё для собак и кошек: от игрушек до ветаптеки.'),
    ],
}

PRODUCTS = {
    'Рестораны': [
        ('Пицца Маргарита', 15.90), ('Пицца Пепперони', 18.50),
        ('Ролл Филадельфия', 12.90), ('Ролл Калифорния', 11.50),
        ('Бургер Классик', 9.90), ('Чизбургер Делюкс', 11.90),
        ('Плов с бараниной', 8.50), ('Шашлык из курицы', 10.90),
        ('Боул с киноа и лососем', 13.90), ('Смузи манго-банан', 6.50),
    ],
    'Супермаркеты': [
        ('Молоко 3.2% 1л', 1.80), ('Хлеб пшеничный', 1.20),
        ('Яйца куриные 10шт', 2.90), ('Яблоки 1кг', 2.50),
        ('Куриное филе 1кг', 6.90), ('Сыр Гауда 300г', 5.40),
    ],
    'Аптеки': [
        ('Парацетамол 500мг №20', 2.10), ('Витамин C 1000мг №30', 4.90),
        ('Термометр электронный', 8.90), ('Маска медицинская 50шт', 6.50),
    ],
    'Цветы': [
        ('Букет из 25 роз', 35.00), ('Композиция "Весна"', 42.00),
        ('Букет тюльпанов 15шт', 22.00), ('Орхидея в горшке', 18.00),
    ],
    'Электроника': [
        ('Наушники беспроводные', 45.00), ('Powerbank 10000mAh', 22.00),
        ('Смарт-часы', 89.00), ('Зарядное устройство USB-C', 12.00),
    ],
    'Кофейни': [
        ('Капучино 300мл', 3.20), ('Латте 350мл', 3.50),
        ('Круассан с миндалём', 2.80), ('Чизкейк Нью-Йорк', 4.20),
    ],
    'Пекарни': [
        ('Багет французский', 1.90), ('Круассан классический', 1.60),
        ('Пирог с вишней', 3.90), ('Булочка с корицей', 2.10),
    ],
    'Зоомагазины': [
        ('Корм для кошек 1кг', 7.50), ('Корм для собак 3кг', 15.90),
        ('Игрушка-мышка', 2.30), ('Наполнитель для кота 5л', 6.80),
    ],
}

REVIEW_TEMPLATES = [
    'Отличный магазин, всё пришло вовремя и в хорошем состоянии.',
    'Доставка быстрая, качество на высоте, буду заказывать ещё.',
    'Немного задержали заказ, но в целом всё понравилось.',
    'Товар соответствует описанию, упаковка аккуратная.',
    'Хороший ассортимент, приятные цены, рекомендую.',
    'Заказ пришёл холодным, но вкус был хороший.',
    'Первый раз заказывал, остался доволен сервисом.',
    'Курьер вежливый, всё привёз аккуратно и быстро.',
    'Есть небольшие недочёты, но в целом магазин достойный.',
    'Прекрасное качество продукции, буду постоянным клиентом.',
]


class Command(BaseCommand):
    help = 'Заполняет базу реалистичными тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Удалить все данные (категории, магазины, товары, отзывы) перед заполнением',
        )
        parser.add_argument(
            '--flush-reviews',
            action='store_true',
            help='Удалить только отзывы (без пересоздания остальных данных)',
        )
        parser.add_argument(
            '--no-reviews',
            action='store_true',
            help='Не создавать отзывы при заполнении',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['flush_reviews']:
            count = Review.objects.count()
            Review.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Удалено отзывов: {count}'))
            return

        if options['flush']:
            Review.objects.all().delete()
            Product.objects.all().delete()
            Store.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING('Старые данные удалены'))

        category_objs = {}
        for name in CATEGORIES:
            category, _ = Category.objects.get_or_create(category_name=name)
            category_objs[name] = category

        store_owner_id = 1
        user_id = 1
        stores_created = 0
        products_created = 0
        reviews_created = 0
        today = timezone.now().date()

        for category_name, stores in STORES.items():
            category = category_objs[category_name]
            for store_name, description in stores:
                store = Store.objects.create(
                    category=category,
                    store_name=store_name,
                    description=description,
                    store_owner=store_owner_id,
                )
                stores_created += 1
                store_owner_id += 1

                for product_name, price in PRODUCTS[category_name]:
                    Product.objects.create(
                        store=store,
                        product_name=product_name,
                        price=price,
                        description=fake.sentence(nb_words=10),
                    )
                    products_created += 1

                if not options['no_reviews']:
                    for _ in range(random.randint(2, 5)):
                        review = Review.objects.create(
                            user=user_id,
                            store=store,
                            text=random.choice(REVIEW_TEMPLATES),
                        )
                        random_date = today - timedelta(days=random.randint(0, 180))
                        Review.objects.filter(pk=review.pk).update(created_date=random_date)
                        reviews_created += 1
                        user_id += 1

        self.stdout.write(self.style.SUCCESS(
            f'Создано: {len(category_objs)} категорий, '
            f'{stores_created} магазинов, '
            f'{products_created} товаров, '
            f'{reviews_created} отзывов.'
        ))