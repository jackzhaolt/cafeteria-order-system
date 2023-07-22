import yaml
import os
import sys
import json

MENU_YAML = "cafeMenu.yml"
MENU = {}


def yaml_reader():
    yaml_file = os.path.join(os.path.dirname(__file__), MENU_YAML)
    global MENU  # pylint: disable-global-statement
    MENU = {}
    with open(yaml_file, "r", encoding="utf-8") as steam:
        try:
            MENU = yaml.safe_load(steam)
        except yaml.YAMLError as err:
            print(f"yaml reader failed with error: {err}")


def validateLogin(username, password):
    # TODO Implement validate login page here
    print("username entered :", username)
    print("password entered :", password)
    return True


def getMenuStr():
    menu_path = os.path.join(os.path.dirname(__file__), MENU_YAML)
    yaml_reader(menu_path)
    return MENU


def getMenuData():
    """Generate a big json file in the format of
    data = {
        <category id 1> : {
            name : <category name>,
            items : [
                {
                    id: <dish id>
                    name: <dish name>
                    price: <dish price>
                },
                {
                    id: <dish id 2>
                    name: <dish name>
                    price: <dish price>
                }
            ]
        },
        <category id 2> : ...
    }

    """
    yaml_reader()
    unsorted_data = {}
    sorted_data = {}
    # Categorory id is always in ascending order due to the way listed in yml file
    for category_id, category_name in MENU["Category"].items():
        unsorted_data[category_id] = {"name": category_name, "items": []}
        sorted_data[category_id] = {"name": category_name, "items": []}
    for dish_name in MENU["Menu"]:
        dish_id = MENU["Menu"][dish_name]["id"]
        dish_price = MENU["Menu"][dish_name]["price"]
        dish_dict = {"id": dish_id, "name": dish_name, "price": dish_price}
        # The magic in the key is to round the id to a single int and then convert it back to str
        unsorted_data[str(int(float(dish_id)))]["items"].append(dish_dict)

    # Sort the items based on ids
    for category in unsorted_data:
        sorted_items = sorted(unsorted_data[category]["items"], key=lambda x: x["id"])
        sorted_data[category]["items"] = sorted_items

    return sorted_data


def main():
    yaml_reader()


class Order:
    """
    Assumes GUI passes in a json formatted string
    """

    def __init__(self, order_json) -> None:
        """Initiate an order with a json string containing all required informations

        Args:
            order_json (string): a json string that represents an order in the format of
            {
                dishes: {
                    <section>: {
                        <name>: <num_of_order_per_table>,
                        <name>: <num_of_order_per_table>,
                    },
                    <section>: {
                        <name>: <num_of_order_per_table>,
                        <name>: <num_of_order_per_table>,
                    },
                }
                num_of_table: <num_of_table>
                num_of_guest: <num_of_guest>
                room_id: <room_id>
                meal_type: <meal_type>
                orderID : <orderID>
                orderDate: <orderDate>
            }
        """
        self.order_json = order_json
        self.dishes = self.order_json["dishes"]
        self.num_of_table = self.order_json["num_of_table"]
        self.num_of_guest = self.order_json["num_of_guest"]
        self.room_id = self.order_json["room_id"]
        self.meal_type = self.order_json["meal_type"]
        self.orderID = self.order_json["orderID"]
        self.orderDate = self.order_json["orderDate"]

    def calculate_total_cost_per_table(self) -> float:
        """Calculate and return the total cost per table

        Returns:
            float: return the total cost per table in 2 decimals
        """
        total_cost_per_table = 0.0
        for section in self.dishes:
            for dish in self.dishes[section]:
                cost_per_dish = float(MENU["Menu"][f"{dish}"]["price"])
                total_cost_per_table += cost_per_dish
        return round(total_cost_per_table, 2)

    def generate_confirmation(self) -> str:
        """generate a json string representing the current order

        Returns:
            str: a json string that contains all information regarding the current order
        """

        # Calculate the costs
        total_cost_per_table = self.calculate_total_cost_per_table()
        total_cost = total_cost_per_table * int(self.num_of_table)

        # Add the calculated cost to the order json
        self.order_json["total_cost_per_table"] = total_cost_per_table
        self.order_json["total_cost"] = round(total_cost, 2)
        return self.order_json


if __name__ == "__main__":
    main()
