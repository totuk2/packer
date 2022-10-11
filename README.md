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
    ```[visualize=False/True | default=True]``` Plots the items fitted into the bins. 
    ```[export_img=False/True | default=False]``` While ```visualize=True``` it is possible to export the visual configuration of each bin to .png file to separate           folder: reports.
    
5. Textualization of packed bins:
    ```[textualize=True | default=True]``` Prints to console the packing list as the tree of bins and items packed into each of the bins.


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

```create_bins(bins: dict) -> list``` - will create the list of Bin types objects from previously loaded JSON file.
```create_items(items: dict) -> list``` - will create the list of Items objects in number specified by ```quantity``` parameter in previously loaded JSON file.

Bin and Items have the same creation params:
```
my_bin = Bin(name, width, height, depth, max_weight)
my_item = Item(name, width, height, depth, weight)
```


Packer have three main functions:
```
packer = Packer()           # PACKER DEFINITION

packer.add_bin(my_bin)      # ADDING BINS TO PACKER
packer.add_item(my_item)    # ADDING ITEMS TO PACKER

packer.pack()               # PACKING - by default (bigger_first=False, distribute_items=False, number_of_decimals=3)
```

After packing:
```
packer.bins                 # GET ALL BINS OF PACKER
my_bin.items                # GET ALL FITTED ITEMS IN EACH BIN
my_bin.unfitted_items       # GET ALL UNFITTED ITEMS IN EACH BIN
```


## Usage

```python
from py3dbp import Packer, Bin, Item
from py3dbp import excute_packing

```




## Credit

* https://github.com/bom-d-van/binpacking
* https://github.com/gedex/bp3d
* [Optimizing three-dimensional bin packing through simulation](erick_dube_507-034.pdf)

## License

[MIT](./LICENSE)
