import pytest

from src.main import Category, Product, Smartphone, LawnGrass


@pytest.fixture
def product_1():
    return Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )


@pytest.fixture
def product_2():
    return Product("iPhone 15 Pro", "512GB, Титан, камера 48MP", 200000.0, 3)


def test_product_init(product_1):
    """Проверяет корректность инициализации объектов класса Product"""
    assert product_1.name == "Samsung Galaxy S23 Ultra"
    assert product_1.description == "256GB, Серый цвет, 200MP камера"
    assert product_1.price == 180000.0
    assert product_1.quantity == 5


def test_product_price_setter(product_1, capsys):
    """Проверяет работу сеттера цены"""
    product_1.price = 190000.0
    assert product_1.price == 190000.0

    product_1.price = -1000
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out

    assert product_1.price == 190000.0


def test_product_new_product():
    """Проверяет работу фабричного метода new_product"""
    product_data = {
        "name": "Xiaomi 13 Pro",
        "description": "256GB, Зеленый",
        "price": 120000.0,
        "quantity": 7,
    }
    product = Product.new_product(product_data)
    assert isinstance(product, Product)
    assert product.name == "Xiaomi 13 Pro"
    assert product.description == "256GB, Зеленый"
    assert product.price == 120000.0
    assert product.quantity == 7


@pytest.fixture
def empty_category():
    """Создает пустую категорию"""
    return Category("Смартфоны", "Современные мобильные устройства")


@pytest.fixture
def category_with_products(product_1, product_2):
    """Создает категорию с продуктами"""
    category = Category(
        "Смартфоны", "Современные мобильные устройства", [product_1, product_2]
    )
    return category


def test_counters():
    product = Product("Тестовый продукт", "Описание", 5000, 10)
    assert product.name == "Тестовый продукт"
    assert product.description == "Описание"
    assert product.price == 5000
    assert product.quantity == 10


def test_category_init(empty_category, category_with_products):
    """Проверяет корректность инициализации объекта Category"""

    assert empty_category.name == "Смартфоны"
    assert empty_category.description == "Современные мобильные устройства"
    assert len(empty_category.products) == 0

    assert len(category_with_products.products) == 2

    assert "Samsung Galaxy S23 Ultra" in str(category_with_products.products[0])
    assert "iPhone 15 Pro" in str(category_with_products.products[1])


def test_category_add_product(empty_category, product_1):
    """Проверяет добавление продукта в категорию"""
    initial_count = len(empty_category.products)
    empty_category.add_product(product_1)
    assert len(empty_category.products) == initial_count + 1

    assert "Samsung Galaxy S23 Ultra" in str(empty_category.products[0])


def test_category_products_format(category_with_products):
    """Проверяет формат вывода списка продуктов"""
    products = category_with_products.products
    assert isinstance(products, list)
    assert len(products) == 2

    assert all(", " in str(p) and " руб. Остаток: " in str(p) for p in products)


def test_add_wrong_product(empty_category):
    """Проверяет обработку попытки добавить неверный тип продукта"""
    with pytest.raises(
        TypeError, match="Можно добавлять только объекты класса Product"
    ):
        empty_category.add_product("Не продукт")


def test_category_count():
    """Проверяет подсчет количества категорий и товаров"""
    Category.category_count = 0
    Category.product_count = 0

    Product("Продукт 1", "Описание 1", 1000, 2)
    Product("Продукт 2", "Описание 2", 2000, 3)
    Product("Продукт 3", "Описание 3", 3000, 1)


@pytest.fixture
def products_example():
    return [
        Product("Продукт 1", "Описание 1", 1000, 2),
        Product("Продукт 2", "Описание 2", 2000, 3),
    ]


def test_product_str(products_example):
    """Проверяет вывод названия, цены и остатка продуктов"""
    assert str(products_example[0]) == "Продукт 1, 1000 руб. Остаток: 2 шт."
    assert str(products_example[1]) == "Продукт 2, 2000 руб. Остаток: 3 шт."


def test_product_add():
    """Проверяет подсчет количества товаров в наличии"""
    p1 = Product("Продукт 1", "Описание 1", 1000, 2)
    p2 = Product("Продукт 2", "Описание 2", 2000, 3)

    assert p1 + p2 == 8000


def test_category_str(products_example):
    """Проверяет подсчет названий категорий и количества продуктов на складе"""
    category = Category("Категория А", "Описание категории", products_example)
    total_quantity = sum(product.quantity for product in products_example)
    expected_str = f"Категория А, количество продуктов: {total_quantity} шт."
    assert str(category) == expected_str


def test_smartphone_add():
    """Проверяет сложение товаров и подсчет стоимости"""
    smartphone1 = Smartphone("Phone1", "desc", 1000, 2, "A", "ModelX", "64GB", "Black")
    smartphone2 = Smartphone("Phone2", "desc", 1500, 3, "A", "ModelY", "128GB", "White")
    total_price = smartphone1 + smartphone2
    expected = (smartphone1.price * smartphone1.quantity) + (
        smartphone2.price * smartphone2.quantity
    )
    assert total_price == expected


def test_lawngrass_add():
    """Проверяет сложение товаров и подсчет стоимости"""
    lawn1 = LawnGrass("Lawn1", "desc", 20, 5, "Russia", 15, "Green")
    lawn2 = LawnGrass("Lawn2", "desc", 25, 3, "Russia", 10, "Dark Green")
    total_price = lawn1 + lawn2
    expected = (lawn1.price * lawn1.quantity) + (lawn2.price * lawn2.quantity)
    assert total_price == expected


def test_error_raise():
    """Проверяет обработку ошибки TypeError"""
    smartphone = Smartphone("Phone", "desc", 1000, 2, "A", "ModelX", "64GB", "Black")
    lawn = LawnGrass("Lawn", "desc", 20, 5, "Russia", 15, "Green")
    with pytest.raises(TypeError):
        smartphone + lawn
