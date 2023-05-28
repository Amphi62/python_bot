from entity.inventory.Item import Item


class Inventory:
    def __init__(self, name, name_code):
        self.__name = name
        self.__name_code = name_code
        self.__items = []

    def get_name(self):
        return self.__name

    def get_name_code(self):
        return self.__name_code

    def set_name_code(self, name_code):
        self.__name_code = name_code

    def add_item(self, item: Item):
        self.__items.append(item)

    def remove_item(self, name_item: str):
        self.__items = filter(lambda inventory: inventory.get_name_code() != name_item,
                              self.__items)

    def to_string(self):
        result = ""

        for item in self.__items:
            result += f"**{self.__name}** *({self.__name_code})*"
            result += item.to_string()
            result += "\n"
