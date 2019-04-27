#!/usr/bin/env python
"""Python trie implementation. Built as a learning exercise. Should have
been built with C to have a smaller memory footprint. Moved to https://gist.github.com/chiedojohn/2ca4b83a3cd8913e1238"""

__author__ = "Chiedo John"
__copyright__ = "Copyright 2015, Chiedo, Inc."
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Chiedo John"
__email__ = "chiedo@chie.do"


class Node:
    """Node for Python Trie Implementation"""

    def __init__(self):
        self.word = None
        self.nodes = {}  # dict of nodes

    def __get_all__(self):
        """Get all of the words in the trie"""
        x = []

        for key, node in self.nodes.items():
            if(node.word is not None):
                x.append(node.word)

            x += node.__get_all__()

        return x

    def __str__(self):
        return self.word

    def __insert__(self, word, string_pos=0):
        """Add a word to the node in a Trie"""
        current_letter = word[string_pos]

        # Create the Node if it does not already exist
        if current_letter not in self.nodes:
            self.nodes[current_letter] = Node()

        if(string_pos + 1 == len(word)):
            self.nodes[current_letter].word = word
        else:
            self.nodes[current_letter].__insert__(word, string_pos + 1)
        return True

    def __get_all_with_prefix__(self, prefix, string_pos):
        """Return all nodes in a trie with a given prefix or that are equal to the prefix"""
        x = []

        for key, node in self.nodes.items():
            # If the current character of the prefix is one of the nodes or we have
            # already satisfied the prefix match, then get the matches
            if(string_pos >= len(prefix) or key == prefix[string_pos]):
                if(node.word is not None):
                    x.append(node.word)

                if(node.nodes != {}):
                    if(string_pos + 1 <= len(prefix)):
                        x += node.__get_all_with_prefix__(
                            prefix, string_pos + 1)
                    else:
                        x += node.__get_all_with_prefix__(prefix, string_pos)

        return x


class Trie:
    """Trie Python Implementation"""

    def __init__(self):
        self.root = Node()

    def insert(self, word):
        self.root.__insert__(word)

    def get_all(self):
        return self.root.__get_all__()

    def get_all_with_prefix(self, prefix, string_pos=0):
        return self.root.__get_all_with_prefix__(prefix, string_pos)

