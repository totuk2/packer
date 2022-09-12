import json
from py3dbp import Item, Bin, Packer

packer = Packer()

# // refresh_ functions can be cached so the objects are created only when the change is made???

def refresh_box_types(file="boxes.json"):
    """"""
    try:
        with open(file) as f:
            bins = json.load(f)
    except FileNotFoundError:
        print("File not found.")
        return 1

    for bin in bins:
        packer.add_bin(             # Bin(name, width, height, depth, max_weight)
            Bin(bins[bin]['name'],
                bins[bin]['width'],
                bins[bin]['hight'],
                bins[bin]['depth'],
                bins[bin]['max_weight']))
    return 0

def refresh_items(file="items.json"):
    """"""

    try:
        with open(file) as f:
            items = json.load(f)
    except FileNotFoundError:
        print("File not found.")

    for item in items:
        for number in range(items[item]['quantity']):
            packer.add_item(                # Item(name, width, height, depth, weight)
                Item(items[item]['name'],
                    items[item]['width'],
                    items[item]['hight'],
                    items[item]['depth'],
                    items[item]['weight']))


refresh_box_types()
refresh_items()
packer.pack()

bin_results = []

for b in packer.bins:
    vol = 0
    for item in b.items:
    print(f'bin {b.name} volume efficacy  {b.get_efficacy()*100:.2f}%')


# Step 2:
# take the unfitted items from the bin with highest efficacy
# iterate