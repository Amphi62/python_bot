from enum import Enum


class StockEnum(Enum):
    IN_STOCK = 'En stock'
    OUT_STOCK = 'Hors stock'
    PREORDER = 'Preorder'
