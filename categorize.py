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
        for node in self.inherited_by.values():
            if node.name == node_name:
                return node
        for node in self.inherited_by.values():
            result = node.find_node(node_name)
            if result:
                return result
        return None


class FrameTree():
    def __init__(self):
        self.roots = []
        return
    
    def __str__(self):
        result = ""
        for root in self.roots:
            result += str(root) + '\n\n'
        return result
    
    def find_self(self, node):
        for root in self.roots:
            if root.name == node.name:
                return root
        return None
    
    def find_father(self, father_name):
        for root in self.roots:
            result = root.find_node(father_name)
            if result:
                return result
        return None
    
    def append_root_father(self, root_node, fathers):
        for father in fathers:
            father_node = FrameNode(name=father)
            father_node.inherited_by[root_node.name] = root_node
            self.roots.append(father_node)
        if root_node in self.roots:
            self.roots.remove(root_node)
        return
    

tree = FrameTree()
for frame in ["Intentionally_affect", "Abandonment", "Key", "Artifact", "Installing"]:
    with open(f"frame_json/{frame}.json", 'r') as fo:
        data_dict = json.load(fo)
        node = FrameNode(data_dict.get("frame_name").strip())
        inherits_from = data_dict.get("fr_rel").get("Inherits from")
        fathers = [father.strip() for father in inherits_from.split(', ')] if inherits_from else []
        print(f"node: {node}, fathers: {fathers}")
        self_node = tree.find_self(node)
        if self_node:
            tree.append_root_father(self_node, fathers)
        elif not fathers:
            tree.roots.append(node)
        else:
            for father in fathers:
                father_node = tree.find_father(father)
                if father_node:
                    father_node.inherited_by[node.name] = node
                else:
                    tree.append_root_father(node, [father])
        print(tree)