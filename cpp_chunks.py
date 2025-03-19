import clang.cindex

# 🛠 Set the correct libclang path (modify as needed)
#clang.cindex.Config.set_library_file("/usr/lib/llvm-14/lib/libclang.so")  # Linux
clang.cindex.Config.set_library_file("C:\\Program Files\\LLVM\\bin\\libclang.dll")  # Windows

def extract_cpp_blocks(file_path):
    """Extracts functions, classes, and structs from C++ code."""
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    chunks = []

    def visit_node(node):
        if node.kind in [
            clang.cindex.CursorKind.FUNCTION_DECL,
            clang.cindex.CursorKind.CLASS_DECL,
            clang.cindex.CursorKind.STRUCT_DECL,
        ]:
            start = node.extent.start.line - 1
            end = node.extent.end.line
            with open(file_path, "r") as f:
                lines = f.readlines()[start:end]
                chunks.append("".join(lines))

        for child in node.get_children():
            visit_node(child)

    visit_node(translation_unit.cursor)
    return chunks

# Example usage
cpp_file = "test1.cpp"
chunks = extract_cpp_blocks(cpp_file)

for chunk in chunks:
    print(chunk, "\n" + "=" * 50)
