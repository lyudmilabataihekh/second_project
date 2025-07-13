import pytest

from src.main import Category, Product


@pytest.fixture
def product_1():
    return Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )


def test_init(product_1):
    """Проверяет корректность инициализации объектов класса Product"""
    assert product_1.name == "Samsung Galaxy S23 Ultra"
    assert product_1.description == "256GB, Серый цвет, 200MP камера"
    assert product_1.price == 180000.0
    assert product_1.quantity == 5


@pytest.fixture
def category(product_1):
    return Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, "
        "но и получения дополнительных функций для удобства жизни",
        [product_1],
    )


def test_category(category):
    """Проверяет корректность инициализации объектов класса Category"""
    assert category.name == "Смартфоны"
    assert category.description == (
        "Смартфоны, как средство не только коммуникации, "
        "но и получения дополнительных функций для удобства жизни"
    )


def test_counters():
    """Проверяет подсчет количества продуктов"""
    Category.category_count = 0
    Category.product_count = 0


def test_category_count():
    """Проверяет подсчет количества категорий"""
    test_counters()

    Category("Категория 1", "Описание", ["Продукт 1", "Продукт 2"])
    Category("Категория 2", "Описание", ["Продукт 3"])

    assert Category.category_count == 2
    assert Category.product_count == 3
