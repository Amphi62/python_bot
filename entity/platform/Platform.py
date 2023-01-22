from datetime import date

from entity.enums.StockEnum import StockEnum


class Platform:
    def __init__(self, link, default_price, reduction_price=None, stock=StockEnum.IN_STOCK):
        self.link = link
        self.default_price = default_price
        self.reduction_price = reduction_price
        self.stock = stock
        self.updated_date = date.today()

    def get_default_price(self):
        return self.default_price

    def get_reduction_price(self):
        return self.reduction_price

    def get_stock(self):
        return self.stock.value
