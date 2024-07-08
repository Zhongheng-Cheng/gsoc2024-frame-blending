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

    def _str_helper(self, level=-1, prefix=""):
        result = "    " * level + prefix + self.name
        for node in self.inherited_by.values():
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
    
    def count_nodes(self):
        return 1 + sum([subnode.count_nodes() for subnode in self.inherited_by.values()])


class FrameTree():
    def __init__(self):
        self.roots = []
        return
    
    def __str__(self):
        result = ""
        for root in self.roots:
            result += str(root) + '\n\n'
        return result
    
    def find_root(self, node_name):
        for root in self.roots:
            if root.name == node_name:
                return root
        return None
    
    def find_node(self, node_name):
        for root in self.roots:
            result = root.find_node(node_name)
            if result:
                return result
        return None
    
    def append_root(self, root_node, fathers=[]):
        if not fathers:
            self.roots.append(root_node)
        else:
            for father in fathers:
                father_node = FrameNode(name=father)
                father_node.inherited_by[root_node.name] = root_node
                self.roots.append(father_node)
            if root_node in self.roots:
                self.roots.remove(root_node)
        return
    
    def count_roots(self):
        return len(self.roots)
    
    def count_nodes(self):
        return sum([root_node.count_nodes() for root_node in self.roots])
    

tree = FrameTree()
for frame in frames:
    is_node_existing = False
    
    # parse node name and fathers
    with open(f"frame_json/{frame}.json", 'r') as fo:
        data_dict = json.load(fo)
    frame_name = data_dict.get("frame_name").strip()
    node = tree.find_root(frame_name)
    if node:
        is_node_existing = True
    else:
        node = FrameNode(data_dict.get("frame_name").strip())
    inherits_from = data_dict.get("fr_rel").get("Inherits from")
    fathers = [father.strip() for father in inherits_from.split(', ')] if inherits_from else []

# 不在tree中：
#     先看有没有father，如果没有：直接append root
#     再看有没有找到father，如果没有找到：append root with father
#         如果找到：append subnode
# 在tree中（一定是root）：
#     没有father：保持原样
#     有father：找father
#         找到：接到father后，删root
#         没找到：append root with father，删root
        

    # insert node into trees
    if not fathers and not is_node_existing:
        tree.append_root(node)
    elif fathers:
        for father in fathers:
            father_node = tree.find_node(father)
            if father_node:
                father_node.inherited_by[node.name] = node
                if node in tree.roots:
                    tree.roots.remove(node)
            else:
                tree.append_root(node, [father])

print(tree)