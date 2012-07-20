import ast
from ast import Assign, Load, Module, Name, Print, Store


expr2 = Module(body=[Assign(targets=[Name(id='a', ctx=Store())],
                            value=ast.Num(n=12)),
                     Print(values=[Name(id='a', ctx=Load())],
                           nl=True),
                     ])

print ast.dump(ast.fix_missing_locations(expr2))

eval(compile(ast.parse(expr2), '<string>', mode='exec'))
