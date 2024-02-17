from typing import Any

import ast_comments as ast  # type: ignore
import black
import isort
from pathier import Pathier, Pathish

from tomfoolery import utilities

root = Pathier(__file__).parent


class TomFoolery:
    def __init__(self, module: ast.Module | None = None, recursive: bool = True):
        """If no `module` is given, an empty new one will be created.

        When generating a `dataclass` from a dictionary,
        if `recursive` is `True` then values that are also dictionaries will have a `dataclass` generated.

        The annotation for that field in the original `dataclass` will be typed as an instance of the second `dataclass`.

        If `recursive` is `False`, values that are dictionaries will be typed as such.

        i.e.
        from a file named "chonker.toml"
        >>> {
        >>>  "name": "yeehaw",
        >>>  "stats": {
        >>>      "average": 77.54,
        >>>      "max": 94.22,
        >>>      "min": 22.76
        >>>  }
        >>> }

        With recursive == True
        >>> @dataclass
        >>> class Stats:
        >>>     average: float
        >>>     max: float
        >>>     min: float
        >>>
        >>> @dataclass
        >>> class Chonker:
        >>>     name: str
        >>>     stats: Stats

        With recursive == False
        >>> @dataclass
        >>> class Chonker:
        >>>     name: str
        >>>     stats: dict
        """
        self.module: ast.Module = module or ast.Module([], [])
        self.recursive = recursive

    @property
    def class_names(self) -> list[str]:
        """List of class names in `self.module.body`."""
        return [node.name for node in self.module.body if type(node) == ast.ClassDef]

    @property
    def source(self) -> str:
        """Returns the source code this object represents."""
        try:
            return self.format_str(ast.unparse(self.module))
        except Exception as e:
            return ast.unparse(self.module)

    def format_str(self, code: str) -> str:
        """Sort imports and format with `black`."""
        return black.format_str(isort.api.sort_code_string(code), mode=black.Mode())  # type: ignore

    # Seat |===================================== Import Nodes =====================================|

    @property
    def dacite_import_node(self) -> ast.Import:
        return ast.Import([ast.alias("dacite")])

    @property
    def dataclass_import_node(self) -> ast.ImportFrom:
        return ast.ImportFrom(
            "dataclasses", [ast.alias("dataclass"), ast.alias("asdict")], 0
        )

    @property
    def import_nodes(self) -> list[ast.Import | ast.ImportFrom]:
        return [
            self.dacite_import_node,
            self.dataclass_import_node,
            self.pathier_import_node,
            self.typing_extensions_import_node,
        ]

    @property
    def pathier_import_node(self) -> ast.ImportFrom:
        return ast.ImportFrom(
            "pathier", [ast.alias("Pathier"), ast.alias("Pathish")], 0
        )

    @property
    def typing_extensions_import_node(self) -> ast.ImportFrom:
        return ast.ImportFrom("typing_extensions", [ast.alias("Self")])

    # Seat |======================================== Nodes ========================================|

    @property
    def dataclass_node(self) -> ast.Name:
        """A node representing `@dataclass`."""
        return ast.Name("dataclass", ast.Load())

    @property
    def dump_node(self) -> ast.FunctionDef:
        """The dumping function for the generated `dataclass`."""
        dump = self.nodes_from_file(root / "_dump.py")[0]
        return dump if isinstance(dump, ast.FunctionDef) else ast.FunctionDef()

    @property
    def load_node(self) -> ast.FunctionDef:
        """The loading function for the generated `dataclass`."""
        load = self.nodes_from_file(root / "_load.py")[0]
        return load if isinstance(load, ast.FunctionDef) else ast.FunctionDef()

    def add_dataclass(self, dataclass: ast.ClassDef):
        """Add or merge `dataclass` into `self.module.body`."""
        if dataclass.name not in self.class_names:
            self.module.body.append(dataclass)
        else:
            classdex = self.class_index(dataclass.name)
            self.module.body[classdex] = self.merge_dataclasses(self.module.body[classdex], dataclass)  # type: ignore

    def class_index(self, class_name: str) -> int:
        """Return the `self.module.body` index for a class with `class_name`."""
        for i, node in enumerate(self.module.body):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                return i
        return len(self.module.body)

    def fix_order(self):
        """Reorder `self.module.body` so that definitions preceede instances.

        i.e. A newly added class is defined before another class creates an instance."""
        new_body: list[ast.stmt] = []
        for node in self.module.body:
            if isinstance(node, ast.ClassDef):
                placed = False
                for i, new_node in enumerate(new_body):
                    if node.name in ast.unparse(new_node):
                        new_body.insert(i, node)
                        placed = True
                        break
                if not placed:
                    new_body.append(node)
            else:
                new_body.append(node)
        self.module.body = new_body

    def last_annassign_index(self, node: ast.ClassDef) -> int:
        """Return the `node.body` index of the last annotated assignment node.
        Assumes all annotated assignments are sequential and the first elements of `node`.
        """
        for i, child in enumerate(node.body):
            if not isinstance(child, ast.AnnAssign):
                return i - 1
        return len(node.body)

    def merge_dataclasses(
        self, class1: ast.ClassDef, class2: ast.ClassDef
    ) -> ast.ClassDef:
        """Add annotated assignments and functions from `class2` to `class1` and return the result."""
        funcs = [node.name for node in class1.body if isinstance(node, ast.FunctionDef)]
        assigns = [
            node.target.id
            for node in class1.body
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
        ]
        for node in class2.body:
            if isinstance(node, ast.FunctionDef) and node.name not in funcs:
                class1.body.append(node)
            elif (
                isinstance(node, ast.AnnAssign)
                and isinstance(node.target, ast.Name)
                and (node.target.id not in assigns)
            ):
                class1.body.insert(self.last_annassign_index(class1) + 1, node)
        return class1

    def nodes_from_file(self, file: Pathish) -> list[ast.stmt]:
        """Return ast-parsed module body from `file`."""
        node = ast.parse(Pathier(file).read_text())  # type: ignore
        return node.body if isinstance(node, ast.Module) else []

    # Seat |======================================= Builders =======================================|

    def annotated_assignments_from_dict(
        self, data: dict[str, Any]
    ) -> list[ast.AnnAssign]:
        """Return a list of annotated assignment nodes built from `data`.

        If `recursive` is `True` (the default),
        any values in `data` that are themselves a dictionary,
        will have a `dataclass` built and inserted in `self.classes`.

        The field for that value will be annotated as an instance of that secondary `dataclass`.
        """
        assigns: list[ast.AnnAssign] = []
        for key, val in data.items():
            if self.recursive and isinstance(val, dict):
                dataclass = self.build_dataclass(key, val)  # type: ignore
                self.add_dataclass(dataclass)
                assigns.append(
                    self.build_annotated_assignment(
                        key, utilities.key_to_classname(key), False
                    )
                )
            else:
                assigns.append(self.build_annotated_assignment(key, val))
        return assigns

    def build_annotated_assignment(
        self, name: str, val: Any, evaluate_type: bool = True
    ) -> ast.AnnAssign:
        """Return an annotated assignment node with `name` and an annotation based on the type of `val`.

        If `evaluate_type` is `False`, then `val` will be used directly as the type annotation instead of `type(val).__name__`.
        """
        return ast.AnnAssign(
            ast.Name(name, ast.Store()),
            ast.Name(utilities.build_type(val) if evaluate_type else val, ast.Load()),
            None,
            1,
        )

    def build_dataclass(
        self, name: str, data: dict[str, Any], add_methods: bool = False
    ) -> ast.ClassDef:
        """Build a `dataclass` with `name` from `data` and insert it into `self.classes`.

        If `add_methods` is `True`, `load()` and `dump()` functions will be added to the class.
        """
        class_ = ast.ClassDef(
            utilities.key_to_classname(name),
            [],
            [],
            self.annotated_assignments_from_dict(data),
            [self.dataclass_node],
        )
        if add_methods:
            class_.body.extend([self.load_node, self.dump_node])
        return class_

    # Seat |======================================== Main ========================================|

    def generate(self, name: str, data: dict[str, Any]) -> str:
        """Generate a `dataclass` with `name` from `data` and return the source code.

        Currently, all keys in `data` and any of its nested dictionaries must be valid Python variable names.
        """
        for node in self.import_nodes:
            if node not in self.module.body:
                self.module.body.insert(0, node)
        dataclass = self.build_dataclass(name, data, True)
        self.add_dataclass(dataclass)
        self.fix_order()
        return self.source


def generate_from_file(
    datapath: Pathish, outpath: Pathish | None = None, recursive: bool = True
):
    """Generate a `dataclass` named after the file `datapath` points at.

    If `outpath` is not given, the output file will be the same as `datapath`, but with a `.py` extension.

    Can be any `.toml` or `.json` file where all keys are valid Python variable names.

    If `recursive` is `True`, dictionary values will be converted to dataclasses.
    """

    datapath = Pathier(datapath)
    if outpath:
        outpath = Pathier(outpath)
    else:
        outpath = datapath.with_suffix(".py")
    module = ast.parse(outpath.read_text()) if outpath.exists() else None  # type: ignore
    data = datapath.loads()
    fool = TomFoolery(module, recursive)  # type: ignore
    source = fool.generate(datapath.stem, data)
    source = source.replace("filepath", datapath.name)
    try:
        source = fool.format_str(source)
    except Exception as e:
        print("Unable to format output.")
    outpath.write_text(source)
