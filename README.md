3D Bin Packing
====

This project is a fork from Enzo Ruiz implementation of 3D Bin Packing available [here](https://github.com/enzoruiz/3dbinpacking.git) version py3dbp==1.1.2.
Original 3D Bin Packing implementation is based on [this paper](erick_dube_507-034.pdf). The code is based on [gedex](https://github.com/gedex/bp3d) implementation in Go.

## Features
1. Sorting Bins and Items:
    ```[bigger_first=False/True | default=True]``` By default all the bins and items are sorted from the biggest to the smallest, also it can be vice versa, to make the packing in such ordering.
    
2. Item Distribution *Feature is **deprecated** and will be removed as no longer useful*:
    ~~- ```[distribute_items=True]``` From a list of bins and items, put the items in the bins that at least one item be in one bin that can be fitted. That is, distribute all the items in all the bins so that they can be contained.~~
    ~~- ```[distribute_items=False]``` From a list of bins and items, try to put all the items in each bin and in the end it show per bin all the items that was fitted and the items that was not.~~
   
3. Number of decimals:
    ```[number_of_decimals=X]``` Define the limits of decimals of the inputs and the outputs. By default is 3.

4. Visualisation of packed bins:
    ```[visualize=False/True | default=False]``` Plots the items fitted into the bins. 
    ```[export_img=False/True | default=False]``` While ```visualize=True``` it is possible to export the visual configuration of each bin to .png file to separate           folder: reports.
    
5. Textualization of packed bins:
    ```[textualize=True/False | default=False]``` Prints to console the packing list as the tree of bins and items packed into each of the bins.


## Basic Explanation

### 1. Load the bin types and item types
Bin types and items to be fitted are loaded from the JSON files:
1. ```load_box_types(file="boxes.json")``` - will load the bin types that are available to fit the items in. Each bin should be defined in JSON file as below:
```json
{
  "box_type": {
    "name": str,
    "width": float,
    "hight": float,
    "depth": float,
    "max_weight": float}
```

2. ```load_items_types(file="items.json")``` - will load the items details that should be fitted into the bins. It is possible to create multiple items of the same type by defining the `quatity`. Items details should be defined in JSON file as below:
```json
{
  "item_type": {
    "name": str ,
    "quantity": int ,
    "width": float ,
    "hight": float ,
    "depth": float ,
    "weight": float }
}
```


### 2. Create Bins and Items objects from the previously loaded JSON files

- ```create_bins(bins: dict) -> list``` 
   - will create the list of Bin types objects from previously loaded JSON file.
- ```create_items(items: dict) -> list``` 
   - will create the list of Items objects in number specified by ```quantity``` parameter in previously loaded JSON file.

-   Bin and Items have the same creation params:
    - ```
      my_bin = Bin(name, width, height, depth, max_weight)
      my_item = Item(name, width, height, depth, weight)
      ```


### 3. Initialize instance of Packer

- `packer = Packer()`           # PACKER DEFINITION

#### Methods to be used on packers instance:
- `packer.add_bin(my_bin)`      # ADDING BINS TO PACKER
    - my_bin` will be added to packer.bins as one of the types of bins that can be used to pack items. 
    
- `packer.add_item(my_item)`    # ADDING ITEMS TO PACKER
    - my_item will be added to packer.items to be fittedd into the bins
    
- `packer.remove_item(my_item)` # REMOVES ITEM FROM PACKER

- `packer.clear_bins(arg)`      # CLEAR PACKER BINS. 
    - Argument type can take values: "all" (default) | "fitted" | "unfitted" 
    
 - `packer.pack()`              # PACKING - by default (bigger_first=False ~~distribute_items=False,~~ number_of_decimals=3)
    - method tries to fit all Items added to `packer` to all Bins added to `packer`. Calling this function will result in each Bin being filled with as many Item as possible. After calling this method each of the Bin in `packer` instance will hold:
        - `my_bin.items` - the list of fitted items
        - `my_bin.unfitted_items - the list of items that could not have been fitted into this bin


### 4. Use `execute_packing()` function to find the most optimal way of packing all items into available box types. 

- `execute_packing(items_to_fit, bin_types, visualize=False, export_img=False, textualize=False)`
    - items_to_fit: holds the list of Item type objects
    - bin_types: holds the list of Bin type objects
    - visualize=True will present the packing results in the 3D visualisation
    - export_img=True will save the visualistation to separate .png file in /reports 
    - textualize=True will print to console the packing list as the tree of bins and items packed into each of the bins.

- the function workflow is as follow:
    - run the packer.pack() on the initiated items/bins
    - find the bin which was packed in the most effective way (as a % of bin volume utilized by packed items)
    - save this bin and all fitted items to the list of results
    - take all the bins that were not fitted and re-iterate the packer.pack() on those objects 
    - do until there are no unfitted items left

Function will return (item, bin) tuple.


## Usage

```python
from py3dbp import Packer, Bin, Item
from py3dbp import excute_packing

bins = load_box_types()                  # load available bin types from JSON file  <-- 'box' should be refactored to 'bins'
items = load_items_types()               # load the items which needs to be packed from JSON file

items_to_fit = create_items(items)       # create objects to be passed to packer
bin_types = create_bins(bins)            # create bin types to which we will pack the items

execute_packing(items_to_fit, bin_types, visualize=False, textualize=False)     # do the packing
```




## Credit

* https://github.com/bom-d-van/binpacking
* https://github.com/gedex/bp3d
* [Optimizing three-dimensional bin packing through simulation](erick_dube_507-034.pdf)

## License

[MIT](./LICENSE)
