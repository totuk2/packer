from typing import List
from copy import deepcopy
import json
from py3dbp import Item, Bin, Packer
from rich import print
from rich.tree import Tree
from py3dbp.auxiliary_methods import plot_box_and_items, textualize_results


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


def add_bins_to_packer(bin_types, packer):
    for bin in bin_types:
        packer.add_bin(deepcopy(bin))


def get_best_bins(items_to_fit: list, bin_types: list, visualize=False, export_img=False, textualize=False) -> List[Bin]:
    best_bins: List[Bin] = []
    tree = Tree("Packing list:", highlight=True, hide_root=True)
    while items_to_fit:
        packer = Packer()
        add_bins_to_packer(bin_types, packer)
        refresh_items(items_to_fit, packer)
        packer.pack(bigger_first=True)
        best_bin = max(packer.bins, key=lambda b: b.efficacy)  # select the best packed bin and copy it
        best_bins.append(best_bin)
        if textualize:
            textualize_results(tree, best_bin)
        if visualize:
            plot_box_and_items(best_bin, export_img=export_img,
                               title=f'{best_bin.name} | efficacy: {best_bin.efficacy * 100:.2f}%')
        else:
            if export_img:
                raise Exception("Export of image can be done only when visualize=True")

        items_to_fit = best_bin.unfitted_items
    print(tree)
    return best_bins


# bins = load_box_types()
# items = load_items_types()
# items_to_fit = create_items(items)
# bin_types = create_bins(bins)
# get_best_bins(items_to_fit, bin_types, visualize=False, textualize=False)
