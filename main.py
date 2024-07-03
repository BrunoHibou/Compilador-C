import re
import subprocess

class Lexer:
    def __init__(self, input_code):
        self.tokens = self.tokenize(input_code)
        self.current_token_index = 0
        #print (self.tokens)

    def tokenize(self, input_code):
        token_specification = [
            ('NUMBER',   r'\d+'),
            ('TYPE',     r'\bint\b|\bfloat\b|\bvoid\b'),
            ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),
            ('ASSIGN',   r'='),
            ('SEMICOLON',r';'),
            ('LPAREN',   r'\('),
            ('RPAREN',   r'\)'),
            ('LBRACE',   r'\{'),
            ('RBRACE',   r'\}'),
            ('COMMA',    r','),
            ('RETURN',   r'\breturn\b'),
            ('SKIP',     r'[ \t\n]+'), # skip whitespace
            ('MISMATCH', r'.'),        # any other character
        ]
        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
        get_token = re.compile(tok_regex).match
        line_num = 1
        line_start = 0
        tokens = []
        mo = get_token(input_code)
        while mo is not None:
            kind = mo.lastgroup
            value = mo.group(kind)
            if kind == 'NUMBER':
                value = int(value)
            elif kind == 'SKIP':
                pass
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected on line {line_num}')
            else:
                tokens.append((kind, value))
            mo = get_token(input_code, mo.end())
        tokens.append(('EOF', 'EOF'))
        return tokens

    def next_token(self):
        self.current_token_index += 1

    def peek_token(self):
        return self.tokens[self.current_token_index]

    def current_token(self):
        return self.tokens[self.current_token_index]

    def match(self, expected_type):
        token_type, token_value = self.current_token()
        if token_type == expected_type:
            self.next_token()
            return token_value
        else:
            pass
            #raise RuntimeError(f"Expected token {expected_type} but got {token_type}")

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

    def parse(self):
        return self.parse_program()

    def parse_program(self):
        program_node = {
            "type": "Program",
            "body": []
        }
        while self.lexer.peek_token()[0] != 'EOF':
            program_node["body"].append(self.parse_function_declaration())
        return program_node

    def parse_function_declaration(self):
        return_type = self.lexer.match('TYPE')
        function_name = self.lexer.match('ID')
        self.lexer.match('LPAREN')
        params = self.parse_parameters()
        self.lexer.match('RPAREN')
        self.lexer.match('LBRACE')
        body = self.parse_block()
        self.lexer.match('RBRACE')
        return {
            "type": "FunctionDeclaration",
            "name": function_name,
            "returnType": return_type,
            "params": params,
            "body": body
        }

    def parse_parameters(self):
        params = []
        if self.lexer.peek_token()[0] != 'RPAREN':
            while True:
                param_type = self.lexer.match('TYPE')
                param_name = self.lexer.match('ID')
                params.append({"datatype": param_type, "name": param_name})
                if self.lexer.peek_token()[0] == 'COMMA':
                    self.lexer.match('COMMA')
                else:
                    break
        return params

    def parse_block(self):
        block = []
        while self.lexer.peek_token()[0] != 'RBRACE':
            block.append(self.parse_statement())
        return block

    def parse_statement(self):
        token_type, token_value = self.lexer.peek_token()
        if token_type == 'TYPE':
            return self.parse_variable_declaration()
        elif token_type == 'ID':
            return self.parse_assignment()
        elif token_type == 'RETURN':
            return self.parse_return_statement()
        elif token_type == 'SEMICOLON':
            self.lexer.match('SEMICOLON')
            return None  # Ignore standalone semicolons
        else:
            raise RuntimeError(f"Unexpected token {token_type}")

    def parse_variable_declaration(self):
        datatype = self.lexer.match('TYPE')
        var_name = self.lexer.match('ID')
        self.lexer.match('SEMICOLON')
        return {
            "type": "VariableDeclaration",
            "datatype": datatype,
            "name": var_name
        }

    def parse_assignment(self):
        var_name = self.lexer.match('ID')
        self.lexer.match('ASSIGN')
        value = self.parse_expression()
