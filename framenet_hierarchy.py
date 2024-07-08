import os
import json

class FrameNode(object):
    def __init__(self, name):
        self.name = name
        self.inherited_by = {}
        return
    
    def __str__(self):
        return self._str_helper()
    
    def _sorted_inherit(self):
        return [item[1] for item in sorted(self.inherited_by.items())]
    
    def _str_helper(self, is_head=True, prefix="", is_tail=False):
        """Print the tree structure of the linked list."""
        if is_head:
            result = self.name + '\n'
        else:
            result = prefix + ("└── " if is_tail else "├── ") + self.name + '\n'
        for i, node in enumerate(self._sorted_inherit()):
            if is_head:
                new_prefix = prefix
            else:
                new_prefix = prefix + ("    " if is_tail else "│   ")
            result += node._str_helper(False, new_prefix, i == len(self.inherited_by) - 1)
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
        self.inherited_by = {key:val for key, val in self.inherited_by.items() if key != node_name}
        return
    
    def count_nodes(self):
        return 1 + sum([subnode.count_nodes() for subnode in self.inherited_by.values()])
    
    def count_inheritage(self):
        return len(self.inherited_by.keys())
    
class RootFrameNode(FrameNode):

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


if __name__ == "__main__":
    frame_folder = "frame"
    frames = [file[:-4] for file in os.listdir(frame_folder) if file[-4:] == ".xml"]
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

    # saving result to file
    output_filename = "tmp_result.txt"
    with open(output_filename, 'w') as fo:
        fo.write(str(root))