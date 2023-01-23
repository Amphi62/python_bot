from datetime import datetime

from entity.enums.TableEnum import TableEnum
from service.DatabaseService import DatabaseService
from utility.game import build_instant_gaming_object, build_steam_object


class GameService:
    def __init__(self):
        self.database_service = DatabaseService()

    def add(self, id_user_discord, name_game, instant_gaming_link=None, steam_link=None):
        print('add')
        id_game = self.database_service.insert_into(TableEnum.GAME.value, {
            "name": name_game
        })

        if id_game == -1:
            return False

        # add instant gaming link and infos
        if instant_gaming_link is not None:
            instant_gaming_game = build_instant_gaming_object(instant_gaming_link)
            self.database_service.insert_into(TableEnum.INSTANT_GAMING.value, {
                "game": id_game,
                "default_price": instant_gaming_game.get_default_price(),
                "discount_price": instant_gaming_game.get_reduction_price(),
                "in_stock": instant_gaming_game.get_stock(),
                "date_updated": datetime.now()
            })

        if steam_link is not None:
            steam_game = build_steam_object(steam_link)
            self.database_service.insert_into(TableEnum.STEAM.value, {
                "game": id_game,
                "default_price": steam_game.get_default_price(),
                "discount_price": steam_game.get_reduction_price(),
                "date_updated": datetime.now()
            })

        # add user who add game in the list
        self.database_service.insert_into(TableEnum.USER_ALERT_REDUCTION_GAME.value, {
            "game": id_game,
            "user": id_user_discord
        })

        return True

    def delete_game(self, name_game: str) -> bool:
        return not self.database_service.delete(TableEnum.GAME, [
            ("LOWER(name)", "=", name_game.lower())
        ])

    def get_all_games(self):
        request = """
        SELECT g.name, i.discount_price, i.default_price, i.in_stock, s.discount_price, s.default_price
        FROM game AS g
        INNER JOIN steam AS s ON g.id = s.game
        INNER JOIN instant_gaming AS i ON g.id = i.game
        ORDER BY g.name ASC
        """

        return self.database_service.specific_select_request(request)
