import json
from py3dbp.main import Item, Bin, Packer
from rich import print, inspect
from rich.console import Console
from rich.tree import Tree


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


console = Console(record=True, color_system="windows")
packer = Packer()
tree = Tree("Packed items", highlight=True)

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

packer.pack()

# best_bin = max(packer.bins, key=lambda b: b.efficacy)    # select the best packed bin

for b in packer.bins:
    # console.print(inspect(b, title=f'[red bold] Inspecting {b.name} [/red bold', sort=False))
    bins_tree = tree.add(f'{b.name} in {b}; w:{b.width}; h:{b.height}; d:{b.depth}; '
                         f'packed: {len(b.items)} of {len(b.items+b.unfitted_items)}')

    for item in b.items:
        bins_tree.add(f'[blue]{item.name}[/blue] in {item} /position/ w:{item.position[0]}-{item.position[0]+item.width} x '
                      f'h:{item.position[1]}-{item.position[1]+item.height} x '
                      f'd:{item.position[2]}-{item.position[2]+item.depth}')
        # console.print(inspect(item, title=f'[red bold] Inspecting {item.name} {item}: [/red bold]', sort=False))
    b.plot_box_and_items(f'{b.name}, efficacy:{b.get_efficacy() * 100:.2f}%', )

console.print(tree)
console.save_html('reports/packing_inspect.html')