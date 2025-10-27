import json
import logging
from datetime import datetime

# Global variable
stock_data = {}

def add_Item(item="default", qty=0, logs=None):
    if logs is None:
        logs = []

    if qty <= 0:
        logging.warning("Attempted to add non-positive qty for item: %s", item)
        return
    
    if not isinstance(item, str) or not item.strip():
        logging.error("Invalid or empty item name: %s", repr(item))
        return
    
    if not item:
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append("%s: Added %d of %s" % (str(datetime.now()), qty, item))

def remove_Item(item, qty):
    if not isinstance(item, str) or not item.strip():
        logging.error("Invalid or empty item name: %s", repr(item))
        return
    if not isinstance(qty, int) or qty <= 0:
        logging.error("Invalid quantity type/negative qty for remove: %s", qty)
        return
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]

    except KeyError:
        logging.warning("Item not found in stock: %s", item)

    except TypeError:
        logging.error("Type error while removing item: %s", item)


def get_Qty(item):
    return stock_data.get(item,0)

def load_Data(file="inventory.json"):
    global stock_data
    try:
        with open(file, "r") as f:
            stock_data = json.load(f)
    except FileNotFoundError:
        logging.error("Inventory file not found: %s", file)
        stock_data = {}
    except json.JSONDecodeError:
        logging.error("Inventory file is corrupt: %s", file)
        stock_data = {}
    except Exception as e:
        logging.error("Could not load data: %s", str(e))
        stock_data = {}

def save_Data(file="inventory.json"):
    try:
        with open(file, "w") as f:
            json.dump(stock_data, f) 
    except Exception as e:
        logging.error("Could not save data: %s", str(e))


def print_Data():
    print("Items Report")
    for i in stock_data:
        print(i, "->", stock_data[i])

def check_Low_Items(threshold=5):
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result

def main():
    add_Item("apple", 10)
    add_Item("banana", -2)
    add_Item("ten", 123)  
    remove_Item("apple", 3)
    remove_Item("orange", 1)
    print("Apple stock:", get_Qty("apple"))
    print("Low items:", check_Low_Items())
    save_Data()
    load_Data()
    print_Data()
 

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
