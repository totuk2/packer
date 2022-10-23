from fastapi import FastAPI
from models import Bin, Item
from typing import List


from packer import get_best_bins, create_bins, create_items
from py3dbp.auxiliary_methods import bins_list_to_json

app = FastAPI()


@app.post("/packer")
def pack(items: dict, bins: dict):
    bin_types = create_bins(bins)
    items_to_pack = create_items(items)
    best_packed_bins = get_best_bins(items_to_pack, bin_types)
    json = bins_list_to_json(best_packed_bins)

    return json
