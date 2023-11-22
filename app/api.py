from fastapi import FastAPI
from .models import Bin, Item
from typing import List, Dict


from .packer import get_best_bins, create_bins, create_items
from .py3dbp.auxiliary_methods import dump_binlist_to_json

app = FastAPI()


@app.post("/packer")
def pack(items: Dict, bins: Dict):
    bin_types: List[Bin] = create_bins(bins)
    items_to_pack: List[Item] = create_items(items)
    best_packed_bins: List[Bin] = get_best_bins(items_to_pack, bin_types)
    json_body: Dict = dump_binlist_to_json(best_packed_bins)

    return json_body
