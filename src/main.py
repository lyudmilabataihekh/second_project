class Product:
    """Класс представляющий товар"""
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс представляющий категорию товара"""
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.products = products

        # Подсчет количества категорий
        Category.category_count += 1

        # Подсчет количества товаров
        self.product_count = len(self.products)
        Category.product_count += self.product_count
