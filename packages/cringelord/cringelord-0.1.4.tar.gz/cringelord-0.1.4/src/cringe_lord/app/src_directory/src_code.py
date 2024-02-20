import ast
from typing import Set

from cringe_lord.app.src_directory.ast_visitor.ast_visitor import CringeASTVisitor


def get_env_call_var_names(src_code: str) -> Set[str]:
    visitor = CringeASTVisitor()
    visitor.clear()

    ast_tree = ast.parse(src_code)
    visitor.visit(ast_tree)

    return visitor.env_call_var_names
