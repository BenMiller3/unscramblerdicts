import json

class DAWGNode:
    def __init__(self):
        self.children = {}
        self.isWord = False

    def insert(self, word):
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = DAWGNode()
            node = node.children[char]
        node.isWord = True

    def to_dict(self):
        output = {}
        if self.isWord:
            output["i"] = True
        else:
            output["i"] = False
        if self.children:
            output["c"] = {k: v.to_dict() for k, v in self.children.items()}
        return output

def dawg_node_key(node):
    """Converts a node to a unique key string for easier comparison."""
    if not node.children:
        return "1"
    key = "".join(sorted(node.children))
    return key + "".join([dawg_node_key(node.children[k]) for k in sorted(node.children.keys())])

def trie_to_dawg(trie_node, known_nodes):
    """Recursively reduces the trie into a DAWG."""
    key = dawg_node_key(trie_node)
    if key in known_nodes:
        return known_nodes[key]

    for child in trie_node.children:
        trie_node.children[child] = trie_to_dawg(trie_node.children[child], known_nodes)

    known_nodes[key] = trie_node
    return trie_node

def build_dawg_from_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        root = DAWGNode()
        for word_list in data.values():
            for word in word_list:
                root.insert(word)
        
        # Convert the trie to DAWG after inserting all words
        known_nodes = {}
        dawg_root = trie_to_dawg(root, known_nodes)
        return dawg_root.to_dict()

def main():
    files = ["words-es.json", "words-fr.json", "words-gb.json", "words-it.json", "words-no.json"]
    for filename in files:
        dawg = build_dawg_from_json_file(filename)
        output_filename = filename.replace('words', 'dawg')
        with open(output_filename, 'w', encoding='utf-8') as out_file:
            json.dump(dawg, out_file, ensure_ascii=False)

if __name__ == "__main__":
	main()

