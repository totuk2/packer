from pathlib import Path
import pytest
from itertools import combinations_with_replacement
from packer import execute_packing, load_items_types, load_box_types, create_items, create_bins
from py3dbp import Item, Bin, Packer

TEST_FOLDER = Path(__file__).resolve().parent


@pytest.mark.xfail(reason="no validation on Item class")
def test_items_creation_when_dims_negative_or_zero():
    dim_value = [-1, 0, 1]
    number_of_dims = 4
    for item_dims in combinations_with_replacement(dim_value, number_of_dims):
        width, hight, depth, weight = item_dims
        if 0 or -1 in item_dims:
            with pytest.raises(Exception):
                Item('test_item', width, hight, depth, weight)


@pytest.mark.xfail(reason="no validation on Bin class")
def test_bin_creation_when_dims_negative_or_zero():
    dim_value = [-1, 0, 1]
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


def test_bin_get_total_weight():
    bin = Bin('test_bin_1', 15, 15, 15, 15)
    items = [Item('test_item1', 5, 5, 5, 5),
             Item('test_item2', 5, 5, 5, 5)]
    for item in items:
        bin.items.append(item)
    assert bin.get_total_weight() == 10


def test_bin_get_efficacy():
    bin = Bin('test_bin_1', 10, 10, 5, 10)
    items = [Item('test_item1', 5, 5, 5, 5),
             Item('test_item2', 5, 5, 5, 5)]
    for item in items:
        bin.items.append(item)
    assert bin.get_efficacy() == 0.5


def test_bin_get_volume():
    # proper calculations
    bin = Bin('test_bin', 10, 10, 10, 10)
    assert bin.get_volume() == 1000


def test_packer_fills_entire_box():
    # ISSUE: this test does not show the number of bins the items were packed to, but the number of bin types!!!
    items = [Item('test_item1', 5, 5, 5, 5),
             Item('test_item2', 5, 5, 5, 5),
             Item('test_item3', 5, 5, 5, 5),
             Item('test_item4', 5, 5, 5, 5)]
    bins = [Bin('test_bin1', 10, 10, 5, 20)]
    solutions = execute_packing(items, bins, visualize=False, textualize=False)
    bins_used = set(bins[1] for bins in solutions)
    assert len(bins_used) == 1


@pytest.mark.xfail(run=True, reason="packer's fitted_items solution lists [item, bin_type], not specific bin")
def test_packer_respects_bin_constraints():
    items = [Item('test_item1', 5, 5, 5, 5),
             Item('test_item2', 5, 5, 5, 5),
             Item('test_item3', 5, 5, 5, 5),
             Item('test_item4', 5, 5, 5, 5)]
    bins = [Bin('test_bin1', 10, 10, 5, 10)]
    solutions = execute_packing(items, bins, visualize=False, textualize=False)
    bins_used = set(bins[1] for bins in solutions)
    assert len(bins_used) == 2


@pytest.mark.xfail(run=False, reason="Program gets into infinite loop while at least one item is larger than any bin")
def test_packer_rises_exception_on_item_too_large_to_fit():
    bins = [Bin('test_bin1', 1, 1, 1, 1)]
    items = [Item('test_item1', 2, 1, 1, 1),
             Item('test_item2', 1, 2, 1, 1),
             Item('test_item3', 1, 1, 2, 1),
             Item('test_item4', 1, 1, 1, 2)]
    for item in items:
        if item.width == 2 or item.height == 2 or item.depth == 2 or item.weight == 2:
            with pytest.raises(Exception):
                execute_packing([item], bins, visualize=False, textualize=False)


def test_packer_add_bin():
    packer = Packer()
    bin = Bin('test_bin1', 10, 10, 10, 10)
    packer.add_bin(bin)
    assert len(packer.bins) == 1


def test_packer_add_item():
    packer = Packer()
    item = Item('test_item1', 5, 5, 5, 5)
    packer.add_item(item)
    assert len(packer.items) == 1


def test_packer_remove_item():
    packer = Packer()
    item = Item('test_item1', 5, 5, 5, 5)
    packer.add_item(item)
    packer.remove_item(item)
    assert len(packer.items) == 0


@pytest.mark.skip(reason="This test passes, however it is not showing what should. It will show correct results"
                         "when Issue #14 is solved and test test_packer_respects_bin_constraints() passes.")
def test_execute_packing_optimum_volume_results():
    bins = load_box_types(file=f"{TEST_FOLDER}/boxes_test.json")
    items = load_items_types(file=f"{TEST_FOLDER}/items_test.json")
    items_to_fit = create_items(items)
    bin_types = create_bins(bins)
    solution = execute_packing(items_to_fit, bin_types, visualize=False, textualize=False)

    bins_used = set(bins[1] for bins in solution)
    total_volume = 0
    for box in bins_used:
        total_volume += box.get_volume()
    assert total_volume != 640000


def test_packer_items_not_packed_out_of_gauge():
    bins = load_box_types(file=f"{TEST_FOLDER}/boxes_test.json")
    items = load_items_types(file=f"{TEST_FOLDER}/items_test.json")
    items_to_fit = create_items(items)
    bin_types = create_bins(bins)
    solution = execute_packing(items_to_fit, bin_types, visualize=False, textualize=False)

    for item, bin in solution:
        assert item.position[0] + item.get_dimension()[0] <= bin.width
        assert item.position[1] + item.get_dimension()[1] <= bin.height
        assert item.position[2] + item.get_dimension()[2] <= bin.depth