#        if value is None:
#           raise RuntimeError(f"Expected an expression after assignment but got {self.lexer.peek_token()}")
        self.lexer.match('SEMICOLON')
        return {
            "type": "AssignmentExpression",
            "left": {
                "type": "Identifier",
                "name": var_name
            },
            "right": value
        }

    def parse_return_statement(self):
        self.lexer.match('RETURN')
        argument = self.parse_expression()
        self.lexer.match('SEMICOLON')
        return {
            "type": "ReturnStatement",
            "argument": argument
        }

    def parse_expression(self):
        token_type, token_value = self.lexer.peek_token()
        if token_type == 'NUMBER':
            self.lexer.match('NUMBER')
            return {
                "type": "Literal",
                "value": token_value
            }
        elif token_type == 'ID':
            var_name = self.lexer.match('ID')
            return {
                "type": "Identifier",
                "name": var_name
            }
        else:
            return None
        
class SemanticAnalyzer:
    def __init__(self, syntax_tree):
        self.syntax_tree = syntax_tree
        self.successful = False  # Flag to track successful analysis

    def analyze(self):
        self.visit(self.syntax_tree)
        self.successful = True  # Mark analysis as successful at the end

    def visit(self, node):
        if node is None:
            return  # Handle None nodes gracefully
        method_name = f"visit_{node['type']}"
        visit_method = getattr(self, method_name, self.generic_visit)
        return visit_method(node)

    def generic_visit(self, node):
        # Default handling if no specific visit method is defined
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, dict):
                    self.visit(value)
                elif isinstance(value, list):
                    for item in value:
                        self.visit(item)

    def visit_Program(self, node):
        for element in node.get("body", []):
            self.visit(element)

    def visit_FunctionDeclaration(self, node):
        for statement in node.get("body", []):
            self.visit(statement)

    def visit_AssignmentExpression(self, node):
        left_type = self.visit(node.get("left"))
        right_type = self.visit(node.get("right"))
        # Further semantic analysis logic for assignments

    def visit_Identifier(self, node):
        # Semantic analysis for identifier nodes
        pass

    def visit_Literal(self, node):
        # Semantic analysis for literal nodes
        pass

# Example usage
input_code = """
int main() {
    int a;
    a = 5;
    return a;
}
"""

lexer = Lexer(input_code)
parser = Parser(lexer)
syntax_tree = parser.parse()

analyzer = SemanticAnalyzer(syntax_tree)
analyzer.analyze()
ast = analyzer.syntax_tree
print(ast)

import subprocess

# Simplified example AST (normally produced by your semantic analyzer)
example_ast = {
    "type": "Program",
    "body": [
        {
            "type": "ClassDeclaration",
            "name": "MainClass",
            "body": [
                {
                    "type": "MethodDeclaration",
                    "name": "main",
                    "returnType": "void",
                    "params": [{"type": "String[]", "name": "args"}],
                    "body": [
                        {"type": "VariableDeclaration", "datatype": "int", "name": "a"},
                        {"type": "AssignmentExpression", "left": {"type": "Identifier", "name": "a"}, "right": {"type": "Literal", "value": 5}},
                        {"type": "ReturnStatement", "argument": {"type": "Identifier", "name": "a"}}
                    ]
                }
            ]
        }
    ]
}

