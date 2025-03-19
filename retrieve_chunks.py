from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# 🔥 Load the same model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 🎯 Load FAISS Index
index = faiss.read_index("faiss_cpp.index")

def retrieve_cpp_chunks(query):
    """Retrieves relevant C++ code chunks based on a query."""
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k=3)

    # Read the extracted chunks from file
    with open("test1.cpp", "r") as f:
        lines = f.readlines()

    results = []
    for idx in indices[0]:
        if idx < len(lines):
            results.append(lines[idx])

    return results

if __name__ == "__main__":
    query = input("Enter your C++ query: ")
    retrieved_chunks = retrieve_cpp_chunks(query)

    for chunk in retrieved_chunks:
        print(chunk, "\n" + "=" * 50)
