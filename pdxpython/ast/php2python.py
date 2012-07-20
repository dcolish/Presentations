import ast
from ast import Assign, Load, Module, Name, Print, Store

node_map = {
    'Assignment': dict(pynode='Assign',
                       mappers={'targets': 'node', 'value': 'expr'},
                       types={'left': 'list'},
                       args={'ctx': ast.Store(lineno=0, col_offset=0)}),

    'Echo': dict(pynode='Print',
                 mappers={'values': 'nodes'},
                 types={'left': list},
                 args={'nl': True, 'ctx': ast.Load(lineno=0, col_offset=0)}),

    'Variable': dict(pynode='Name',
                     mappers={'id': 'name'},
                     types={'left': 'var'},
                     args={'ctx': ast.Store(lineno=0, col_offset=0)}),
    }

body = []


def eval_node(phpnode, ctx=None):

    node_type, el = phpnode.generic()
    mapdef = node_map[node_type]
    py_ast_class = getattr(ast, mapdef['pynode'])
    instance = py_ast_class(lineno=0, col_offset=0,
                            **mapdef.get('args', {}))
    if ctx:
        instance.ctx = ctx
    else:
        ctx = getattr(instance, 'ctx')

    for key, val in mapdef['mappers'].iteritems():
        sub_expr = getattr(phpnode, val)

        if isinstance(sub_expr, Node):
            if mapdef['types']['left'] == 'list':
                sub_expr = [eval_node(sub_expr, ctx)]
            else:
                sub_expr = eval_node(sub_expr, ctx)

        elif isinstance(sub_expr, list):
            list_expr = sub_expr
            sub_expr = []
            for list_node in list_expr:
                if not isinstance(list_node, Node):
                    if isinstance(list_node, str):
                        sub_expr.append(ast.Str(s=list_node, lineno=0,
                                                col_offset=0))
                else:
                    sub_expr.append(eval_node(list_node, ctx))

        elif isinstance(sub_expr, int):
            sub_expr = ast.Num(n=sub_expr, lineno=0, col_offset=0)

        setattr(instance, key, sub_expr)

    return instance

for node in output:
    body.append(eval_node(node))

expr = ast.Module(body, lineno=0, col_offset=0)

eval(compile(ast.parse(expr), '<string>', mode='exec'))

