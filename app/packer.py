from typing import List, Dict
from copy import deepcopy
import json
from .py3dbp import Item, Bin, Packer


def load_box_types(file="boxes.json") -> Dict:
    with open(file) as f:
        bins = json.load(f)
    return bins


def load_items_types(file="items.json") -> Dict:
    with open(file) as f:
        items = json.load(f)
    return items


def create_items(items: Dict) -> List[Item]:
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


def create_bins(bins: Dict) -> List[Bin]:
    bins_list = []
    for bin in bins:
        bins_list.append(Bin(
            bins[bin]['name'],    # Bin(name, width, height, depth, max_weight)
            bins[bin]['width'],
            bins[bin]['hight'],
            bins[bin]['depth'],
            bins[bin]['max_weight']))
    return bins_list


def add_items_to_packer(unfitted_items: List[Item], packer: Packer) -> None:
    for item in unfitted_items:
        packer.add_item(item)


def add_bins_to_packer(bin_types: List[Bin], packer: Packer) -> None:
    for bin in bin_types:
        packer.add_bin(deepcopy(bin))


def get_best_bins(items_to_fit: List[Item], bin_types: List[Bin], bigger_first=True) -> List[Bin]:
    best_bins: List[Bin] = []

    while items_to_fit:
        packer = Packer()
        add_bins_to_packer(bin_types, packer)
        add_items_to_packer(items_to_fit, packer)
        packer.pack(bigger_first=bigger_first)

        best_bin = packer.get_most_filled_bin()
        best_bins.append(best_bin)
        items_to_fit = best_bin.unfitted_items

    return best_bins
