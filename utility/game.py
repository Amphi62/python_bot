from requests_html import HTMLSession

from entity.enums.StockEnum import StockEnum
from entity.platform.InstantGamingPlatform import InstantGamingPlatform
from entity.platform.SteamPlatform import SteamPlatform


def build_instant_gaming_object(instant_gaming_link):
    session = HTMLSession()
    response = session.get(instant_gaming_link)

    game = response.html.find(".panel.item.wide", first=True)
    discount = game.find("div.amount", first=True)
    sub_infos = game.find("div.subinfos", first=True)

    stock = sub_infos.find("div.stock,div.nostock", first=True)
    in_stock = StockEnum.IN_STOCK

    if stock is None:
        in_stock = StockEnum.PREORDER
    elif stock.text != 'En stock':
        in_stock = StockEnum.OUT_STOCK

    default_price = discount.find("div.retail", first=True).text
    discount_price = discount.find("div.total", first=True).text

    session.close()

    return InstantGamingPlatform(instant_gaming_link, default_price, discount_price, in_stock)


def build_steam_object(steam_link):
    session = HTMLSession()
    response = session.get(steam_link)

    game = response.html.find(".game_area_purchase_game_wrapper", first=True)

    discount = game.find(".discount_block.game_purchase_discount", first=True)

    if discount is None:
        default_price = game.find(".game_purchase_price.price", first=True).text
        discount_price = None
    else:
        default_price = discount.find(".discount_original_price", first=True).text
        discount_price = discount.find(".discount_final_price", first=True).text

    session.close()

    return SteamPlatform(steam_link, default_price, discount_price, StockEnum.IN_STOCK)


def check_link_game_exist(link_game):
    session = HTMLSession()
    status = session.get(link_game).status_code
    session.close()
    return status == 200
