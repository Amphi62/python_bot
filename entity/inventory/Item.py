from entity.inventory.Resource import Resource


class Item:
    def __init__(self, name, name_code, description):
        self.__name = name
        self.__name_code = name_code
        self.__description = description
        self.__resources = []
        self.__success = False

    def get_name_code(self) -> str:
        return self.__name_code

    def set_name_code(self, name_code: str) -> None:
        self.__name_code = name_code

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_description(self) -> str:
        return self.__description

    def set_description(self, description: str) -> None:
        self.__description = description

    def add_resource(self, resource: Resource) -> None:
        self.__resources.append(resource)

    def remove_resources(self, number: int) -> None:
        self.__resources.pop(number)

    def show_resources(self) -> str:
        result = ""

        for i in range(len(self.__resources)):
            result += f"{self.__resources[i].get_link} **({i})**\n"

        result += "Tapez \"!del_resource name_inventory name_item number_resource\" pour supprimer une ressource."
        return result

    def set_success(self, success: bool) -> None:
        self.__success = success

    def to_string(self, show_success) -> str:
        result = f"**Nom :** {self.__name}"
        if show_success and self.__success:
            result += " **(fait)**"
        result += "\n"
        result += f"**Description :** {self.__description}\n"

        for resource in self.__resources:
            result += f"\n{resource.get_link()}"

        return result
