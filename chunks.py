import faiss
import json
import numpy as np
import re
from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Read C++ file
cpp_file = "test.cpp"  # Change this to your C++ file path
try:
    with open(cpp_file, "r", encoding="utf-8") as f:
        cpp_code = f.read()
except FileNotFoundError:
    print(f"❌ Error: File '{cpp_file}' not found.")
    exit(1)

# Regex to extract functions (handling return types and function names correctly)
function_pattern = re.compile(r"\b([a-zA-Z_][a-zA-Z0-9_<>:]*)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)\s*{([\s\S]*?)\n}")
functions = []
for match in function_pattern.finditer(cpp_code):
    return_type = match.group(1).strip()
    function_name = match.group(2).strip()
    parameters = match.group(3).strip()
    function_body = match.group(4).strip()
    function_code = f"{return_type} {function_name}({parameters}){{{function_body}}}"
    functions.append({"type": "function", "name": function_name, "code": function_code})

# Regex to extract classes
class_pattern = re.compile(r"class\s+(\w+)\s*{([\s\S]*?)};")
classes = []
for match in class_pattern.finditer(cpp_code):
    class_name = match.group(1).strip()
    class_body = match.group(2).strip()
    class_code = f"class {class_name} {{{class_body}}};"
    classes.append({"type": "class", "name": class_name, "code": class_code})

# Combine functions and classes
chunks = functions + classes

# Save chunks as JSON
json_file = "chunks.json"
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=4)
print(f"✅ Functions and Classes saved in {json_file}")

# Print all extracted functions and classes
print("\n🔹 Extracted Functions and Classes:")
for chunk in chunks:
    print(f"\n📌 {chunk['type'].capitalize()} Name: {chunk['name']}\nCode:\n{chunk['code']}\n" + "-" * 50)

# Convert chunks to embeddings
if chunks:
    chunk_texts = [chunk["code"] for chunk in chunks]
    chunk_embeddings = np.array([model.encode(text) for text in chunk_texts], dtype="float32")

    # Create FAISS index
    dimension = chunk_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(chunk_embeddings)

    # Save FAISS index
    faiss.write_index(index, "chunks.index")
    print("✅ Functions and Classes indexed in FAISS")
else:
    print("❌ No functions or classes extracted. Please check your input file.")
