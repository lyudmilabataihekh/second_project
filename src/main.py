from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Выводит основную информацию о товаре"""

    @abstractmethod
    def get_data(self):
        pass


class CreatedObjectMixin:
    """Миксин для создания объектов с базовыми атрибутами"""

    name: str
    description: str
    _Product__price = int
    quantity: int

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f'name="{self.name}", '
            f'description="{self.description}", '
            f'price="{self._Product__price}", '
            f'quantity="{self.quantity}")'
        )


class Product(CreatedObjectMixin, BaseProduct):
    """Класс представляющий товар"""

    def __init__(self, name, description, price, quantity):
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        super().__init__()

    @classmethod
    def new_product(cls, product_data):
        """Создает новый товар из словаря с параметрами"""
        return cls(
            product_data["name"],
            product_data["description"],
            product_data["price"],
            product_data["quantity"],
        )

    @property
    def price(self):
        """Геттер для цены."""
        return self.__price

    @price.setter
    def price(self, amount):
        """Сеттер для цены. Проверяет, что цена положительная."""
        if amount <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = amount

    def __str__(self):
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """Считает сумму всех товаров в наличии, если типы совпадают."""
        if isinstance(other, Product):
            if type(self) is not type(other):
                raise TypeError("Товары должны быть одного класса.")
            else:
                total_price = (self.price * self.quantity) + (
                    other.price * other.quantity
                )
                return total_price
        else:
            raise TypeError("Можно складывать только объекты класса Product.")

    def get_data(self):
        return {
            "name": self.name,
            "description": self.description,
            "price": self.__price,
            "quantity": self.quantity,
        }


class Smartphone(Product):
    """Представляет категорию класса класса Product,  товара «Смартфон»"""

    def __init__(
        self, name, description, price, quantity, efficiency, model, memory, color
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def get_data(self):
        return f"Название:{self.name}, цена: {self.__price}"


class LawnGrass(Product):
    """Представляет категорию класса класса Product, товара «Трава газонная»"""

    def __init__(
        self, name, description, price, quantity, country, germination_period, color
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def get_data(self):
        return f"Название:{self.name}, цена: {self.__price}"


class Category:
    """Класс представляющий категорию товара."""

    category_count = 0
    product_count = 0

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.__products = []

        if products:
            for product in products:
                self.add_product(product)

        Category.category_count += 1

    def add_product(self, product):
        """Добавляет объект Product в категорию"""
        if issubclass(type(product), Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Можно добавлять только объекты класса Product.")

    @property
    def products(self):
        return self.__products

    def __str__(self):
        """Возвращает строку с названием категории и общим количеством товаров"""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def middle_price(self):
        try:
            total_price = sum(product.price for product in self.__products)
            count = len(self.__products)
            return total_price / count
        except ZeroDivisionError:
            return 0
