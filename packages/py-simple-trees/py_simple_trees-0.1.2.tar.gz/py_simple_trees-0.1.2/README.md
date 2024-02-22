# py-simple-trees

<p align="center">
    <em>This package is a implementation collection of tree data structures.</em>
</p>

<p align="center">
    <a href="https://github.com/lpthong90/py-simple-trees/actions?query=workflow%3ATest" target="_blank">
        <img src="https://github.com/lpthong90/py-simple-trees/workflows/Test/badge.svg" alt="Test">
    </a>
    <a href="https://github.com/lpthong90/py-simple-trees/actions?query=workflow%3APublish" target="_blank">
        <img src="https://github.com/lpthong90/py-simple-trees/workflows/Publish/badge.svg" alt="Publish">
    </a>
    <a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/lpthong90/py-simple-trees" target="_blank">
        <img src="https://coverage-badge.samuelcolvin.workers.dev/lpthong90/py-simple-trees.svg" alt="Coverage">
    </a>
    <a href="https://pypi.org/project/py-simple-trees" target="_blank">
        <img src="https://img.shields.io/pypi/v/py-simple-trees?color=%2334D058&label=pypi%20package" alt="Package version">
    </a>
    <a href="https://pypi.org/project/py-simple-trees" target="_blank">
        <img alt="Downloads" src="https://img.shields.io/pypi/dm/py-simple-trees?color=%2334D058" />
    </a>
</p>
<p align="center">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/py-simple-trees">
</p>


---

**Documentation**: <a href="https://lpthong90.dev/py-simple-trees" target="_blank">https://lpthong90.dev/py-simple-trees</a>

**Source  Code**: <a href="https://github.com/lpthong90/py-simple-trees" target="_blank">https://github.com/lpthong90/py-simple-trees</a>

---

This package is a implementation collection of tree data structures.

## Installation

<div class="termy">

```console

$ pip install py-simple-trees

---> 100%

Successfully installed py-simple-trees
```

</div>

## Tree Types
- Binary Tree
- Binary Search Tree (BST)
- AVL Tree

## Basic Usage

```Python
from py_simple_trees import AVLTree

if __name__ == "__main__":
    tree = AVLTree()

    tree.insert(1, 1)
    tree.insert(2, 2)
    tree.insert(3, 3)
    tree.insert(4, 4)
    tree.insert(5, 5)
    tree.insert(6, 6)
    tree.insert(7, 7)

    tree.print()
```

Output
```
4 --L--> 2
4 --R--> 6
2 --L--> 1
2 --R--> 3
6 --L--> 5
6 --R--> 7
```






## License

This project is licensed under the terms of the [MIT license](https://github.com/lpthong90/py-simple-trees/blob/main/LICENSE).
