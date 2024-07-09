import json

# A dictionary mapping frame relations to their verbal descriptors.
frame_relations = {
    "Inheritance": ["Inherits from", "Is Inherited by"],
    "Perspective": ["Perspective on", "Is Perspectivized in"],
    "Usage": ["Uses", "Is Used by"],
    "Subframe": ["Subframe of", "Has Subframe(s)"],
    "Precedes": ["Precedes", "Is Preceded by"],
    "Causation": ["Is Inchoative of", "Is Causative of"]
}

class FrameNode(object):
    """
    Represents a node in a frame hierarchy. Each node corresponds to a frame.
    """

    def __init__(self, name: str):
        """
        Initializes the FrameNode with a specified name.
        :param name: Name of the frame.
        """
        self.name = name
        self.next = {}
        return
    
    def __str__(self):
        """
        Returns the string representation of the node hierarchy.
        """
        return self._str_helper()
    
    def _sorted_next_list(self):
        """
        Helper function to get a list of child nodes sorted by name.
        :return: List of child FrameNodes.
        """
        return [item[1] for item in sorted(self.next.items())]
    
    def _str_helper(self, is_head=True, prefix="", is_tail=False):
        """
        Recursive helper function to generate a string representation of the node hierarchy.
        :param is_head: Indicates if the current node is the root.
        :param prefix: String prefix for each line of the hierarchy.
        :param is_tail: Indicates if the current node is the last child.
        :return: Formatted string representation of the node hierarchy.
        """
        if is_head:
            result = self.name + '\n'
        else:
            result = prefix + ("└── " if is_tail else "├── ") + self.name + '\n'
        for i, node in enumerate(self._sorted_next_list()):
            if is_head:
                new_prefix = prefix
            else:
                new_prefix = prefix + ("    " if is_tail else "│   ")
            result += node._str_helper(False, new_prefix, i == len(self.next) - 1)
        return result
    
    def find(self, node_name: str):
        """
        Finds a node by name within the subtree rooted at the current node.
        :param node_name: Name of the node to find.
        :return: The node if found, None otherwise.
        """
        if self.name == node_name:
            return self
        for node in self.next.values():
            result = node.find(node_name)
            if result:
                return result
        return None
    
    def delete(self, node_name: str):
        """
        Deletes a node by name from the children of the current node.
        :param node_name: Name of the node to delete.
        """
        self.next = {key:val for key, val in self.next.items() if key != node_name}
        return
    
    def count_nodes(self):
        """
        Counts the total number of nodes in the subtree including this node.
        :return: Total number of nodes.
        """
        return 1 + sum([subnode.count_nodes() for subnode in self.next.values()])
    
    def count_inheritage(self):
        """
        Counts the number of immediate child nodes of this node.
        :return: Number of child nodes.
        """
        return len(self.next.keys())
    
class RootFrameNode(FrameNode):
    """
    Specialized FrameNode that acts as the root of a frame hierarchy.
    """

    def append_root(self, node: FrameNode, fathers: list=[]):
        """
        Appends a node to the root or under specified father nodes.
        :param node: FrameNode to append.
        :param fathers: List of father node names under which the node will be appended.
        """
        if not fathers:
            self.next[node.name] = node
        else:
            for father in fathers:
                father_node = FrameNode(name=father)
                father_node.next[node.name] = node
                self.next[father_node.name] = father_node
            if node in self.next.values():
                self.delete(node.name)
        return

def analyze_hierarchy(frames: list, frame_relation: str, reverse_order: bool=False):
    """
    Analyzes and builds the frame hierarchy based on the specified relation.
    :param frames: List of frame names to include in the hierarchy.
    :param frame_relation: The relation type to build the hierarchy.
        Choose from: ["Inheritance", "Perspective", "Usage", "Subframe", "Precedes", "Causation"]
    :param reverse_order: Whether to reverse the order of the relation.
    :return: Root node of the constructed hierarchy.
    """
    assert frame_relation in frame_relations, f"Please enter one of the relations: {", ".join(frame_relations.keys())}"
    root = RootFrameNode(f"[{frame_relation}]")
    for frame in frames:
        is_node_existing = False
        
        # parse node name and fathers
        with open(f"frame_json/{frame}.json", 'r') as fo:
            data_dict = json.load(fo)
        frame_name = data_dict.get("frame_name").strip()
        if frame_name in root.next.keys():
            node = root.next[frame_name]
            is_node_existing = True
        else:
            node = FrameNode(data_dict.get("frame_name").strip())
        fathers = data_dict.get("fr_rel").get(frame_relations[frame_relation][0 if not reverse_order else 1])
        fathers = [father.strip() for father in fathers.split(', ')] if fathers else []

        # insert node into trees
        if not fathers and not is_node_existing:
            root.append_root(node)
        elif fathers:
            for father in fathers:
                father_node = root.find(father)
                if father_node:
                    father_node.next[node.name] = node
                    if node in root.next.values():
                        root.delete(node.name)
                else:
                    root.append_root(node, [father])
    return root

def save_hierarchy_to_file(root, filename):
    """
    Saves the hierarchy to a file.
    :param root: Root node of the hierarchy to save.
    :param filename: Filename to save the hierarchy.
    """
    with open(filename, 'w') as fo:
        fo.write(str(root))
    print(f"Hierarchy has been saved to {filename}!")

if __name__ == "__main__":
    import os
    frame_folder = "frame"
    frames = [file[:-4] for file in os.listdir(frame_folder) if file[-4:] == ".xml"]
    frame_relation = "Inheritance"
    root = analyze_hierarchy(frames, frame_relation)
    save_hierarchy_to_file(root, "tmp_result.txt")