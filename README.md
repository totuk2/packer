3D Bin Packing
====

This project is a fork from Enzo Ruiz implementation of 3D Bin Packing available [here](https://github.com/enzoruiz/3dbinpacking.git) version py3dbp==1.1.2.
Original 3D Bin Packing implementation is based on [this paper](erick_dube_507-034.pdf). The code is based on [gedex](https://github.com/gedex/bp3d) implementation in Go.

## Features
1. Sorting Bins and Items:
    ```[bigger_first=False/True | default=True]``` By default all the bins and items are sorted from the biggest to the smallest, also it can be vice versa, to make the packing in such ordering.
   
2. Number of decimals:
    ```[number_of_decimals=X]``` Define the limits of decimals of the inputs and the outputs. By default is 3.

3. Visualisation of packed bins:
    ```visualize_results(best_bins: List[Bin], export_img=False)``` Plots the items fitted into the bins. 
    ```[export_img=False/True | default=False]``` - it is possible to export the visual configuration of each bin to .png file to separate folder: reports.
    
4. Textualization of packed bins:
    ```textualize_results(best_bins: List[Bin])``` Prints to console the packing list as the tree of bins and items packed into each of the bins.

5. API returning best packed bins in JSON format

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

- ```python
  packer = Packer()              # Packer definition
  ```

#### Methods to be used on packers instance:
- ```python
  packer.add_bin(my_bin)         # Adding Bins to packer instance
  ```
    - `my_bin` will be added to packer.bins as one of the types of bins that can be used to pack items. 
    
- ```python
  packer.add_item(my_item)       # Adding Items to packer instance 
  ```
    - `my_item` will be added to packer.items to be fittedd into the bins
    
- ```python
  packer.remove_item(my_item)    # Removes Item from packer instance
  ```
    
 - ```python
   packer.pack()                 # Analyze the Items fitting each Bin  - by default (bigger_first=False ~~distribute_items=False,~~ number_of_decimals=3)
   ```
    - method tries to fit all Items added to `packer` to all Bins added to `packer`. Calling this function will result in each Bin being filled with as many Item as possible. After calling this method each of the Bin in `packer` instance will hold:
        - `my_bin.items` - the list of fitted items
        - `my_bin.unfitted_items - the list of items that could not have been fitted into this bin


### 4. Use `execute_packing()` function to find the most optimal way of packing all items into available box types. 

- `execute_packing(items_to_fit, bin_types, visualize=False, export_img=False, textualize=False)`
    - items_to_fit: holds the list of Item type objects
    - bin_types: holds the list of Bin type objects

- the function workflow is as follow:
    - run the packer.pack() on the initiated items/bins
    - find the bin which was packed in the most effective way (as a % of bin volume utilized by packed items)
    - save this bin and all fitted items to the list of results
    - take all the bins that were not fitted and re-iterate the packer.pack() on those objects 
    - do until there are no unfitted items left

Function will return best_packed_bins list.


## Usage

```python
from py3dbp import Packer, Bin, Item
from py3dbp import execute_packing

bins = load_box_types()                  # load available bin types from JSON file  <-- 'box' should be refactored to 'bins'
items = load_items_types()               # load the items which needs to be packed from JSON file

items_to_fit = create_items(items)       # create objects to be passed to packer
bin_types = create_bins(bins)            # create bin types to which we will pack the items

execute_packing(items_to_fit: List[Item], bin_types: List[Bin])     # do the packing
```




## Credit

* https://github.com/bom-d-van/binpacking
* https://github.com/gedex/bp3d
* [Optimizing three-dimensional bin packing through simulation](erick_dube_507-034.pdf)

## License

[MIT](./LICENSE)
