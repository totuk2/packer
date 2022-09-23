import json
from py3dbp import Item, Bin, Packer
from rich import print, inspect


def refresh_box_types(file="boxes.json"):
    """Imports JSON file with definitions of boxes available."""
    try:
        with open(file) as f:
            bins = json.load(f)
    except FileNotFoundError:
        print("File not found.")
        return 1
    return bins


def refresh_items(file="items.json"):
    """Imports items from the basket in JSON format"""
    try:
        with open(file) as f:
            items = json.load(f)
    except FileNotFoundError:
        print("File not found.")
        return 1
    return items


packer = Packer()


# import items from basket and box types
bins = refresh_box_types()
items = refresh_items()

for bin in bins:
    packer.add_bin(  # Bin(name, width, height, depth, max_weight)
        Bin(bins[bin]['name'],
            bins[bin]['width'],
            bins[bin]['hight'],
            bins[bin]['depth'],
            bins[bin]['max_weight']))


# convert basket to Item objects and add to packer instance
for item in items:
    for number in range(items[item]['quantity']):
        packer.add_item(                                    # Item(name, width, height, depth, weight)
            Item(items[item]['name'],
                 items[item]['width'],
                 items[item]['hight'],
                 items[item]['depth'],
                 items[item]['weight']))

fitted_items = []   # list of solutions

# pack until no more unfitted items
unfitted_items = 1
while unfitted_items != 0:
    packing_efficacy = 0

    packer.pack()
    best_bin = max(packer.bins, key=lambda b: b.efficacy)    # select the best packed bin

    # print(best_bin.name, best_bin.efficacy)
    unfitted_items = len(best_bin.unfitted_items)
    best_bin.plotBoxAndItems()
    inspect(best_bin)
    for item in best_bin.items:
        print(item.string())
        fitted_items.append((item, best_bin.name))           # add item+bin to solutions
        packer.remove_item(item)                             # remove from items to be packed and reiterate

    packer.clear_bins()                                     # clear all items in each of the bins