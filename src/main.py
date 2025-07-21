class Product:
    """Класс представляющий товар"""

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

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
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Можно добавлять только объекты класса Product.")

    @property
    def products(self):
        """Возвращает список товаров в виде строк (для совместимости с вашим кодом)"""
        return [
            f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            for product in self.__products
        ]
