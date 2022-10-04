import pytest
from itertools import combinations_with_replacement
from packer import execute_packing
from py3dbp import *

@pytest.mark.xfail(reason="no validation on Item class")
def test_items_creation_when_dims_negative_or_zero():
    dim_value = [-1, 0 ,1]
    number_of_dims = 4
    for item_dims in combinations_with_replacement(dim_value, number_of_dims):
        width, hight, depth, weight = item_dims
        if 0 or -1 in item_dims:
            with pytest.raises(Exception):
                Item('test_item', width, hight, depth, weight)
        else:
            assert Item('test_item', width, hight, depth, weight) == isinstance(Item)


@pytest.mark.xfail(reason="no validation on Bin class")
def test_bin_creation_when_dims_negative_or_zero():
    dim_value = [-1, 0 ,1]
    number_of_dims = 4
    for bin_dims in combinations_with_replacement(dim_value, number_of_dims):
        if 0 or -1 in bin_dims:
            with pytest.raises(Exception):
                width, hight, depth, max_weight = bin_dims
                Item('test_bin', width, hight, depth, max_weight)


@pytest.mark.xfail(reason="no validation on Item class")
def test_items_creation_when_dims_nan():
    width, hight, depth, weight = ['a', 'b', 'c', 'd']
    with pytest.raises(Exception):
        Item('test_item', width, hight, depth, weight)


@pytest.mark.xfail(reason="no validation on Bin class")
def test_bin_creation_when_dims_nan():
    width, hight, depth, max_weight = ['a', 'b', 'c', 'd']
    with pytest.raises(Exception):
        Item('test_bin', width, hight, depth, max_weight)
        
        
def test_item_get_volume():
    # proper calculations
    item = Item('test_item', 10, 10, 10, 10)
    assert item.get_volume() == 1000
    
    
def test_bin_get_volume():
    # proper calculations
    bin = Bin('test_bin', 10, 10, 10, 10)
    assert bin.get_volume() == 1000
        

def test_packer_fills_entire_box():
    items = [Item('test_item1', 5, 5, 5, 5),
            Item('test_item2', 5, 5, 5, 5),
            Item('test_item3', 5, 5, 5, 5),
            Item('test_item4', 5, 5, 5, 5)]
    bins = [Bin('test_bin1', 10, 10, 5, 20)]
    solutions = execute_packing(items, bins, visualize=False, textualize=False)
    bins_used = set(bins[1] for bins in solutions)
    assert len(bins_used) == 1


@pytest.mark.xfail(run=False, reason="Program gets into infinite loop while unfitted_items != 0")
def test_packer_rises_exception_on_item_too_large_to_fit():
    bins = [Bin('test_bin1', 1, 1, 1, 1)]
    items = [Item('test_item1', 2, 1, 1, 1),
            Item('test_item2', 1, 2, 1, 1),
            Item('test_item3', 1, 1, 2, 1),
            Item('test_item4', 1, 1, 1, 2)]
    for item in items:
        if item.width or item.height or item.depth or item.weight == 2:
            with pytest.raises(Exception) as exinfo:
                execute_packing([item], bins, visualize=False, textualize=False)


def test_bin_remove_item():
    pass


def test_bin_get_efficacy():
    pass


def test_bin_get_total_weight():
    pass


def test_packer_add_bin():
    pass


def test_packer_add_item():
    pass


def test_packer_clear_bins():
    pass