# Code generation function to convert AST to Java code
def generate_java_code(ast):
    code = ""
    if ast["type"] == "Program":
        for element in ast["body"]:
            code += generate_java_code(element)
    elif ast["type"] == "ClassDeclaration":
        code += f"public class {ast['name']} {{\n"
        for member in ast["body"]:
            code += generate_java_code(member)
        code += "}\n"
    elif ast["type"] == "MethodDeclaration":
        params = ", ".join([f"{param['type']} {param['name']}" for param in ast["params"]])
        code += f"public static {ast['returnType']} {ast['name']}({params}) {{\n"
        for statement in ast["body"]:
            code += generate_java_code(statement)
        code += "}\n"
    elif ast["type"] == "VariableDeclaration":
        code += f"{ast['datatype']} {ast['name']};\n"
    elif ast["type"] == "AssignmentExpression":
        left = generate_java_code(ast["left"])
        right = generate_java_code(ast["right"])
        code += f"{left} = {right};\n"
    elif ast["type"] == "Identifier":
        code += ast["name"]
    elif ast["type"] == "Literal":
        code += str(ast["value"])
    elif ast["type"] == "ReturnStatement":
        argument = generate_java_code(ast["argument"])
        code += f"System.out.println({argument});\nreturn;\n"
    elif ast is None:
        code += "null"
    return code

# Generate the Java code from the AST
import subprocess

# Simplified example AST (normally produced by your semantic analyzer)
example_ast = {
    "type": "Program",
    "body": [
        {
            "type": "ClassDeclaration",
            "name": "MainClass",
            "body": [
                {
                    "type": "MethodDeclaration",
                    "name": "main",
                    "returnType": "void",
                    "params": [{"type": "String[]", "name": "args"}],
                    "body": [
                        {"type": "VariableDeclaration", "datatype": "int", "name": "a"},
                        {"type": "AssignmentExpression", "left": {"type": "Identifier", "name": "a"}, "right": {"type": "Literal", "value": 5}},
                        {"type": "ReturnStatement", "argument": {"type": "Identifier", "name": "a"}}
                    ]
                }
            ]
        }
    ]
}

# Code generation function to convert AST to Java code
def generate_java_code(ast):
    code = ""
    if ast["type"] == "Program":
        for element in ast["body"]:
            code += generate_java_code(element)
    elif ast["type"] == "ClassDeclaration":
        code += f"public class {ast['name']} {{\n"
        for member in ast["body"]:
            code += generate_java_code(member)
        code += "}\n"
    elif ast["type"] == "MethodDeclaration":
        params = ", ".join([f"{param['type']} {param['name']}" for param in ast["params"]])
        code += f"public static {ast['returnType']} {ast['name']}({params}) {{\n"
        for statement in ast["body"]:
            code += generate_java_code(statement)
        code += "}\n"
    elif ast["type"] == "VariableDeclaration":
        code += f"{ast['datatype']} {ast['name']};\n"
    elif ast["type"] == "AssignmentExpression":
        left = generate_java_code(ast["left"])
        right = generate_java_code(ast["right"])
        code += f"{left} = {right};\n"
    elif ast["type"] == "Identifier":
        code += ast["name"]
    elif ast["type"] == "Literal":
        code += str(ast["value"])
    elif ast["type"] == "ReturnStatement":
        argument = generate_java_code(ast["argument"])
        code += f"System.out.println({argument});\nreturn;\n"
    elif ast is None:
        code += "null"
    return code

# Generate the Java code from the AST
generated_java_code = generate_java_code(ast)
print(generate_java_code)

# Save the generated Java code to a file
java_file_path = 'MainClass.java'
with open(java_file_path, 'w') as java_file:
    java_file.write(generated_java_code)

# Compile the generated Java code using javac
compile_command = ['javac', java_file_path]
try:
    subprocess.run(compile_command, check=True)
    print("Compilation successful!")
except subprocess.CalledProcessError as e:
    print(f"Compilation failed: {e}")

# Run the compiled Java program
run_command = ['java', 'MainClass']
try:
    subprocess.run(run_command, check=True)
    print("Execution successful!")
except subprocess.CalledProcessError as e:
    print(f"Execution failed: {e}")

# Print the generated Java code for verification
print("Generated Java Code:\n", generated_java_code)
