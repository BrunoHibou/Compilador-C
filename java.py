import subprocess

# Simplified example AST (normally produced by your semantic analyzer)
ast = {
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
generated_java_code = generate_java_code(example_ast)

# Debug: Print the generated Java code for verification
print("Generated Java Code:\n", generated_java_code)

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
