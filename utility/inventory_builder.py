from entity.inventory.ListInventory import ListInventory
import pickle


def build_inventory(name_path: str) -> ListInventory:
    with open(name_path, 'rb') as file:
        return pickle.load(file)