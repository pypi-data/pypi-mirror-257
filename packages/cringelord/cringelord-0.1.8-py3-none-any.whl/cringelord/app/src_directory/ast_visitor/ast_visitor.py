import ast

from . import (
    environ_get_call,
    environ_subscript,
    getenv_call,
    get_cringe_setting_call
)


class CringeASTVisitor(ast.NodeVisitor):
    env_call_var_names = set()

    def clear(self):
        self.env_call_var_names = set()

    def visit_Subscript(self, subscript):
        if environ_subscript.is_environ_subscript(subscript):
            self._parse_visit(subscript, environ_subscript)

        self.generic_visit(subscript)

    def visit_Call(self, call):
        if environ_get_call.is_environ_get_call(call):
            self._parse_visit(call, environ_get_call)
        elif getenv_call.is_getenv_call(call):
            self._parse_visit(call, getenv_call)
        elif get_cringe_setting_call.is_get_cringe_setting_call(call):
            self._parse_visit(call, get_cringe_setting_call)

        self.generic_visit(call)

    def _parse_visit(self, node, helper):
        if value := helper.get_value(node):
            self.env_call_var_names.add(value)
