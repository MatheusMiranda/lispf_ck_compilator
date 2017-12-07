from getch import getche
import click
import pprint
import ox

lexer = ox.make_lexer([
    ('COMMENT', r';(.)*'),
    ('NEW_LINE', r'\n+'),
    ('OPEN_BRACKET', r'\('),
    ('CLOSE_BRACKET', r'\)'),
    ('NAME', r'[a-zA-Z_][a-zA-Z_0-9-]*'),
    ('NUMBER', r'\d+(\.\d*)?'),
])

token_list = [
    'NAME',
    'NUMBER',
    'OPEN_BRACKET',
    'CLOSE_BRACKET',
]

identity = lambda x: x

parser = ox.make_parser([

    ('tuple : OPEN_BRACKET elements CLOSE_BRACKET', lambda a, x, b: x),
    ('tuple : OPEN_BRACKET CLOSE_BRACKET', lambda a, b: '[]'),
    ('elements : term elements', lambda x, xs: [x] + xs),
    ('elements : term', lambda x: [x]),
    ('term : atom', identity),
    ('term : tuple', identity),
    ('atom : NAME', identity),
    ('atom : NUMBER', lambda x: int(x)),

] , token_list)

data = [0]
ptr = 0
code_ptr = 0
breakpoints = []

@click.command()
@click.argument('source_file',type=click.File('r'))
def build(source_file):

    print_ast = pprint.PrettyPrinter(width=60, compact=True)
    source = source_file.read()

    tokens = lexer(source)

    tokens = [value for value in tokens if str(value)[:7] != 'COMMENT' and str(value)[:8] != 'NEW_LINE']
    ast = parser(tokens)

    interpret_lisp_f_ck_code(ast, ptr)

function_definition = {}

def generate_brain_f_ck_code(command):
    character = '' 
    if command == 'inc':
        character = '+'
    
    elif command == 'dec':
        character = '-'
    
    elif command == 'right':
        character = '>'
    
    elif command == 'left':
        character = '<'
    
    elif command == 'print':
        character = '.'
    
    elif command == 'read':
        character = ','

    return character

def interpret_lisp_f_ck_code(source, ptr):
    brain_f_ck_code = ""

    for command in source:
        brain_f_ck_code += process_by_command(command)

    print(brain_f_ck_code)

def process_by_command(command):
    if isinstance(command, list):
        if command[0] == 'add':
            return command[1] * '+'
    
        elif command[0] == 'sub':
            return command[1] * '-'
            
        elif command[0] == 'loop':
            aux = ''
            aux += '['
            for i in range(1,len(command)):
                element_command = command[i]
                aux += process_by_command(element_command)
            aux += ']'
            return aux
    
    elif isinstance(command, str):
        return generate_brain_f_ck_code(command)
    

if __name__ == '__main__':
    build()
