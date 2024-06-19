from product.models import SuppliesPetProduct
from home.models import PetFood

CART_SESSION_ID_FOOD = 'cart_food'
CART_SESSION_ID_PRODUCT = 'cart_product'


class CartProduct:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID_PRODUCT)
        if not cart:
            cart = self.session[CART_SESSION_ID_PRODUCT] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = SuppliesPetProduct.objects.filter(id__in=product_ids, is_available=True)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product_name'] = product.title
            cart[str(product.id)]['product_id'] = product.id

        for item in cart.values():
            item['total_price'] = int(item['price']) * int(item['quantity'])
            yield item

    def get_items(self):
        return list(self.__iter__())

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        self.cart[product_id]['quantity'] += quantity
        self.cart[str(product.id)]['product_id'] = product.id
        self._save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self._save()

    def clear(self):
        if CART_SESSION_ID_PRODUCT in self.session:
            del self.session[CART_SESSION_ID_PRODUCT]
        if CART_SESSION_ID_FOOD in self.session:
            del self.session[CART_SESSION_ID_FOOD]
        self._save()

    def _save(self):
        self.session.modified = True


class CartFood:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID_FOOD)
        if not cart:
            cart = self.session[CART_SESSION_ID_FOOD] = {}
        self.cart = cart

    def __iter__(self):
        food_ids = self.cart.keys()
        foods = PetFood.objects.filter(id__in=food_ids, is_available=True)
        cart = self.cart.copy()
        for food in foods:
            cart[str(food.id)]['product_name'] = food.title
            cart[str(food.id)]['product_id'] = food.id

        for item in cart.values():
            item['total_price'] = int(item['price']) * int(item['quantity'])
            yield item

    def get_items(self):
        return list(self.__iter__())

    def add(self, food, quantity):
        product_id = str(food.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(food.price)}
        self.cart[product_id]['quantity'] += quantity
        self._save()

    def remove(self, food):
        product_id = str(food.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self._save()

    def _save(self):
        self.session.modified = True
