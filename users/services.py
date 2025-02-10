import stripe
from config.settings import STRIPE_API_KEY
from forex_python.converter import CurrencyRates


def create_stripe_product(product):
    """
    Создает продукт stripe.
    """
    stripe.api_key = STRIPE_API_KEY
    p = stripe.Product.create(name=product)
    print(f'СОЗДАНИЕ ПРОДУКТА {p}')
    return p


# def convert_rub_to_dollars(amount):
#     """
#     Конвертирует рубли в доллары.
#     """
#     c = CurrencyRates()
#     rate = c.get_rate('RUB', 'USD')
#     return int(amount * rate)


def create_stripe_price(amount, product):
    """
    Создает цену stripe.
    """
    stripe.api_key = STRIPE_API_KEY
    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": product},
    )
    return price


def create_stripe_session(price):
    """
    Создает сессию на оплату в stripe.
    """
    stripe.api_key = STRIPE_API_KEY
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
