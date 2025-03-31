import re

# Specify the input C++ file
cpp_file = "modified.cpp"

# Read the C++ file
with open(cpp_file, "r", encoding="utf-8") as f:
    cpp_code = f.read()

# Regular expressions to detect classes and functions
class_pattern = re.compile(r"(class\s+\w+\s*{)", re.MULTILINE)
function_pattern = re.compile(r"(\b\w+\s+\w*\s*\([^)]*\)\s*{)", re.MULTILINE)

# Add comments before and after classes
cpp_code = class_pattern.sub(r"// ⬇⬇ Class starts ⬇⬇\n\1", cpp_code)
cpp_code = cpp_code.replace("};", "};\n// ⬆⬆ Class ends ⬆⬆")

# Add comments before and after functions
cpp_code = function_pattern.sub(r"// ⬇⬇ Function starts ⬇⬇\n\1", cpp_code)
cpp_code = cpp_code.replace("}", "}\n// ⬆⬆ Function ends ⬆⬆")

# Save the modified file
with open(cpp_file, "w", encoding="utf-8") as f:
    f.write(cpp_code)

print(f"✅ Comments added to functions and classes in {cpp_file}")
