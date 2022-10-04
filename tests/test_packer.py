import pytest
from py3dbp import *
from catch_2 import *
from itertools import combinations_with_replacement


def test_items_creation_when_dims_negative_or_zero():
    dim_value = [-1, 0 ,1]
    number_of_dims = 4
    for item_dims in combinations_with_replacement(dim_value, number_of_dims):
        if 0 or -1 in item_dims:
            with pytest.raises(Exception):
                width, hight, depth, weight = item_dims
                Item('test_item', width, hight, depth, weight)


def test_bin_creation_when_dims_negative_or_zero():
    dim_value = [-1, 0 ,1]
    number_of_dims = 4
    for bin_dims in combinations_with_replacement(dim_value, number_of_dims):
        if 0 or -1 in bin_dims:
            with pytest.raises(Exception):
                width, hight, depth, max_weight = bin_dims
                Item('test_bin', width, hight, depth, max_weight)


def test_items_creation_when_dims_nan():
    width, hight, depth, weight = ['a', 'b', 'c', 'd']
    with pytest.raises(Exception):
        Item('test_item', width, hight, depth, weight)


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

