from decimal import Decimal
from .constants import Axis
import matplotlib.pyplot as plt
from rich import print
from rich.tree import Tree
import json


def rect_intersect(item1, item2, x, y):
    d1 = item1.get_dimension()
    d2 = item2.get_dimension()

    cx1 = item1.position[x] + d1[x]/2
    cy1 = item1.position[y] + d1[y]/2
    cx2 = item2.position[x] + d2[x]/2
    cy2 = item2.position[y] + d2[y]/2

    ix = max(cx1, cx2) - min(cx1, cx2)
    iy = max(cy1, cy2) - min(cy1, cy2)

    return ix < (d1[x]+d2[x])/2 and iy < (d1[y]+d2[y])/2


def intersect(item1, item2):
    return (
        rect_intersect(item1, item2, Axis.WIDTH, Axis.HEIGHT) and
        rect_intersect(item1, item2, Axis.HEIGHT, Axis.DEPTH) and
        rect_intersect(item1, item2, Axis.WIDTH, Axis.DEPTH)
    )


def get_limit_number_of_decimals(number_of_decimals):
    return Decimal('1.{}'.format('0' * number_of_decimals))


def set_to_decimal(value, number_of_decimals):
    number_of_decimals = get_limit_number_of_decimals(number_of_decimals)

    return Decimal(value).quantize(number_of_decimals)


def _plot_cube(bin, ax, x, y, z, dx, dy, dz, color='red', lw=4):
    """ Auxiliary function to plot a cube. code taken somewhere from the web.  """
    xx = [x, x, x+dx, x+dx, x]
    yy = [y, y+dy, y+dy, y, y]
    kwargs = {'alpha': 1, 'color': color, 'lw': lw}
    ax.plot3D(xx, yy, [z]*5, **kwargs)
    ax.plot3D(xx, yy, [z+dz]*5, **kwargs)
    ax.plot3D([x, x], [y, y], [z, z+dz], **kwargs)
    ax.plot3D([x, x], [y+dy, y+dy], [z, z+dz], **kwargs)
    ax.plot3D([x+dx, x+dx], [y+dy, y+dy], [z, z+dz], **kwargs)
    ax.plot3D([x+dx, x+dx], [y, y], [z, z+dz], **kwargs)


def plot_box_and_items(bin, export_img, title=""):
    """ side effective. Plot the Bin and the items it contains. """
    fig = plt.figure()
    ax_glob = plt.axes(projection='3d')
    # . plot scatola
    _plot_cube(bin, ax_glob, 0, 0, 0, float(bin.width), float(bin.height), float(bin.depth))
    # . plot intems in the box
    color_list = ["black", "blue", "magenta", "orange"]
    counter = 0
    for item in bin.items:
        lw = 2
        color = color_list[counter % len(color_list)]
        x, y, z = item.position
        w, h, d = item.get_dimension()
        _plot_cube(bin, ax_glob, float(x), float(y), float(z), float(w), float(h), float(d), color=color, lw=lw)
        counter = counter + 1
    plt.title(title)
    if export_img:
        plt.savefig(f'reports/{bin.name}_{id(bin)}.png', format="png")
    plt.show()


def textualize_results(best_bins):
    tree = Tree("Packing list:", highlight=True)
    for best_bin in best_bins:
        bins_tree = tree.add(f'{best_bin.name}; w:{best_bin.width}; h:{best_bin.height}; d:{best_bin.depth}; '
                             f'packed: {len(best_bin.items)} of {len(best_bin.items + best_bin.unfitted_items)}; '
                             f'{best_bin.efficacy * 100:.2f}% used')
        for item in best_bin.items:
            bins_tree.add(
                f'[blue]{item.name}[/blue] /position/ w:{item.position[0]} x h:{item.position[1]} x '
                f'd:{item.position[2]} x /rotarion/ type: {item.rotation_type}')
    return print(tree)


def visualize_results(best_bins, export_img=False):
    for best_bin in best_bins:
        plot_box_and_items(best_bin, export_img=export_img,
                           title=f'{best_bin.name} | efficacy: {best_bin.efficacy * 100:.2f}%')


def bins_list_to_json(bin_list: list):
    json_body = {}
    for bin in bin_list:
        items = items_list_to_json(bin.items)
        unfitted_items = items_list_to_json(bin.unfitted_items)
        json_result = {"name": bin.name,
                       "width": str(bin.width),
                       "height": str(bin.height),
                       "depth": str(bin.depth),
                       "max_weight": str(bin.max_weight),
                       "items": items,
                       "unfitted_items": unfitted_items,
                       "efficacy": str(bin.efficacy)}
        json_body = json.dumps(json_result)

    return json_body


def items_list_to_json(item_list):
    json_body = {}
    for item in item_list:
        json_result = {"name": item.name,
                       "width": str(item.width),
                       "height": str(item.height),
                       "depth": str(item.depth),
                       "weight": str(item.weight),
                       "rotation_type": str(item.rotation_type),
                       "position": str(item.position)}
        json_body = json.dumps(json_result)

    return json_body
