from framenet_hierarchy import analyze_hierarchy, frame_relations
import os
import json

def check_node(node, father_node, frame_relation, reverse_order=False):
    """
    Checks if a node has correct father and child relations.
    """
    with open(f"frame_json/{node.name}.json", 'r') as fo:
        data_dict = json.load(fo)
    children = data_dict.get("fr_rel").get(frame_relations[frame_relation][1 if not reverse_order else 0])
    children = [child.strip() for child in children.split(', ')] if children else []
    fathers = data_dict.get("fr_rel").get(frame_relations[frame_relation][0 if not reverse_order else 1])
    fathers = [father.strip() for father in fathers.split(', ')] if fathers else []
    if father_node.name == f"[{frame_relations[frame_relation][1 if not reverse_order else 0]}]" and fathers == [] or father_node.name in fathers:
        if sorted(node.next.keys()) == sorted(children):
            return 1, 
    return 0


def check_hierarchy(node, frame_relation, reverse_order=False):
    """
    Recursively check all the son nodes.
    """
    if node.next == {}:
        return True
    for son_node in node.next.values():
        if not check_node(son_node, node, frame_relation, reverse_order) \
            or not check_hierarchy(son_node, frame_relation, reverse_order):
            return False
    return True


if __name__ == "__main__":
    frame_folder = "frame"
    frames = [file[:-4] for file in os.listdir(frame_folder) if file[-4:] == ".xml"]
    frame_relation = "Inheritance"
    root = analyze_hierarchy(frames, frame_relation)
    if check_hierarchy(root, frame_relation):
        print(f"Successfully passed!")
    else:
        print("Failed!")