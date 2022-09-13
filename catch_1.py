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

packer.pack(distribute_items=True)

for b in packer.bins:
    print(":::::::::::", b.string())

    print("FITTED ITEMS:")
    vol = 0
    for item in b.items:
        print("====> ", item.string())
        vol += item.get_volume()
    print(f"Usage volume: {vol}, which is {vol / b.get_volume() *100:.2f}%")
    print(f"Usage weight: {b.get_total_weight()} / {b.max_weight}, which is {b.get_total_weight()/ b.max_weight * 100:.2f}%")

    # print("\nUNFITTED ITEMS:")
    # vol = 0
    # for item in b.unfitted_items:
    #     vol += item.get_volume()
    #     print("====> ", item.string())
    # print(f"Unfitted volume: {vol}")
