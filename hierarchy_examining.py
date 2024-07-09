from framenet_hierarchy import analyze_hierarchy
import os
import json

frame_folder = "frame"
frames = [file[:-4] for file in os.listdir(frame_folder) if file[-4:] == ".xml"]
root = analyze_hierarchy(frames)
count = 0

def check_node(node, father_node):
    """
    Checks if a node has correct "Inherited from" and "Is Inherited by" relations.
    """
    global count
    count += 1
    with open(f"frame_json/{node.name}.json", 'r') as fo:
        data_dict = json.load(fo)
    is_inherited_by = data_dict.get("fr_rel").get("Is Inherited by")
    children = [father.strip() for father in is_inherited_by.split(', ')] if is_inherited_by else []
    inherits_from = data_dict.get("fr_rel").get("Inherits from")
    fathers = [father.strip() for father in inherits_from.split(', ')] if inherits_from else []
    if father_node.name == "[root]" and fathers == [] or father_node.name in fathers:
        if sorted(node.inherited_by.keys()) == sorted(children):
            return 1
    return 0


def check_hierarchy(node):
    """
    Recursively check all the son nodes.
    """
    result = 1
    if node.inherited_by == {}:
        return 1
    for son_node in node.inherited_by.values():
        if check_node(son_node, node) and check_hierarchy(son_node):
            result = 1
        else:
            result = 0
    return result


if check_hierarchy(root):
    print(f"Successfully passed {count}/{root.count_nodes() - 1} nodes!") # all the nodes except root node
else:
    print("Failed!")