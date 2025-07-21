import pytest

from src.main import Category, Product


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
    # Проверка корректного изменения цены
    product_1.price = 190000.0
    assert product_1.price == 190000.0

    # Проверка на некорректную цену
    product_1.price = -1000
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product_1.price == 190000.0  # Цена не изменилась


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


def test_category_init(empty_category, category_with_products):
    """Проверяет корректность инициализации объектов класса Category"""

    assert empty_category.name == "Смартфоны"
    assert empty_category.description == "Современные мобильные устройства"
    assert len(empty_category.products) == 0

    assert len(category_with_products.products) == 2
    assert "Samsung Galaxy S23 Ultra" in category_with_products.products[0]
    assert "iPhone 15 Pro" in category_with_products.products[1]


def test_category_add_product(empty_category, product_1):
    """Проверяет добавление продукта в категорию"""
    initial_count = len(empty_category.products)
    empty_category.add_product(product_1)
    assert len(empty_category.products) == initial_count + 1
    assert "Samsung Galaxy S23 Ultra" in empty_category.products[0]


def test_category_products_format(category_with_products):
    """Проверяет формат вывода списка продуктов"""
    products = category_with_products.products
    assert isinstance(products, list)
    assert len(products) == 2
    assert all(", " in item and " руб. Остаток: " in item for item in products)


def test_category_count():
    """Проверяет подсчет количества категорий и товаров"""
    Category.category_count = 0
    Category.product_count = 0

    p1 = Product("Продукт 1", "Описание 1", 1000, 2)
    p2 = Product("Продукт 2", "Описание 2", 2000, 3)
    p3 = Product("Продукт 3", "Описание 3", 3000, 1)

    Category("Категория 1", "Описание 1", [p1, p2])
    Category("Категория 2", "Описание 2", [p3])

    assert Category.category_count == 2
    assert Category.product_count == 3


def test_add_wrong_product(empty_category):
    """Проверяет обработку попытки добавить неверный тип продукта"""
    with pytest.raises(
        TypeError, match="Можно добавлять только объекты класса Product"
    ):
        empty_category.add_product("Не продукт")
