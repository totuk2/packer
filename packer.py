from copy import deepcopy
import json
from py3dbp import Item, Bin, Packer
from rich import print
from rich.tree import Tree
from py3dbp.auxiliary_methods import plotBoxAndItems, textualize_results

def load_box_types(file="boxes.json"):
    """Imports JSON file with definitions of boxes available."""
    try:
        with open(file) as f:
            bins = json.load(f)
    except FileNotFoundError:
        print("File not found.")
        return 1
    return bins
def load_items_types(file="items.json"):
    """Imports items from the basket in JSON format"""
    try:
        with open(file) as f:
            items = json.load(f)
    except FileNotFoundError:
        print("File not found.")
        return 1
    return items
def create_items(items: dict) -> list:
    item_list = []
    for item in items:
        for number in range(items[item]['quantity']):
            item_list.append(Item(
                items[item]['name'],
                items[item]['width'],
                items[item]['hight'],
                items[item]['depth'],
                items[item]['weight']))
    return item_list
def create_bins(bins: dict) -> list:
    bins_list = []
    for bin in bins:
        bins_list.append(Bin(
            bins[bin]['name'],    # Bin(name, width, height, depth, max_weight)
            bins[bin]['width'],
            bins[bin]['hight'],
            bins[bin]['depth'],
            bins[bin]['max_weight']))
    return bins_list
def refresh_items(unfitted_items, packer):
    for item in unfitted_items:
        packer.add_item(item)

def refresh_bin_types(bin_types, packer):
    for bin in bin_types:
        packer.add_bin(bin)
def execute_packing(items_to_fit: list, visualize=True, export_img=False, textualize=True) -> list:
    fitted_items = []   # list of solutions
    if textualize:
        tree = Tree("Packing list:", highlight=True, hide_root=True)
    while items_to_fit:
        packing_efficacy = 0
        packer = Packer()
        refresh_bin_types(bin_types, packer)
        refresh_items(items_to_fit, packer)
        packer.pack(bigger_first=True)
        best_bin = max(packer.bins, key=lambda b: b.efficacy)    # select the best packed bin
        for item in best_bin.items:
            fitted_items.append((item, best_bin))           # add item+bin to solutions
        if textualize:
            textualize_results(tree, best_bin)
        if visualize:
            plotBoxAndItems(best_bin, f'{best_bin.name} | efficacy: {best_bin.efficacy * 100:.2f}%',
                                     export_img=export_img)

        items_to_fit = deepcopy(best_bin.unfitted_items)
        packer.clear_bins()
    print(tree)
    return fitted_items

bins = load_box_types()
items = load_items_types()

unfitted_items = create_items(items)
bin_types = create_bins(bins)

execute_packing(unfitted_items, visualize=False, textualize=True)