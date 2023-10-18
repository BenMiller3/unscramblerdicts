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
        if self.children:
            output["c"] = {k: v.to_dict() for k, v in self.children.items()}
        return output

def build_dawg_from_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        root = DAWGNode()
        for word_list in data.values():
            for word in word_list:
                root.insert(word)
    return root.to_dict()

def main():
    files = ["words-es.json", "words-fr.json", "words-gb.json", "words-it.json", "words-no.json"]
    for filename in files:
        dawg = build_dawg_from_json_file(filename)
        output_filename = filename.replace('words', 'dawg')
        with open(output_filename, 'w', encoding='utf-8') as out_file:
            json.dump(dawg, out_file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()

