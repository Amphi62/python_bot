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
        return len([inv for inv in self.__list_inventories if inv.getName() == name_inventory]) > 0

    def remove_inventory(self, name_inventory: str) -> None:
        self.__list_inventories = filter(lambda inventory: inventory.getName() != name_inventory,
                                         self.__list_inventories)

    def save_inventory(self):
        with open(self.__path, 'wb') as file:
            pickle.dump(self, file)
