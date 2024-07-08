import os
import json

frame_folder = "frame"
frames = [file[:-4] for file in os.listdir(frame_folder) if file[-4:] == ".xml"]

x_ing_frames = [frame for frame in frames if frame.split("_")[0].endswith("ing")]

class FrameNode(object):
    def __init__(self, name):
        self.name = name
        self.inherited_by = {}
        return
    
    def __str__(self):
        return self._str_helper()
    
    def _sorted_inherit(self):
        return [item[1] for item in sorted(self.inherited_by.items())]

    def _str_helper(self, level=-1, prefix=""):
        result = "    " * level + prefix + self.name
        for node in self._sorted_inherit():
            result += '\n' + node._str_helper(level=level+1, prefix="|-- ")
        return result
    
    def find_node(self, node_name):
        if self.name == node_name:
            return self
        for node in self.inherited_by.values():
            result = node.find_node(node_name)
            if result:
                return result
        return None
    
    def delete(self, node_name):
        self.inhertied_by = {key:val for key, val in self.inherited_by.items() if key != node_name}
        return
    
    def count_nodes(self):
        return 1 + sum([subnode.count_nodes() for subnode in self.inherited_by.values()])
    
    def count_inheritage(self):
        return len(self.inherited_by.keys())
    
class RootFrameNode(FrameNode):
    def __str__(self):
        result = ""
        for node in self._sorted_inherit():
            result += str(node) + '\n\n'
        return result

    def append_root(self, node, fathers=[]):
        if not fathers:
            self.inherited_by[node.name] = node
        else:
            for father in fathers:
                father_node = FrameNode(name=father)
                father_node.inherited_by[node.name] = node
                self.inherited_by[father_node.name] = father_node
            if node in self.inherited_by.values():
                self.delete(node.name)
        return
    

root = RootFrameNode("[root]")
for frame in frames:
    is_node_existing = False
    
    # parse node name and fathers
    with open(f"frame_json/{frame}.json", 'r') as fo:
        data_dict = json.load(fo)
    frame_name = data_dict.get("frame_name").strip()
    if frame_name in root.inherited_by.keys():
        node = root.inherited_by[frame_name]
        is_node_existing = True
    else:
        node = FrameNode(data_dict.get("frame_name").strip())
    inherits_from = data_dict.get("fr_rel").get("Inherits from")
    fathers = [father.strip() for father in inherits_from.split(', ')] if inherits_from else []

    # insert node into trees
    if not fathers and not is_node_existing:
        root.append_root(node)
    elif fathers:
        for father in fathers:
            father_node = root.find_node(father)
            if father_node:
                father_node.inherited_by[node.name] = node
                if node in root.inherited_by.values():
                    root.delete(node.name)
            else:
                root.append_root(node, [father])

with open("tmp_result.txt", 'w') as fo:
    fo.write(str(root))
print(root.find_node("State"))