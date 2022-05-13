from entity.inventory.Inventory import Inventory
import pickle


class ListInventory:
    def __init__(self, id_author: int, path: str):
        self.__list_inventories = []
        self.__id_author = id_author
        self.__path = path

    def add_inventory(self, new_inventory: Inventory) -> None:
        self.__list_inventories.append(new_inventory)

    def contains_inventory(self, name_inventory: str) -> bool:
        return len([inv for inv in self.__list_inventories if inv.get_name_code() == name_inventory]) > 0

    def remove_inventory(self, name_inventory: str) -> None:
        self.__list_inventories = filter(lambda inventory: inventory.get_name_code() != name_inventory,
                                         self.__list_inventories)

    def save_inventory(self):
        with open(self.__path, 'wb') as file:
            pickle.dump(self, file)

    def get_inventories(self):
        result = "**Vos inventaires :**\n\n"

        for index, inventory in enumerate(self.__list_inventories):
            result += f"**{index}-** {inventory.get_name()} *({inventory.get_name_code()})*\n"

        return result[:-1]

    def list_inventories_is_empty(self):
        return len(self.__list_inventories) == 0
